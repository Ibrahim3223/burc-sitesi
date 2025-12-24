import os
import re

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content", "burc")

# Burç listesi ve isimleri
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
    gunluk_file = os.path.join(content_dir, burc_key, "gunluk.md")

    if os.path.exists(gunluk_file):
        with open(gunluk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add burc parameter if missing
        if 'burc:' not in content:
            # Find the line with url: and add burc: after it
            content = re.sub(
                r'(url: "/[^"]+"\n)',
                r'\1burc: "' + info['ad'] + '"\n',
                content
            )
            print(f"[OK] Added burc parameter to {burc_key}/gunluk.md")

        # Fix archive link
        old_archive_link = f'/[^"]+{info["slug"]}/gunluk/'
        new_archive_link = f'/{info["slug"]}/gunluk-arsiv/'

        if re.search(old_archive_link, content):
            content = re.sub(
                rf'(\[arşive göz atın\]\()/[^)]*{info["slug"]}/gunluk/\)',
                rf'\1/{info["slug"]}/gunluk-arsiv/)',
                content
            )
            print(f"[OK] Fixed archive link in {burc_key}/gunluk.md")

        # Write back
        with open(gunluk_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"[ERROR] File not found: {gunluk_file}")

print("\n[OK] All gunluk.md files updated!")
