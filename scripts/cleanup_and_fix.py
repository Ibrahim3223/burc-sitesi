import os
import re

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content")

# Burç bilgileri
burc_info = {
    "koc": {"ad": "Koç", "slug": "koc-burcu"},
    "boga": {"ad": "Boğa", "slug": "boga-burcu"},
    "ikizler": {"ad": "İkizler", "slug": "ikizler-burcu"},
    "yengec": {"ad": "Yengeç", "slug": "yengec-burcu"},
    "aslan": {"ad": "Aslan", "slug": "aslan-burcu"},
    "basak": {"ad": "Başak", "slug": "basak-burcu"},
    "terazi": {"ad": "Terazi", "slug": "terazi-burcu"},
    "akrep": {"ad": "Akrep", "slug": "akrep-burcu"},
    "yay": {"ad": "Yay", "slug": "yay-burcu"},
    "oglak": {"ad": "Oğlak", "slug": "oglak-burcu"},
    "kova": {"ad": "Kova", "slug": "kova-burcu"},
    "balik": {"ad": "Balık", "slug": "balik-burcu"}
}

print("=== FIX 1: Günlük dosyalarını düzenleme ===")
for burc_key, info in burc_info.items():
    gunluk_file = os.path.join(content_dir, "gunluk", f"{burc_key}.md")

    if os.path.exists(gunluk_file):
        with open(gunluk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # URL parametresini kaldır, Hugo kendi oluştursun
        content = re.sub(r'url: "[^"]*"\n', '', content)

        # Arşiv linkini düzelt
        content = re.sub(
            r'\[arşive göz atın\]\([^)]+\)',
            f'[arşive göz atın](/{info["slug"]}/gunluk-arsiv/)',
            content
        )

        with open(gunluk_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Fixed gunluk/{burc_key}.md")

print("\n=== FIX 2: Haftalık dosyalarını düzenleme ===")
for burc_key, info in burc_info.items():
    haftalik_file = os.path.join(content_dir, "haftalik", f"{burc_key}.md")

    if os.path.exists(haftalik_file):
        with open(haftalik_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # URL parametresini kaldır
        content = re.sub(r'url: "[^"]*"\n', '', content)

        with open(haftalik_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Fixed haftalik/{burc_key}.md")

print("\n=== FIX 3: Aylık dosyalarını düzenleme ===")
for burc_key, info in burc_info.items():
    aylik_file = os.path.join(content_dir, "aylik", f"{burc_key}.md")

    if os.path.exists(aylik_file):
        with open(aylik_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # URL parametresini kaldır
        content = re.sub(r'url: "[^"]*"\n', '', content)

        with open(aylik_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Fixed aylik/{burc_key}.md")

print("\n=== Tüm içerik dosyaları düzeltildi! ===")
