"""
12 Burç Ana Sayfası İçerik Üretimi
Groq API ile her burç için detaylı içerik üretir
"""

import os
import sys
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

def create_burc_prompt(burc_key, burc_data):
    """Burç için detaylı içerik üretim promptu"""
    return f"""Sen profesyonel bir astrolog ve içerik yazarısın. {burc_data['ad']} burcu için kapsamlı bir burç rehberi yazacaksın.

BURÇ BİLGİLERİ:
- Burç: {burc_data['ad']}
- Tarih: {burc_data['tarih']}
- Element: {burc_data['element']}
- Nitelik: {burc_data['nitelik']}
- Yönetici Gezegen: {burc_data['gezegen']}
- Şans Günü: {burc_data['sans_gunu']}
- Şans Renkleri: {', '.join(burc_data['sans_renkleri'])}
- Uyumlu Burçlar: {', '.join(burc_data['uyumlu_burclar'])}

YAZILACAK BÖLÜMLER (Markdown formatında):

## Genel Bilgiler
- Burç tarih aralığı ve temel özellikler (100 kelime)

## Kişilik Özellikleri
{burc_data['ad']} burcunun detaylı karakter analizi. Güçlü yönleri, zayıf yönleri, genel davranış kalıpları. (500-700 kelime)

## Aşk ve İlişkiler
{burc_data['ad']} burcunun aşk hayatı, ilişkilerde nasıl davrandığı, ideal partner özellikleri, beklentileri. (300-400 kelime)

## Kariyer ve İş Hayatı
Uygun meslekler, çalışma tarzı, iş hayatındaki başarı faktörleri, liderlik özellikleri. (300-400 kelime)

## Sağlık
Dikkat etmesi gereken sağlık konuları, hassas organlar, sağlık önerileri. (200-300 kelime)

## Para ve Finans
Para yönetimi, harcama alışkanlıkları, yatırım eğilimleri. (200-300 kelime)

## Aile ve Arkadaşlık
Aile içindeki rolü, arkadaşlık anlayışı, sosyal ilişkiler. (200-300 kelime)

## Ünlü {burc_data['ad']} Burcu Kişileri
Bu burçtan 8-10 ünlü Türk ve dünya ünlüsü (sadece isimlerini listele)

## Sık Sorulan Sorular

### {burc_data['ad']} burcu hangi burçlarla uyumludur?
(Detaylı cevap, 2-3 cümle)

### {burc_data['ad']} burcunun en güçlü yönü nedir?
(Detaylı cevap, 2-3 cümle)

### {burc_data['ad']} burcu hangi mesleklerde başarılı olur?
(Detaylı cevap, 5-6 meslek örneği)

### {burc_data['ad']} burcunun şans taşı nedir?
(Detaylı cevap, taş özellikleri)

### {burc_data['ad']} burcu nasıl biri ile evlenmeli?
(Detaylı cevap, ideal eş özellikleri)

ÖNEMLİ:
- Tamamen Türkçe yaz
- Profesyonel ama samimi bir dil kullan
- Bilimsel değil, astrolojik bir yaklaşım
- SEO dostu, akıcı ve okunabilir içerik
- Her bölümü ## başlıklarla ayır
- Gerçekçi ve kullanışlı bilgiler ver
- Ünlü isimleri madde işareti ile listele
- SSS bölümünde ### başlıkları kullan

Sadece içeriği yaz, başka açıklama ekleme."""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir astrolog ve içerik yazarısın. Türkçe burç içerikleri yazıyorsun."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.7,
                max_tokens=4000,
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

def create_markdown_file(burc_key, burc_data, content):
    """Markdown dosyası oluştur"""
    # Klasör oluştur
    burc_dir = CONTENT_DIR / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Özellikleri, Kişilik Analizi ve Uyumu"
slug: "{burc_data['slug']}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu özellikleri, kişilik analizi, aşk uyumu, kariyer, sağlık ve finansal durumu hakkında detaylı bilgiler."
keywords: ["{burc_data['ad']} burcu", "{burc_data['slug']}", "{burc_data['ad']} özellikleri", "{burc_data['ad']} kişiliği", "{burc_data['ad']} uyumu"]
element: "{burc_data['element']}"
nitelik: "{burc_data['nitelik']}"
gezegen: "{burc_data['gezegen']}"
tarih: "{burc_data['tarih']}"
sans_gunu: "{burc_data['sans_gunu']}"
sans_sayilari: {burc_data['sans_sayilari']}
sans_renkleri: {burc_data['sans_renkleri']}
uyumlu_burclar: {burc_data['uyumlu_burclar']}
uyumsuz_burclar: {burc_data['uyumsuz_burclar']}
sans_taslari: {burc_data['sans_taslari']}
draft: false
---

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = burc_dir / '_index.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ {burc_data['ad']} burcu sayfası oluşturuldu: {file_path}")

def main():
    """Ana fonksiyon"""
    print("🌟 12 Burç Ana Sayfası İçerik Üretimi Başlıyor...\n")

    # Content dizini oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f"\n{'='*60}")
        print(f"📝 {burc_data['ad']} burcu içeriği üretiliyor...")
        print(f"{'='*60}")

        # Prompt oluştur
        prompt = create_burc_prompt(burc_key, burc_data)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Markdown dosyası oluştur
            create_markdown_file(burc_key, burc_data, content)
            success_count += 1
            print(f"✅ {burc_data['ad']} burcu tamamlandı!")
        else:
            failed_count += 1
            print(f"❌ {burc_data['ad']} burcu üretilemedi!")

        # Rate limiting (30 req/min için 2 saniye bekle)
        if burc_key != list(BURCLAR.keys())[-1]:  # Son burç değilse
            print("⏳ 3 saniye bekleniyor...")
            time.sleep(3)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"📁 İçerikler: {CONTENT_DIR}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
