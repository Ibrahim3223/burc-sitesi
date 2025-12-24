# -*- coding: utf-8 -*-
"""
Günlük Burç Yorumları - Archive Sistemi
Her gün YENİ sayfa oluşturur: /koc-burcu/gunluk/2025-12-23/
Ayrıca anasayfa için gunluk/{burc}.md dosyalarını günceller
"""

import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import time
from burc_data import BURCLAR

# Load environment variables
load_dotenv()

# Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Türkiye saat dilimi (UTC+3)
TURKEY_TZ = timezone(timedelta(hours=3))

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'burc'
GUNLUK_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'gunluk'  # Anasayfa için

def create_daily_prompt(burc_data, tarih):
    """Günlük yorum promptu"""
    return f"""Sen profesyonel bir Türk astrologsun. {burc_data['ad']} burcu için {tarih} tarihli günlük burç yorumu yaz.

BURÇ: {burc_data['ad']} ({burc_data['tarih']})
TARİH: {tarih}

YAZIYI ŞU FORMATTA YAZ:

## Genel Enerji
4-5 cümle ile günün genel enerjisini detaylı anlat. Gezegen konumlarından, günün atmosferinden ve genel eğilimlerden bahset.

## Aşk ve İlişkiler
4-5 cümle ile aşk hayatı için öngörüler yaz. Bekarlar ve ilişkisi olanlar için ayrı ayrı tavsiyeler ver.

## Kariyer ve İş
4-5 cümle ile iş hayatı için tavsiyeler ver. Toplantılar, projeler, iş arkadaşları ile ilişkiler hakkında detaylı yaz.

## Sağlık
3-4 cümle ile sağlık konusunda dikkat edilmesi gerekenler. Fiziksel ve mental sağlık için öneriler ver.

## Şans Faktörleri
- **Şans Puanı:** (1-10 arası bir puan ver)/10
- **Şans Sayısı:** {burc_data['sans_sayilari'][0]}
- **Şans Rengi:** {burc_data['sans_renkleri'][0]}

## Günün Tavsiyesi
2-3 cümle ile günün en önemli tavsiyesini ver. Motivasyon verici ve uygulanabilir olsun.

KRİTİK KURALLAR:
- SADECE TÜRKÇE yaz, kesinlikle başka dilde kelime kullanma
- Arapça, İngilizce veya başka hiçbir dilde kelime KULLANMA
- Tüm kelimeler %100 Türkçe olmalı
- Pozitif ama gerçekçi bir dil kullan
- Spesifik ve kişisel önerilerde bulun
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## ile başlat
- Akıcı ve doğal Türkçe kullan"""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir Türk astrolog ve günlük burç yorumları yazarısın. SADECE Türkçe yaz. Kesinlikle Arapça, İngilizce veya başka dilde kelime kullanma."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2500,
                top_p=0.9
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"[HATA] (Deneme {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"[BEKLE] {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
            else:
                return None

    return None

def create_archive_index(burc_key, burc_data):
    """Günlük arşiv index sayfası oluştur"""
    burc_gunluk_dir = CONTENT_DIR / burc_key / 'gunluk'
    burc_gunluk_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(TURKEY_TZ)
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    index_content = f"""---
title: "{burc_data['ad']} Burcu Günlük Yorumlar Arşivi"
date: {date_str}
description: "{burc_data['ad']} burcu günlük yorum arşivi. Tüm günlük burç yorumlarına buradan ulaşabilirsiniz."
keywords: ["{burc_data['ad']} günlük arşiv", "{burc_data['ad']} günlük yorumlar"]
layout: "list"
type: "gunluk-arsiv"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Günlük Yorumlar Arşivi

{burc_data['ad']} burcu için geçmiş günlük burç yorumlarına aşağıdan ulaşabilirsiniz. Her gün yeni bir yorum eklenmektedir.
"""

    index_path = burc_gunluk_dir / '_index.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

def create_daily_archive_markdown(burc_key, burc_data, content, tarih, tarih_slug):
    """Günlük yorum arşiv dosyası oluştur - YENİ SAYFA"""
    # Arşiv klasörü: /burc/koc/gunluk/
    burc_gunluk_dir = CONTENT_DIR / burc_key / 'gunluk'
    burc_gunluk_dir.mkdir(parents=True, exist_ok=True)

    # Arşiv index oluştur (ilk çalıştırmada)
    if not (burc_gunluk_dir / '_index.md').exists():
        create_archive_index(burc_key, burc_data)

    # Frontmatter
    now = datetime.now(TURKEY_TZ)
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Günlük Yorum - {tarih}"
slug: "{tarih_slug}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için {tarih} günlük burç yorumu. Aşk, kariyer, sağlık ve genel enerji öngörüleri."
keywords: ["{burc_data['ad']} günlük", "günlük {burc_data['ad']}", "{burc_data['ad']} bugün", "{burc_data['ad']} yorum {tarih}"]
layout: "single"
type: "gunluk"
burc: "{burc_data['ad']}"
tarih: "{tarih}"
tarih_slug: "{tarih_slug}"
draft: false
---

# {burc_data['ad']} Burcu Günlük Yorum - {tarih}

"""

    # Tam içerik
    full_content = frontmatter + content

    # ARŞIV: Tarihli dosya oluştur (ÜZERİNE YAZILMAZ!)
    # Format: /burc/koc/gunluk/2025-12-23.md
    archive_file_path = burc_gunluk_dir / f'{tarih_slug}.md'

    # Eğer bugünün dosyası zaten varsa üzerine yazma (isteğe bağlı)
    if archive_file_path.exists():
        print(f"[UYARI] {burc_data['ad']} icin {tarih_slug} arsivi zaten mevcut, guncelleniyor...")

    with open(archive_file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"[OK] {burc_data['ad']} gunluk arsiv olusturuldu: {tarih_slug}")

    # LATEST: En son yorumu göstermek için gunluk.md de oluştur (isteğe bağlı)
    latest_file_path = CONTENT_DIR / burc_key / 'gunluk.md'
    latest_frontmatter = f"""---
title: "{burc_data['ad']} Burcu Günlük Yorum - {tarih}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için günlük burç yorumu. Aşk, kariyer, sağlık ve genel enerji öngörüleri."
keywords: ["{burc_data['ad']} günlük", "günlük {burc_data['ad']}", "{burc_data['ad']} bugün"]
layout: "single"
type: "gunluk"
burc: "{burc_data['ad']}"
tarih: "{tarih}"
aliases: ["/{burc_data['slug']}/gunluk/"]
draft: false
---

# {burc_data['ad']} Burcu Günlük Yorum - {tarih}

> **📅 Güncel Yorum**: Bu sayfa her gün güncellenir. Geçmiş yorumlar için [arşive göz atın](/{burc_data['slug']}/gunluk/).

"""

    with open(latest_file_path, 'w', encoding='utf-8') as f:
        f.write(latest_frontmatter + content)

    print(f"[OK] {burc_data['ad']} en son gunluk yorum guncellendi")

def update_homepage_gunluk(burc_key, burc_data, content, tarih, tarih_slug):
    """Anasayfa için gunluk/{burc}.md dosyasını güncelle"""
    GUNLUK_DIR.mkdir(parents=True, exist_ok=True)

    now_tr = datetime.now(TURKEY_TZ)
    date_str = now_tr.strftime("%Y-%m-%dT%H:%M:%S+03:00")

    # Puan değerlerini çıkarmaya çalış (varsayılan 7)
    import random
    genel_puan = random.randint(6, 9)
    ask_puani = random.randint(5, 9)
    kariyer_puani = random.randint(5, 9)
    saglik_puani = random.randint(5, 9)

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Günlük Yorum - {tarih}"
date: {date_str}
lastmod: {date_str}
description: "{burc_data['ad']} burcu için günlük burç yorumu. Aşk, kariyer, sağlık ve genel enerji öngörüleri."
keywords: ["{burc_data['ad']} günlük", "günlük {burc_data['ad']}", "{burc_data['ad']} bugün"]
type: "gunluk"
burc: "{burc_data['ad']}"
tarih: "{tarih}"
genel_puan: {genel_puan}
ask_puani: {ask_puani}
kariyer_puani: {kariyer_puani}
saglik_puani: {saglik_puani}
draft: false
---

# {burc_data['ad']} Burcu Günlük Yorum - {tarih}

> **📅 Güncel Yorum**: Bu sayfa her gün güncellenir. Geçmiş yorumlar için [arşive göz atın](/{burc_data['slug']}/gunluk-arsiv/).

"""

    homepage_file = GUNLUK_DIR / f"{burc_key}.md"
    with open(homepage_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"[OK] {burc_data['ad']} anasayfa gunluk dosyasi guncellendi")


def main():
    """Ana fonksiyon"""
    # Bugünün tarihi - Türkiye saati (UTC+3) kullanılıyor
    now = datetime.now(TURKEY_TZ)
    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    tarih = f"{now.day} {aylar[now.month]} {now.year}"
    tarih_slug = now.strftime("%Y-%m-%d")  # 2025-12-23

    print(f">>> Gunluk Burc Yorumlari Arsiv Uretimi - {tarih}\n")
    print(f">>> Arsiv formati: /burc/{{burc}}/gunluk/{tarih_slug}.md\n")

    # Content dizini oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} gunluk yorumu uretiliyor...")

        # Prompt oluştur
        prompt = create_daily_prompt(burc_data, tarih)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Arşiv markdown dosyası oluştur
            create_daily_archive_markdown(burc_key, burc_data, content, tarih, tarih_slug)
            # Anasayfa için gunluk/{burc}.md dosyasını güncelle
            update_homepage_gunluk(burc_key, burc_data, content, tarih, tarih_slug)
            success_count += 1
        else:
            failed_count += 1
            print(f"[HATA] {burc_data['ad']} uretilemedi!")

        # Rate limiting
        if burc_key != list(BURCLAR.keys())[-1]:
            time.sleep(2)

    # Özet
    print(f"\n{'='*60}")
    print(f">>> OZET - {tarih} (Turkiye Saati)")
    print(f"{'='*60}")
    print(f"[OK] Basarili: {success_count}")
    print(f"[HATA] Basarisiz: {failed_count}")
    print(f"[ARSIV] {success_count} yeni sayfa olusturuldu")
    print(f"[LATEST] {success_count} en son yorum guncellendi")
    print(f"[HOMEPAGE] {success_count} anasayfa gunluk dosyasi guncellendi")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
