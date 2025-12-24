# -*- coding: utf-8 -*-
"""
Aylık Burç Yorumları - Archive Sistemi
Her ay YENİ sayfa oluşturur: /koc-burcu/aylik/2025-12/
"""

import os
from datetime import datetime
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import time
from burc_data import BURCLAR

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'burc'

def create_monthly_prompt(burc_data, ay_tam, aylar):
    """Aylık yorum promptu"""
    now = datetime.now()
    return f"""Sen profesyonel bir Türk astrologsun. {burc_data['ad']} burcu için {ay_tam} aylık burç yorumu yaz.

## Ayın Genel Değerlendirmesi
6-7 cümle ile ayın genel enerjisini detaylı anlat. Gezegen hareketlerinden, retrolardan ve kozmik etkilerden bahset.

## Aşk ve İlişkiler
6-7 cümle ile aşk hayatı için öngörüler yaz. Ayın ilk yarısı ve ikinci yarısı için ayrı değerlendirme yap. Bekarlar ve ilişkide olanlar için tavsiyeler ver.

## Kariyer ve İş Hayatı
6-7 cümle ile iş hayatında beklenen gelişmeleri anlat. Projeler, iş görüşmeleri ve kariyer fırsatları hakkında bilgi ver.

## Finans ve Para
5-6 cümle ile finansal konularda öngörüler yaz. Yatırımlar, harcamalar ve para yönetimi hakkında tavsiyeler ver.

## Sağlık ve Enerji
4-5 cümle ile fiziksel ve mental sağlık için ay boyunca dikkat edilmesi gerekenleri anlat.

## Ayın Önemli Tarihleri
### 5 {aylar[now.month]} - Yeni Ay
3-4 cümle ile yeni ayın etkileri ve yapılması gerekenler
### 15 {aylar[now.month]} - Dolunay
3-4 cümle ile dolunayın etkileri ve dikkat edilmesi gerekenler
### 23 {aylar[now.month]} - Özel Gün
3-4 cümle ile bu günün özel enerjisi

## Ayın Tavsiyesi
4-5 cümle ile ayın en önemli tavsiyesini ver. Motivasyon verici ve ay boyunca uygulanabilir olsun.

KRİTİK KURALLAR:
- SADECE TÜRKÇE yaz, kesinlikle başka dilde kelime kullanma
- Arapça, İngilizce veya başka hiçbir dilde kelime KULLANMA
- Tüm kelimeler %100 Türkçe olmalı
- Pozitif ama gerçekçi bir dil kullan
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## ile başlat"""

def generate_with_groq(prompt, max_tokens=3500, temperature=0.7):
    """Groq API ile içerik üret"""
    try:
        result = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen profesyonel bir Türk astrolog ve içerik yazarısın. SADECE Türkçe burç içerikleri yazıyorsun. Kesinlikle başka dilde kelime kullanma."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9
        )
        return result.choices[0].message.content
    except Exception as e:
        print(f"[HATA] {e}")
        return None

def create_archive_index(burc_key, burc_data):
    """Aylık arşiv index sayfası oluştur"""
    burc_aylik_dir = CONTENT_DIR / burc_key / 'aylik'
    burc_aylik_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    index_content = f"""---
title: "{burc_data['ad']} Burcu Aylık Yorumlar Arşivi"
date: {date_str}
description: "{burc_data['ad']} burcu aylık yorum arşivi. Tüm aylık burç yorumlarına buradan ulaşabilirsiniz."
keywords: ["{burc_data['ad']} aylık arşiv", "{burc_data['ad']} aylık yorumlar"]
layout: "list"
type: "aylik-arsiv"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Aylık Yorumlar Arşivi

{burc_data['ad']} burcu için geçmiş aylık burç yorumlarına aşağıdan ulaşabilirsiniz. Her ay yeni bir yorum eklenmektedir.
"""

    index_path = burc_aylik_dir / '_index.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

def create_monthly_archive(burc_key, burc_data):
    """Aylık yorum arşiv dosyası oluştur"""
    now = datetime.now()
    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    ay_tam = f"{aylar[now.month]} {now.year}"

    # Ay slug: 2025-12
    month_slug = now.strftime("%Y-%m")

    prompt = create_monthly_prompt(burc_data, ay_tam, aylar)
    content = generate_with_groq(prompt, max_tokens=2500, temperature=0.8)

    if not content:
        return False

    # Arşiv klasörü: /burc/koc/aylik/
    burc_aylik_dir = CONTENT_DIR / burc_key / 'aylik'
    burc_aylik_dir.mkdir(parents=True, exist_ok=True)

    # Arşiv index oluştur (ilk çalıştırmada)
    if not (burc_aylik_dir / '_index.md').exists():
        create_archive_index(burc_key, burc_data)

    now_dt = datetime.now().astimezone()
    date_str = now_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Aylık Yorum - {ay_tam}"
slug: "{month_slug}"
date: {date_str}
description: "{burc_data['ad']} burcu için {ay_tam} aylık burç yorumu."
keywords: ["{burc_data['ad']} aylık", "aylık {burc_data['ad']}"]
type: "aylik"
burc: "{burc_data['ad']}"
ay_tam: "{ay_tam}"
month_slug: "{month_slug}"
draft: false
---

# {burc_data['ad']} Burcu Aylık Yorum - {ay_tam}

"""

    # ARŞIV: Ay numaralı dosya oluştur
    archive_file_path = burc_aylik_dir / f'{month_slug}.md'

    with open(archive_file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"[OK] {burc_data['ad']} aylik arsiv olusturuldu: {month_slug}")

    # LATEST: En son yorumu göstermek için aylik.md de oluştur
    latest_file_path = CONTENT_DIR / burc_key / 'aylik.md'
    latest_frontmatter = f"""---
title: "{burc_data['ad']} Burcu Aylık Yorum - {ay_tam}"
date: {date_str}
description: "{burc_data['ad']} burcu için aylık burç yorumu."
keywords: ["{burc_data['ad']} aylık", "aylık {burc_data['ad']}"]
type: "aylik"
burc: "{burc_data['ad']}"
ay_tam: "{ay_tam}"
aliases: ["/{burc_data['slug']}/aylik/"]
draft: false
---

# {burc_data['ad']} Burcu Aylık Yorum - {ay_tam}

> **📅 Güncel Yorum**: Bu sayfa her ay güncellenir. Geçmiş yorumlar için [arşive göz atın](/{burc_data['slug']}/aylik/).

"""

    with open(latest_file_path, 'w', encoding='utf-8') as f:
        f.write(latest_frontmatter + content)

    print(f"[OK] {burc_data['ad']} en son aylik yorum guncellendi")

    return True

def main():
    """Ana fonksiyon - aylık yorumlar"""
    now = datetime.now()
    month_slug = now.strftime("%Y-%m")
    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
    ay_tam = f"{aylar[now.month]} {now.year}"

    print("="*60)
    print(f">>> AYLIK ARŞİV ÜRETİMİ - {month_slug} ({ay_tam})")
    print("="*60)

    aylik_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} aylık...")
        if create_monthly_archive(burc_key, burc_data):
            aylik_ok += 1
        time.sleep(2)

    print(f"\n[OK] {aylik_ok}/12 aylık arşiv oluşturuldu")
    print("="*60)

if __name__ == '__main__':
    main()
