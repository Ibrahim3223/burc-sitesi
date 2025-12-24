# -*- coding: utf-8 -*-
"""
TUM SAYFALARI OLUSTUR: Burc + Yukselen + Uyum + Haftalik/Aylik
"""

import os
import sys
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
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content'

def generate_with_groq(prompt, max_tokens=4000, temperature=0.7):
    """Groq API ile icerik uret"""
    try:
        result = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen profesyonel bir astrolog ve icerik yazarissin. Turkce burc icerikleri yaziyorsun."},
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

def create_weekly(burc_key, burc_data):
    """Haftalik yorum olustur"""
    now = datetime.now()
    days_to_monday = now.weekday()
    monday = now - timedelta(days=days_to_monday)
    sunday = monday + timedelta(days=6)

    aylar = ['', 'Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran',
             'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik']

    tarih_araligi = f"{monday.day} {aylar[monday.month]} - {sunday.day} {aylar[sunday.month]} {sunday.year}"

    prompt = f"""Sen astrologsun. {burc_data['ad']} burcu icin {tarih_araligi} haftalik yorum yaz.

## Haftanin Genel Enerjisi
3-4 cumle
## Ask ve Iliskiler
3-4 cumle (bekar ve iliski olanlara ayri degin)
## Kariyer ve Finans
3-4 cumle
## Saglik ve Wellness
2-3 cumle
## Haftanin Onemli Gunleri
### Pazartesi
1-2 cumle
### Carsamba
1-2 cumle
### Cuma
1-2 cumle
## Haftanin Tavsiyesi
2 cumle

Turkce yaz, sadece icerigi yaz."""

    content = generate_with_groq(prompt, max_tokens=2000, temperature=0.8)
    if not content:
        return False

    burc_dir = CONTENT_DIR / 'burc' / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Haftalik Yorum - {tarih_araligi}"
date: {date_str}
description: "{burc_data['ad']} burcu icin {tarih_araligi} haftalik burc yorumu."
keywords: ["{burc_data['ad']} haftalik", "haftalik {burc_data['ad']}"]
type: "haftalik"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Haftalik Yorum - {tarih_araligi}

"""

    file_path = burc_dir / 'haftalik.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True

def create_monthly(burc_key, burc_data):
    """Aylik yorum olustur"""
    now = datetime.now()
    aylar = ['', 'Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran',
             'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik']
    ay_tam = f"{aylar[now.month]} {now.year}"

    prompt = f"""Sen astrologsun. {burc_data['ad']} burcu icin {ay_tam} aylik yorum yaz.

## Ayin Genel Degerlendirmesi
4-5 cumle, planetsel hareketler
## Ask ve Iliskiler
4-5 cumle (ilk yari ve ikinci yari ayir)
## Kariyer ve Is Hayati
4-5 cumle
## Finans ve Para
3-4 cumle
## Saglik ve Enerji
2-3 cumle
## Ayin Onemli Tarihleri
### 5 {aylar[now.month]} - Yeni Ay
2 cumle
### 15 {aylar[now.month]} - Dolunay
2 cumle
### 23 {aylar[now.month]} - Ozel Gun
2 cumle
## Ayin Tavsiyesi
2-3 cumle

Turkce yaz, sadece icerigi yaz."""

    content = generate_with_groq(prompt, max_tokens=2500, temperature=0.8)
    if not content:
        return False

    burc_dir = CONTENT_DIR / 'burc' / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Aylik Yorum - {ay_tam}"
date: {date_str}
description: "{burc_data['ad']} burcu icin {ay_tam} aylik burc yorumu."
keywords: ["{burc_data['ad']} aylik", "aylik {burc_data['ad']}"]
type: "aylik"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Aylik Yorum - {ay_tam}

"""

    file_path = burc_dir / 'aylik.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True

def create_yukselen(burc_key, burc_data):
    """Yukselen burc sayfasi olustur"""
    prompt = f"""Sen astrologsun. Yukselen {burc_data['ad']} ozellikleri hakkinda detayli rehber yaz.

## Yukselen Burc Nedir?
2-3 cumle genel aciklama
## Yukselen {burc_data['ad']} Genel Ozellikleri
4-5 cumle kisilik ozellikleri
## Fiziksel Gorunum ve Ilk Izlenim
3-4 cumle
## Kisilik ve Davranis Sekli
4-5 cumle sosyal hayat, dis dunyaya gorunum
## Askta Yukselen {burc_data['ad']}
3-4 cumle iliskilerdeki tavir
## Kariyerde Yukselen {burc_data['ad']}
3-4 cumle is hayati yaklasimi
## Gunes Burcu ile Farki
3 cumle gunes burcu vs yukselen burc
## Yukselen {burc_data['ad']} ile Uyumlu Yukselenler
2-3 cumle uyumlu yukselenler
## Yukselen Burcunuzu Nasil Ogrenirsiniz?
2-3 cumle hesaplama bilgisi

Turkce yaz, sadece icerigi yaz."""

    content = generate_with_groq(prompt, max_tokens=2500, temperature=0.7)
    if not content:
        return False

    yukselen_dir = CONTENT_DIR / 'yukselen-burc'
    yukselen_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    slug = f"yukselen-{burc_key}"

    frontmatter = f"""---
title: "Yukselen {burc_data['ad']} Ozellikleri - Kisilik ve Davranis"
slug: "{slug}"
date: {date_str}
description: "Yukselen {burc_data['ad']} olanların kisilik ozellikleri, fiziksel gorunum ve iliski yaklasimlari."
keywords: ["yukselen {burc_data['ad']}", "yukselen {burc_key}"]
element: "{burc_data['element']}"
gezegen: "{burc_data['gezegen']}"
type: "yukselen"
draft: false
---

# Yukselen {burc_data['ad']} Ozellikleri

"""

    file_path = yukselen_dir / f'{slug}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True

