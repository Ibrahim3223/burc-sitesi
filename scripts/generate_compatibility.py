"""
144 Burç Uyumu Sayfası Üretimi
Her burç çifti için uyum analizi
"""

import os
from datetime import datetime
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import time
from burc_data import BURCLAR
from itertools import combinations_with_replacement

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'burc-uyumu'

def create_compatibility_prompt(burc1_data, burc2_data):
    """Burç uyumu içerik promptu"""
    return f"""Sen profesyonel bir astrologsun. {burc1_data['ad']} ve {burc2_data['ad']} burçları arasındaki uyumu detaylı analiz et.

BURÇ 1: {burc1_data['ad']} - Element: {burc1_data['element']}, Gezegen: {burc1_data['gezegen']}
BURÇ 2: {burc2_data['ad']} - Element: {burc2_data['element']}, Gezegen: {burc2_data['gezegen']}

YAZIYI ŞU FORMATTA YAZ:

## Genel Uyum Değerlendirmesi
3-4 cümle ile bu iki burcun genel uyumunu analiz et. Element ve gezegen uyumuna değin.

## Aşk ve Romantik İlişki Uyumu
**Uyum Puanı:** 8/10 (1-10 arası gerçekçi bir puan)

4-5 cümle ile romantik ilişkideki uyumlarını anlat. Güçlü yönler ve zorluklar neler?

## Evlilik ve Uzun Vadeli İlişki
3-4 cümle ile evlilik ve uzun vadeli ilişkide nasıl olacaklarını anlat.

## Cinsel Uyum
2-3 cümle ile fiziksel ve cinsel uyumları hakkında bilgi ver.

## Arkadaşlık Uyumu
**Uyum Puanı:** 7/10

3 cümle ile arkadaşlık ilişkisindeki uyumları.

## İş ve Kariyer Ortaklığı
**Uyum Puanı:** 6/10

3 cümle ile iş ortaklığında nasıl olacakları.

## Güçlü Yönleri
- İlk güçlü yön (1 cümle açıklama)
- İkinci güçlü yön (1 cümle açıklama)
- Üçüncü güçlü yön (1 cümle açıklama)

## Zorluklar ve Dikkat Edilmesi Gerekenler
- İlk zorluk (1 cümle açıklama)
- İkinci zorluk (1 cümle açıklama)
- Üçüncü zorluk (1 cümle açıklama)

## İlişkiyi Güçlendirmek İçin Öneriler
3 madde halinde pratik önerilerde bulun.

## Ünlü {burc1_data['ad']}-{burc2_data['ad']} Çiftleri
2-3 ünlü çift örneği ver (gerçek veya olası)

ÖNEMLİ:
- Tamamen Türkçe yaz
- Dürüst ve gerçekçi ol (her çift mükemmel değildir)
- Pozitif ama gerçekçi bir dil kullan
- Uyum puanlarını element ve gezegen uyumuna göre belirle
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Madde işaretlerini - ile yap"""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir astrolog ve burç uyumu uzmanısın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.7,
                max_tokens=3000,
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

def create_compatibility_markdown(burc1_key, burc1_data, burc2_key, burc2_data, content):
    """Burç uyumu markdown dosyası oluştur"""
    # Klasör oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    # Slug oluştur (alfabetik sıra)
    slug_parts = sorted([burc1_key, burc2_key])
    slug = f"{slug_parts[0]}-{slug_parts[1]}"

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc1_data['ad']} ve {burc2_data['ad']} Burcu Uyumu - Aşk, Evlilik, Arkadaşlık"
slug: "{slug}"
date: {date_str}
lastmod: {date_str}
description: "{burc1_data['ad']} ve {burc2_data['ad']} burçları arasındaki aşk, evlilik, arkadaşlık ve iş uyumu. Detaylı uyum analizi ve öneriler."
keywords: ["{burc1_data['ad']} {burc2_data['ad']} uyumu", "{burc1_data['ad']} {burc2_data['ad']} aşk uyumu", "{burc1_key} {burc2_key} uyum"]
burc1: "{burc1_data['ad']}"
burc2: "{burc2_data['ad']}"
type: "uyum"
draft: false
---

# {burc1_data['ad']} ve {burc2_data['ad']} Burcu Uyumu

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = CONTENT_DIR / f'{slug}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ {burc1_data['ad']}-{burc2_data['ad']} uyumu oluşturuldu")

def create_main_compatibility_page():
    """Ana burç uyumu sayfası oluştur"""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    content = f"""---
title: "Burç Uyumu Hesaplama - 12 Burç Uyum Analizi"
date: {date_str}
lastmod: {date_str}
description: "Burç uyumu hesaplama aracı ile 12 burç arasındaki aşk, evlilik, arkadaşlık ve iş uyumunu öğrenin. Detaylı uyum analizleri."
keywords: ["burç uyumu", "burç uyumu hesaplama", "aşk uyumu", "burç eşleştirme", "burç uyum testi"]
layout: "list"
---

# Burç Uyumu Nedir?

Burç uyumu, iki kişinin astrolojik özelliklerinin birbirleriyle ne kadar uyumlu olduğunu gösterir. Element uyumu, gezegen ilişkileri ve burç nitelikleri bir araya gelerek iki kişi arasındaki potansiyel uyumu belirler.

## Burç Uyumunu Etkileyen Faktörler

### Element Uyumu
- **Ateş Burçları:** Koç, Aslan, Yay
- **Toprak Burçları:** Boğa, Başak, Oğlak
- **Hava Burçları:** İkizler, Terazi, Kova
- **Su Burçları:** Yengeç, Akrep, Balık

Aynı elementten burçlar genellikle uyumludur. Ateş-Hava ve Toprak-Su kombinasyonları da iyi çalışır.

## Burç Uyumu Hesaplama

Aşağıdaki burç kombinasyonları için detaylı uyum analizlerimizi inceleyebilirsiniz:
"""

    file_path = CONTENT_DIR / '_index.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Ana burç uyumu sayfası oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🌟 144 Burç Uyumu Sayfası Üretimi Başlıyor...\n")

    # Ana sayfa oluştur
    create_main_compatibility_page()

    success_count = 0
    failed_count = 0
    total_combinations = 0

    # Tüm kombinasyonları oluştur (kendisiyle dahil)
    burc_keys = list(BURCLAR.keys())

    for i, burc1_key in enumerate(burc_keys):
        for j, burc2_key in enumerate(burc_keys):
            if j < i:  # Tekrarları atla
                continue

            total_combinations += 1
            burc1_data = BURCLAR[burc1_key]
            burc2_data = BURCLAR[burc2_key]

            print(f"\n[{total_combinations}/78] 📝 {burc1_data['ad']}-{burc2_data['ad']} uyumu üretiliyor...")

            # Prompt oluştur
            prompt = create_compatibility_prompt(burc1_data, burc2_data)

            # İçerik üret
            content = generate_content_with_groq(prompt)

            if content:
                # Markdown dosyası oluştur
                create_compatibility_markdown(burc1_key, burc1_data, burc2_key, burc2_data, content)
                success_count += 1
            else:
                failed_count += 1
                print(f"❌ {burc1_data['ad']}-{burc2_data['ad']} üretilemedi!")

            # Rate limiting (önemli!)
            if total_combinations < 78:
                print("⏳ 3 saniye bekleniyor...")
                time.sleep(3)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"📄 Toplam: {total_combinations}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
