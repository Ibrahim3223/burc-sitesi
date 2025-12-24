import os
import re

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content", "burc")

# Burç listesi
burclar = ["koc", "boga", "ikizler", "yengec", "aslan", "basak",
           "terazi", "akrep", "yay", "oglak", "kova", "balik"]

for burc in burclar:
    gunluk_file = os.path.join(content_dir, burc, "gunluk.md")

    if os.path.exists(gunluk_file):
        with open(gunluk_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace url: parameter with slug: parameter
        # Remove layout: "single" if present
        content = re.sub(r'layout: "single"\n', '', content)
        content = re.sub(r'url: "/[^/]+-burcu/bugun/"\n', 'slug: "bugun"\n', content)

        # Write back
        with open(gunluk_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Updated {burc}/gunluk.md to use slug")
    else:
        print(f"[ERROR] File not found: {gunluk_file}")

print("\n[OK] All gunluk.md files updated to use slug!")
