# -*- coding: utf-8 -*-
"""
Tum icerik uretim scripti - 12 burc + yukselen + uyum + gunluk/haftalik/aylik
"""

import os
import sys
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
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content'

def generate_with_groq(prompt, max_tokens=4000, temperature=0.7):
    """Groq API ile icerik uret"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen profesyonel bir astrolog ve icerik yazarissin. Turkce burc icerikleri yaziyorsun."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.9
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"[HATA] API: {e}")
        return None

def create_burc_page(burc_key, burc_data):
    """Burc ana sayfasi olustur"""
    print(f">>> {burc_data['ad']} burcu ana sayfasi uretiliyor...")

    prompt = f"""Sen profesyonel bir astrologsun. {burc_data['ad']} burcu icin kapsamli bir rehber yaz.

BURC: {burc_data['ad']} ({burc_data['tarih']})
ELEMENT: {burc_data['element']}
GEZEGEN: {burc_data['gezegen']}

SU BOLUMLERI YAZ (Markdown):

## Genel Bilgiler
Tarih araligi ve temel ozellikler (100 kelime)

## Kisilik Ozellikleri
Detayli karakter analizi, guclu ve zayif yonler (500-700 kelime)

## Ask ve Iliskiler
Ask hayati, ideal partner, iliskide beklentiler (300-400 kelime)

## Kariyer ve Is Hayati
Uygun meslekler, calisma tarzi, liderlik ozellikleri (300-400 kelime)

## Saglik
Dikkat edilmesi gereken organlar, saglik onerileri (200-300 kelime)

## Para ve Finans
Para yonetimi, harcama aliskanl

iklari, yatirim egilimleri (200-300 kelime)

## Aile ve Arkadaslik
Aile ici rol, arkadaslik anlayisi (200-300 kelime)

## Unlu {burc_data['ad']} Burcu Kisileri
8-10 unlu isim listele

## Sik Sorulan Sorular

### {burc_data['ad']} burcu hangi burclarla uyumludur?
### {burc_data['ad']} burcunun en guclu yonu nedir?
### {burc_data['ad']} burcu hangi mesleklerde basarili olur?
### {burc_data['ad']} burcunun sans tasi nedir?
### {burc_data['ad']} burcu nasil biri ile evlenmeli?

ONEMLI: Turkce yaz, profesyonel ama samimi dil, SEO dostu, sadece icerigi yaz."""

    content = generate_with_groq(prompt)
    if not content:
        print(f"[HATA] {burc_data['ad']} burcu uretilemedi")
        return False

    # Klasor olustur
    burc_dir = CONTENT_DIR / 'burc' / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Ozellikleri, Kisilik Analizi ve Uyumu"
slug: "{burc_data['slug']}"
date: {date_str}
description: "{burc_data['ad']} burcu ozellikleri, kisilik analizi, ask uyumu, kariyer hakkinda detayli bilgiler."
keywords: ["{burc_data['ad']} burcu", "{burc_data['slug']}", "{burc_data['ad']} ozellikleri"]
element: "{burc_data['element']}"
nitelik: "{burc_data['nitelik']}"
gezegen: "{burc_data['gezegen']}"
tarih: "{burc_data['tarih']}"
draft: false
---

"""

    # Yaz
    file_path = burc_dir / '_index.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"[OK] {burc_data['ad']} burcu tamamlandi")
    return True

def create_daily(burc_key, burc_data):
    """Gunluk yorum olustur"""
    now = datetime.now()
    aylar = ['', 'Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran',
             'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik']
    tarih = f"{now.day} {aylar[now.month]} {now.year}"

    prompt = f"""Sen astrologsun. {burc_data['ad']} burcu icin {tarih} gunluk yorum yaz.

## Genel Enerji
2-3 cumle
## Ask ve Iliskiler
2-3 cumle
## Kariyer ve Is
2-3 cumle
## Saglik
1-2 cumle
## Sans Faktorleri
- Sans Puani: 7/10
- Sans Sayisi: {burc_data['sans_sayilari'][0]}
- Sans Rengi: {burc_data['sans_renkleri'][0]}
## Gunun Tavsiyesi
1 cumle

Turkce yaz, sadece icerigi yaz."""

    content = generate_with_groq(prompt, max_tokens=1500, temperature=0.8)
    if not content:
        return False

    burc_dir = CONTENT_DIR / 'burc' / burc_key
    burc_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    frontmatter = f"""---
title: "{burc_data['ad']} Burcu Gunluk Yorum - {tarih}"
date: {date_str}
description: "{burc_data['ad']} burcu icin {tarih} gunluk burc yorumu."
keywords: ["{burc_data['ad']} gunluk", "gunluk {burc_data['ad']}"]
type: "gunluk"
burc: "{burc_data['ad']}"
draft: false
---

# {burc_data['ad']} Burcu Gunluk Yorum - {tarih}

"""

    file_path = burc_dir / 'gunluk.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True

def main():
    """Ana fonksiyon"""
    print("="*60)
    print(">>> BURC SOZLUGU - ICERIK URETIMI")
    print("="*60)

    # 12 Burc Ana Sayfalari
    print("\n[1/2] 12 Burc Ana Sayfasi Uretiliyor...")
    burc_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        if create_burc_page(burc_key, burc_data):
            burc_ok += 1
        time.sleep(3)

    print(f"\n[OK] {burc_ok}/12 burc ana sayfasi olusturuldu")

    # Gunluk Yorumlar
    print("\n[2/2] 12 Gunluk Yorum Uretiliyor...")
    gunluk_ok = 0
    for burc_key, burc_data in BURCLAR.items():
        print(f">>> {burc_data['ad']} gunluk yorum...")
        if create_daily(burc_key, burc_data):
            gunluk_ok += 1
        time.sleep(2)

    print(f"\n[OK] {gunluk_ok}/12 gunluk yorum olusturuldu")

    # Ozet
    print("\n" + "="*60)
    print(">>> OZET")
    print("="*60)
    print(f"[OK] Burc Sayfalari: {burc_ok}/12")
    print(f"[OK] Gunluk Yorumlar: {gunluk_ok}/12")
    print(f"[DIZIN] {CONTENT_DIR}")
    print("="*60)

if __name__ == '__main__':
    main()
