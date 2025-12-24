# -*- coding: utf-8 -*-
"""
Haftalık Burç Yorumları - Archive Sistemi
Her hafta YENİ sayfa oluşturur: /koc-burcu/haftalik/2025-W51/
"""

import os
from datetime import datetime, timedelta
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

def create_weekly_prompt(burc_data, tarih_araligi):
    """Haftalık yorum promptu"""
    return f"""Sen profesyonel bir Türk astrologsun. {burc_data['ad']} burcu için {tarih_araligi} haftalık burç yorumu yaz.

## Haftanın Genel Enerjisi
5-6 cümle ile haftanın genel enerjisini detaylı anlat. Gezegen hareketlerinden ve kozmik etkilerden bahset.

## Aşk ve İlişkiler
5-6 cümle ile aşk hayatı için öngörüler yaz. Bekarlar için ve ilişkide olanlar için ayrı ayrı detaylı tavsiyeler ver.

## Kariyer ve Finans
5-6 cümle ile iş hayatı ve finansal konularda tavsiyeler ver. Hafta içi dikkat edilmesi gerekenlerden bahset.

## Sağlık ve Wellness
4-5 cümle ile fiziksel ve mental sağlık için öneriler ver. Beslenme, egzersiz ve stres yönetimi hakkında tavsiyeler ekle.

## Haftanın Önemli Günleri
### Pazartesi
2-3 cümle ile günün enerjisi ve dikkat edilmesi gerekenler
### Çarşamba
2-3 cümle ile günün enerjisi ve fırsatlar
### Cuma
2-3 cümle ile hafta sonu öncesi değerlendirme

## Haftanın Tavsiyesi
3-4 cümle ile haftanın en önemli tavsiyesini ver. Motivasyon verici ve uygulanabilir olsun.

KRİTİK KURALLAR:
- SADECE TÜRKÇE yaz, kesinlikle başka dilde kelime kullanma
- Arapça, İngilizce veya başka hiçbir dilde kelime KULLANMA
- Tüm kelimeler %100 Türkçe olmalı
- Pozitif ama gerçekçi bir dil kullan
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## ile başlat"""

def generate_with_groq(prompt, max_tokens=3000, temperature=0.7):
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
    """Haftalık arşiv index sayfası oluştur"""
    burc_haftalik_dir = CONTENT_DIR / burc_key / 'haftalik'
    burc_haftalik_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    index_content = f"""---
title: "{burc_data['ad']} Burcu Haftalık Yorumlar Arşivi"
date: {date_str}
description: "{burc_data['ad']} burcu haftalık yorum arşivi. Tüm haftalık burç yorumlarına buradan ulaşabilirsiniz."
keywords: ["{burc_data['ad']} haftalık arşiv", "{burc_data['ad']} haftalık yorumlar"]
layout: "list"
type: "haftalik-arsiv"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Haftalık Yorumlar Arşivi

{burc_data['ad']} burcu için geçmiş haftalık burç yorumlarına aşağıdan ulaşabilirsiniz. Her hafta yeni bir yorum eklenmektedir.
"""

    index_path = burc_haftalik_dir / '_index.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

def create_weekly_archive(burc_key, burc_data):
    """Haftalık yorum arşiv dosyası oluştur"""
    now = datetime.now()
    days_to_monday = now.weekday()
    monday = now - timedelta(days=days_to_monday)
    sunday = monday + timedelta(days=6)

    aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
             'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

    tarih_araligi = f"{monday.day} {aylar[monday.month]} - {sunday.day} {aylar[sunday.month]} {sunday.year}"

    # ISO hafta numarası: 2025-W51
    year, week, _ = monday.isocalendar()
    week_slug = f"{year}-W{week:02d}"

    prompt = create_weekly_prompt(burc_data, tarih_araligi)
    content = generate_with_groq(prompt, max_tokens=2000, temperature=0.8)

    if not content:
        return False

    # Arşiv klasörü: /burc/koc/haftalik/
    burc_haftalik_dir = CONTENT_DIR / burc_key / 'haftalik'
    burc_haftalik_dir.mkdir(parents=True, exist_ok=True)

    # Arşiv index oluştur (ilk çalıştırmada)
    if not (burc_haftalik_dir / '_index.md').exists():
        create_archive_index(burc_key, burc_data)

    now_dt = datetime.now().astimezone()
    date_str = now_dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}"
slug: "{week_slug}"
date: {date_str}
description: "{burc_data['ad']} burcu için {tarih_araligi} haftalık burç yorumu."
keywords: ["{burc_data['ad']} haftalık", "haftalık {burc_data['ad']}"]
type: "haftalik"
burc: "{burc_data['ad']}"
tarih_araligi: "{tarih_araligi}"
week_slug: "{week_slug}"
draft: false
---

# {burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}

"""

    # ARŞIV: Hafta numaralı dosya oluştur
    archive_file_path = burc_haftalik_dir / f'{week_slug}.md'

    with open(archive_file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"[OK] {burc_data['ad']} haftalik arsiv olusturuldu: {week_slug}")

    # LATEST: En son yorumu göstermek için haftalik.md de oluştur
    latest_file_path = CONTENT_DIR / burc_key / 'haftalik.md'
    latest_frontmatter = f"""---
title: "{burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}"
date: {date_str}
description: "{burc_data['ad']} burcu için haftalık burç yorumu."
keywords: ["{burc_data['ad']} haftalık", "haftalık {burc_data['ad']}"]
type: "haftalik"
burc: "{burc_data['ad']}"
tarih_araligi: "{tarih_araligi}"
aliases: ["/{burc_data['slug']}/haftalik/"]
draft: false
---

# {burc_data['ad']} Burcu Haftalık Yorum - {tarih_araligi}

> **📅 Güncel Yorum**: Bu sayfa her hafta güncellenir. Geçmiş yorumlar için [arşive göz atın](/{burc_data['slug']}/haftalik/).

"""

    with open(latest_file_path, 'w', encoding='utf-8') as f:
        f.write(latest_frontmatter + content)

    print(f"[OK] {burc_data['ad']} en son haftalik yorum guncellendi")

    return True

def main():
    """Ana fonksiyon - haftalık yorumlar"""
    now = datetime.now()
    year, week, _ = now.isocalendar()
    week_slug = f"{year}-W{week:02d}"

    print("="*60)
    print(f">>> HAFTALİK ARŞİV ÜRETİMİ - {week_slug}")
    print("="*60)

    haftalik_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} haftalık...")
        if create_weekly_archive(burc_key, burc_data):
            haftalik_ok += 1
        time.sleep(2)

    print(f"\n[OK] {haftalik_ok}/12 haftalık arşiv oluşturuldu")
    print("="*60)

if __name__ == '__main__':
    main()
