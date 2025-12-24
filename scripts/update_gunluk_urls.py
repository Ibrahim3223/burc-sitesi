import os
import re

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content", "burc")

# Burç listesi
burclar = ["koc", "boga", "ikizler", "yengec", "aslan", "basak",
           "terazi", "akrep", "yay", "oglak", "kova", "balik"]

# Burç slug mapping
slug_map = {
    "koc": "koc-burcu",
    "boga": "boga-burcu",
    "ikizler": "ikizler-burcu",
    "yengec": "yengec-burcu",
    "aslan": "aslan-burcu",
    "basak": "basak-burcu",
    "terazi": "terazi-burcu",
    "akrep": "akrep-burcu",
    "yay": "yay-burcu",
    "oglak": "oglak-burcu",
    "kova": "kova-burcu",
    "balik": "balik-burcu"
}

for burc in burclar:
    gunluk_file = os.path.join(content_dir, burc, "gunluk.md")

    if os.path.exists(gunluk_file):
        # Read file
        with open(gunluk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get slug for this burc
        slug = slug_map.get(burc, f"{burc}-burcu")

        # Replace /gunluk/ with /bugun/ in URL parameter
        old_url = f'url: "/{slug}/gunluk/"'
        new_url = f'url: "/{slug}/bugun/"'

        if old_url in content:
            content = content.replace(old_url, new_url)

            # Write back
            with open(gunluk_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"[OK] Updated {burc}/gunluk.md: {old_url} -> {new_url}")
        else:
            print(f"[WARN] {burc}/gunluk.md: URL pattern not found")
    else:
        print(f"[ERROR] File not found: {gunluk_file}")

print("\n[OK] All gunluk.md files updated!")
