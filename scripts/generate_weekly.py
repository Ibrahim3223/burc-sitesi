"""
Haftalık Burç Yorumları Üretimi
Her Pazartesi otomatik çalışır
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import time
from burc_data import BURCLAR

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'burc'

def get_week_range():
    """Haftanın tarih aralığını hesapla (Pazartesi-Pazar)"""
    now = datetime.now()
    # Pazartesi bul (weekday 0 = Pazartesi)
    days_to_monday = now.weekday()
    monday = now - timedelta(days=days_to_monday)
    sunday = monday + timedelta(days=6)

    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

    monday_str = f"{monday.day} {aylar[monday.month]}"
    sunday_str = f"{sunday.day} {aylar[sunday.month]} {sunday.year}"

    return f"{monday_str} - {sunday_str}", monday, sunday

def create_weekly_prompt(burc_data, tarih_araligi):
    """Haftalık yorum promptu"""
    return f"""Sen profesyonel bir astrologsun. {burc_data['ad']} burcu için {tarih_araligi} haftalık burç yorumu yaz.

BURÇ: {burc_data['ad']} ({burc_data['tarih']})
HAFTA: {tarih_araligi}

YAZIYI ŞU FORMATTA YAZ:

## Haftanın Genel Enerjisi
3-4 cümle ile haftanın genel enerjisini anlat. Planetsel hareketlere ve burç özelliklerine göre yorumla.

## Aşk ve İlişkiler
3-4 cümle ile haftalık aşk hayatı öngörüleri. Bekarlara ve ilişkisi olanlara ayrı ayrı değin.

## Kariyer ve Finans
3-4 cümle ile iş hayatı ve para konularında bu hafta neler olacak.

## Sağlık ve Wellness
2-3 cümle ile sağlık ve enerji durumu. Hangi aktivitelere ağırlık vermeli.

## Haftanın Önemli Günleri

### Pazartesi
Günün enerjisi ve tavsiye (1-2 cümle)

### Çarşamba
Günün enerjisi ve tavsiye (1-2 cümle)

### Cuma
Günün enerjisi ve tavsiye (1-2 cümle)

## Haftanın Tavsiyesi
2 cümle, hafta boyunca yapılması gerekenler

ÖNEMLİ:
- Tamamen Türkçe yaz
- Pozitif ama gerçekçi bir dil kullan
- Spesifik günler için özel önerilerde bulun
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## veya ### ile başlat"""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir astrolog ve haftalık burç yorumları yazarısın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.8,
                max_tokens=2000,
                top_p=0.9
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"❌ Hata (Deneme {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"⏳ {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
            else:
                return None

    return None

def create_weekly_markdown(burc_key, burc_data, content, tarih_araligi):
    """Haftalık yorum markdown dosyası oluştur"""
    # Klasör oluştur
    burc_dir = CONTENT_DIR / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için {tarih_araligi} haftalık burç yorumu. Aşk, kariyer, sağlık ve haftalık öngörüler."
keywords: ["{burc_data['ad']} haftalık", "haftalık {burc_data['ad']}", "{burc_data['ad']} bu hafta", "{burc_data['ad']} hafta yorumu"]
layout: "single"
type: "haftalik"
burc: "{burc_data['ad']}"
tarih_araligi: "{tarih_araligi}"
draft: false
---

# {burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = burc_dir / 'haftalik.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ {burc_data['ad']} haftalık yorum güncellendi")

def main():
    """Ana fonksiyon"""
    tarih_araligi, monday, sunday = get_week_range()

    print(f"🌟 Haftalık Burç Yorumları Üretimi - {tarih_araligi}\n")

    # Content dizini oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f"📝 {burc_data['ad']} haftalık yorumu üretiliyor...")

        # Prompt oluştur
        prompt = create_weekly_prompt(burc_data, tarih_araligi)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Markdown dosyası oluştur
            create_weekly_markdown(burc_key, burc_data, content, tarih_araligi)
            success_count += 1
        else:
            failed_count += 1
            print(f"❌ {burc_data['ad']} üretilemedi!")

        # Rate limiting
        if burc_key != list(BURCLAR.keys())[-1]:
            time.sleep(2)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET - {tarih_araligi}")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