def create_compatibility(burc1_key, burc1_data, burc2_key, burc2_data):
    """Burc uyumu sayfasi olustur"""
    prompt = f"""Sen astrologsun. {burc1_data['ad']} ve {burc2_data['ad']} burcları arasindaki uyumu analiz et.

## Genel Uyum Degerlendirmesi
3-4 cumle element ve gezegen uyumu
## Ask ve Romantik Iliski Uyumu
**Uyum Puani:** 7/10
4-5 cumle romantik iliskide nasil olurlar
## Evlilik ve Uzun Vadeli Iliski
3-4 cumle evlilik potansiyeli
## Cinsel Uyum
2-3 cumle fiziksel uyum
## Arkadaslik Uyumu
**Uyum Puani:** 6/10
3 cumle arkadaslik iliskisi
## Is ve Kariyer Ortakligi
**Uyum Puani:** 5/10
3 cumle is ortakligi
## Guclu Yonleri
- Ilk guclu yon (1 cumle)
- Ikinci guclu yon (1 cumle)
- Ucuncu guclu yon (1 cumle)
## Zorluklar
- Ilk zorluk (1 cumle)
- Ikinci zorluk (1 cumle)
- Ucuncu zorluk (1 cumle)
## Iliskiyi Guclendirmek Icin Oneriler
3 madde pratik oneriler
## Unlu {burc1_data['ad']}-{burc2_data['ad']} Ciftleri
2-3 unlu cift ornegi

Turkce yaz, gerçekçi ol, sadece icerigi yaz."""

    content = generate_with_groq(prompt, max_tokens=3000, temperature=0.7)
    if not content:
        return False

    uyum_dir = CONTENT_DIR / 'burc-uyumu'
    uyum_dir.mkdir(parents=True, exist_ok=True)

    slug_parts = sorted([burc1_key, burc2_key])
    slug = f"{slug_parts[0]}-{slug_parts[1]}"

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc1_data['ad']} ve {burc2_data['ad']} Burcu Uyumu - Ask, Evlilik, Arkadaslik"
slug: "{slug}"
date: {date_str}
description: "{burc1_data['ad']} ve {burc2_data['ad']} burclari arasindaki uyum analizi."
keywords: ["{burc1_data['ad']} {burc2_data['ad']} uyumu", "{burc1_key} {burc2_key}"]
burc1: "{burc1_data['ad']}"
burc2: "{burc2_data['ad']}"
type: "uyum"
draft: false
---

# {burc1_data['ad']} ve {burc2_data['ad']} Burcu Uyumu

"""

    file_path = uyum_dir / f'{slug}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True

def main():
    """Ana fonksiyon - tum sayfalari olustur"""
    print("="*60)
    print(">>> TUM SAYFALARI OLUSTUR")
    print("="*60)

    # 1. Haftalik Yorumlar
    print("\n[1/4] 12 Haftalik Yorum Uretiliyor...")
    haftalik_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} haftalik...")
        if create_weekly(burc_key, burc_data):
            haftalik_ok += 1
        time.sleep(2)
    print(f"[OK] {haftalik_ok}/12 haftalik yorum olusturuldu")

    # 2. Aylik Yorumlar
    print("\n[2/4] 12 Aylik Yorum Uretiliyor...")
    aylik_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} aylik...")
        if create_monthly(burc_key, burc_data):
            aylik_ok += 1
        time.sleep(2)
    print(f"[OK] {aylik_ok}/12 aylik yorum olusturuldu")

    # 3. Yukselen Burc
    print("\n[3/4] 12 Yukselen Burc Sayfasi Uretiliyor...")
    yukselen_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> Yukselen {burc_data['ad']}...")
        if create_yukselen(burc_key, burc_data):
            yukselen_ok += 1
        time.sleep(3)
    print(f"[OK] {yukselen_ok}/12 yukselen burc olusturuldu")

    # 4. Burc Uyumu (78 kombinasyon)
    print("\n[4/4] 78 Burc Uyumu Sayfasi Uretiliyor...")
    uyum_ok = 0
    total = 0
    burc_keys = list(BURCLAR.keys())

    for i, burc1_key in enumerate(burc_keys):
        for j, burc2_key in enumerate(burc_keys):
            if j < i:
                continue

            total += 1
            burc1_data = BURCLAR[burc1_key]
            burc2_data = BURCLAR[burc2_key]

            print(f"[{total}/78] >>> {burc1_data['ad']}-{burc2_data['ad']}...")
            if create_compatibility(burc1_key, burc1_data, burc2_key, burc2_data):
                uyum_ok += 1
            time.sleep(3)

    print(f"[OK] {uyum_ok}/78 burc uyumu olusturuldu")

    # Ozet
    print("\n" + "="*60)
    print(">>> OZET")
    print("="*60)
    print(f"[OK] Haftalik: {haftalik_ok}/12")
    print(f"[OK] Aylik: {aylik_ok}/12")
    print(f"[OK] Yukselen: {yukselen_ok}/12")
    print(f"[OK] Uyum: {uyum_ok}/78")
    print(f"TOPLAM: {haftalik_ok + aylik_ok + yukselen_ok + uyum_ok}/114")
    print("="*60)

if __name__ == '__main__':
    main()
