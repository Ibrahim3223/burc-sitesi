import os
import shutil

# Hugo site content directory
hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
content_dir = os.path.join(hugo_dir, "content")

# Burç listesi
burclar = ["koc", "boga", "ikizler", "yengec", "aslan", "basak",
           "terazi", "akrep", "yay", "oglak", "kova", "balik"]

# Move gunluk, haftalik, aylik files to new locations
for burc in burclar:
    old_burc_dir = os.path.join(content_dir, "burc", burc)

    # Move gunluk.md
    old_gunluk = os.path.join(old_burc_dir, "gunluk.md")
    new_gunluk = os.path.join(content_dir, "gunluk", f"{burc}.md")
    if os.path.exists(old_gunluk):
        shutil.move(old_gunluk, new_gunluk)
        print(f"[OK] Moved {burc}/gunluk.md to gunluk/{burc}.md")

    # Move haftalik.md
    old_haftalik = os.path.join(old_burc_dir, "haftalik.md")
    new_haftalik = os.path.join(content_dir, "haftalik", f"{burc}.md")
    if os.path.exists(old_haftalik):
        shutil.move(old_haftalik, new_haftalik)
        print(f"[OK] Moved {burc}/haftalik.md to haftalik/{burc}.md")

    # Move aylik.md
    old_aylik = os.path.join(old_burc_dir, "aylik.md")
    new_aylik = os.path.join(content_dir, "aylik", f"{burc}.md")
    if os.path.exists(old_aylik):
        shutil.move(old_aylik, new_aylik)
        print(f"[OK] Moved {burc}/aylik.md to aylik/{burc}.md")

print("\n[OK] All files moved!")
