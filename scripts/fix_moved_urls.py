import os
import re

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content")

# Burç listesi ve bilgileri
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

for burc_key, info in burc_info.items():
    # Fix gunluk files
    gunluk_file = os.path.join(content_dir, "gunluk", f"{burc_key}.md")
    if os.path.exists(gunluk_file):
        with open(gunluk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace slug: "bugun" with url: "/xxx-burcu/bugun/"
        content = re.sub(r'slug: "bugun"', f'url: "/{info["slug"]}/bugun/"', content)

        with open(gunluk_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Fixed URL for gunluk/{burc_key}.md")

    # Fix haftalik files
    haftalik_file = os.path.join(content_dir, "haftalik", f"{burc_key}.md")
    if os.path.exists(haftalik_file):
        with open(haftalik_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Make sure URL is correct
        if f'url: "/{info["slug"]}/haftalik/"' not in content:
            content = re.sub(
                r'url: "[^"]*"',
                f'url: "/{info["slug"]}/haftalik/"',
                content,
                count=1
            )

        with open(haftalik_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Fixed URL for haftalik/{burc_key}.md")

    # Fix aylik files
    aylik_file = os.path.join(content_dir, "aylik", f"{burc_key}.md")
    if os.path.exists(aylik_file):
        with open(aylik_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Make sure URL is correct
        if f'url: "/{info["slug"]}/aylik/"' not in content:
            content = re.sub(
                r'url: "[^"]*"',
                f'url: "/{info["slug"]}/aylik/"',
                content,
                count=1
            )

        with open(aylik_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Fixed URL for aylik/{burc_key}.md")

print("\n[OK] All URLs fixed!")
