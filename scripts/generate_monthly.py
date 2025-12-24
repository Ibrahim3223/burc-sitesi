"""
Aylık Burç Yorumları Üretimi
Her ayın 1'inde otomatik çalışır
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

def get_month_info():
    """Ay bilgilerini al"""
    now = datetime.now()
    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

    ay_adi = aylar[now.month]
    yil = now.year

    return f"{ay_adi} {yil}", ay_adi, yil

def create_monthly_prompt(burc_data, ay_tam):
    """Aylık yorum promptu"""
    return f"""Sen profesyonel bir astrologsun. {burc_data['ad']} burcu için {ay_tam} aylık burç yorumu yaz.

BURÇ: {burc_data['ad']} ({burc_data['tarih']})
AY: {ay_tam}

YAZIYI ŞU FORMATTA YAZ:

## Ayın Genel Değerlendirmesi
4-5 cümle ile ayın genel enerjisi, planetsel hareketler ve burç için öne çıkan temalar.

## Aşk ve İlişkiler
4-5 cümle ile aylık aşk hayatı. İlk yarı ve ikinci yarı olarak ayır. Bekar ve ilişkisi olanlara ayrı değin.

## Kariyer ve İş Hayatı
4-5 cümle ile iş hayatındaki gelişmeler. Hangi projelere ağırlık vermeli, hangi konularda dikkatli olmalı.

## Finans ve Para
3-4 cümle ile gelir-gider durumu, yatırım fırsatları, bütçe yönetimi.

## Sağlık ve Enerji
2-3 cümle ile fiziksel ve mental sağlık durumu. Hangi alanlara dikkat edilmeli.

## Ayın Önemli Tarihleri

### [Tarih 1] - [Olay]
Örnek: 5 {ay_tam.split()[0]} - Yeni Ay
Açıklama (2 cümle)

### [Tarih 2] - [Olay]
Örnek: 15 {ay_tam.split()[0]} - Merkür Retrosu
Açıklama (2 cümle)

### [Tarih 3] - [Olay]
Örnek: 23 {ay_tam.split()[0]} - Venüs Geçişi
Açıklama (2 cümle)

## Ayın Tavsiyesi
2-3 cümle, ay boyunca nelere odaklanmalı, hangi fırsatları değerlendirmeli.

ÖNEMLİ:
- Tamamen Türkçe yaz
- Pozitif ama gerçekçi bir dil kullan
- Spesifik tarihler ve olaylar belirt
- Ay boyunca planetsel hareketleri referans göster
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
                        "content": "Sen profesyonel bir astrolog ve aylık burç yorumları yazarısın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.8,
                max_tokens=2500,
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

def create_monthly_markdown(burc_key, burc_data, content, ay_tam):
    """Aylık yorum markdown dosyası oluştur"""
    # Klasör oluştur
    burc_dir = CONTENT_DIR / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Aylık Yorum - {ay_tam}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için {ay_tam} aylık burç yorumu. Aşk, kariyer, sağlık, finans ve aylık öngörüler."
keywords: ["{burc_data['ad']} aylık", "aylık {burc_data['ad']}", "{burc_data['ad']} {ay_tam}", "{burc_data['ad']} ay yorumu"]
layout: "single"
type: "aylik"
burc: "{burc_data['ad']}"
ay: "{ay_tam}"
draft: false
---

# {burc_data['ad']} Burcu Aylık Yorum - {ay_tam}

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = burc_dir / 'aylik.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ {burc_data['ad']} aylık yorum güncellendi")

def main():
    """Ana fonksiyon"""
    ay_tam, ay_adi, yil = get_month_info()

    print(f"🌟 Aylık Burç Yorumları Üretimi - {ay_tam}\n")

    # Content dizini oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f"📝 {burc_data['ad']} aylık yorumu üretiliyor...")

        # Prompt oluştur
        prompt = create_monthly_prompt(burc_data, ay_tam)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Markdown dosyası oluştur
            create_monthly_markdown(burc_key, burc_data, content, ay_tam)
            success_count += 1
        else:
            failed_count += 1
            print(f"❌ {burc_data['ad']} üretilemedi!")

        # Rate limiting
        if burc_key != list(BURCLAR.keys())[-1]:
            time.sleep(2)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET - {ay_tam}")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
