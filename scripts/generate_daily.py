"""
Günlük Burç Yorumları Üretimi
Her gün otomatik çalışır, 12 burç için günlük yorum üretir
"""

import os
from datetime import datetime
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

def create_daily_prompt(burc_data, tarih):
    """Günlük yorum promptu"""
    return f"""Sen profesyonel bir astrologsun. {burc_data['ad']} burcu için {tarih} tarihli günlük burç yorumu yaz.

BURÇ: {burc_data['ad']} ({burc_data['tarih']})
TARİH: {tarih}

YAZIYI ŞU FORMATTA YAZ:

## Genel Enerji
2-3 cümle ile günün genel enerjisini anlat

## Aşk ve İlişkiler
2-3 cümle ile aşk hayatı için öngörüler

## Kariyer ve İş
2-3 cümle ile iş hayatı için tavsiyeler

## Sağlık
1-2 cümle ile sağlık konusunda dikkat edilmesi gerekenler

## Şans Faktörleri
- **Şans Puanı:** 7/10 (1-10 arası bir puan)
- **Şans Sayısı:** {burc_data['sans_sayilari'][0]} (burcun şans sayılarından birini kullan)
- **Şans Rengi:** {burc_data['sans_renkleri'][0]} (burcun şans renklerinden birini kullan)

## Günün Tavsiyesi
1 cümle, kısa ve öz bir tavsiye

ÖNEMLİ:
- Tamamen Türkçe yaz
- Pozitif ama gerçekçi bir dil kullan
- Spesifik ve kişisel önerilerde bulun
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## ile başlat"""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir astrolog ve günlük burç yorumları yazarısın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.8,
                max_tokens=1500,
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

def create_daily_markdown(burc_key, burc_data, content, tarih):
    """Günlük yorum markdown dosyası oluştur"""
    # Klasör oluştur
    burc_dir = CONTENT_DIR / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    tarih_url_format = now.strftime("%d-%m-%Y")

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Günlük Yorum - {tarih}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için {tarih} günlük burç yorumu. Aşk, kariyer, sağlık ve genel enerji öngörüleri."
keywords: ["{burc_data['ad']} günlük", "günlük {burc_data['ad']}", "{burc_data['ad']} bugün", "{burc_data['ad']} yorum {tarih}"]
layout: "single"
type: "gunluk"
burc: "{burc_data['ad']}"
tarih: "{tarih}"
draft: false
---

# {burc_data['ad']} Burcu Günlük Yorum - {tarih}

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = burc_dir / 'gunluk.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ {burc_data['ad']} günlük yorum güncellendi")

def main():
    """Ana fonksiyon"""
    # Bugünün tarihi (Türkçe format)
    now = datetime.now()
    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    tarih = f"{now.day} {aylar[now.month]} {now.year}"

    print(f"🌟 Günlük Burç Yorumları Üretimi - {tarih}\n")

    # Content dizini oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f"📝 {burc_data['ad']} günlük yorumu üretiliyor...")

        # Prompt oluştur
        prompt = create_daily_prompt(burc_data, tarih)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Markdown dosyası oluştur
            create_daily_markdown(burc_key, burc_data, content, tarih)
            success_count += 1
        else:
            failed_count += 1
            print(f"❌ {burc_data['ad']} üretilemedi!")

        # Rate limiting
        if burc_key != list(BURCLAR.keys())[-1]:
            time.sleep(2)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET - {tarih}")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
