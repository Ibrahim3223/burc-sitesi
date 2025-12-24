import os
import re

hugo_dir = r"c:\Users\Dante\Desktop\Yeniden\WebSite\burc-sitesi\hugo-site"
layouts_dir = os.path.join(hugo_dir, "layouts")

# Burç key'leri
burc_keys = ["koc", "boga", "ikizler", "yengec", "aslan", "basak",
             "terazi", "akrep", "yay", "oglak", "kova", "balik"]

print("=== FIX 1: index.html - Ana sayfa kartları ===")
index_file = os.path.join(layouts_dir, "index.html")
with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Günlük linkini düzelt - burcKey kullanarak
# Eski: href="/{{ $burc.slug }}/bugun/"
# Yeni: href="/gunluk/{{ $key }}/"
content = re.sub(
    r'<a href="/\{\{ \$burc\.slug \}\}/bugun/" class="card-cta">',
    r'<a href="/gunluk/{{ $key }}/" class="card-cta">',
    content
)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated index.html")

print("\n=== FIX 2: gunluk-liste/single.html ===")
gunluk_liste_file = os.path.join(layouts_dir, "gunluk-liste", "single.html")
with open(gunluk_liste_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Eski: href="/{{ $burc.slug }}/bugun/"
# Yeni: href="/gunluk/{{ $key }}/"
content = re.sub(
    r'<a href="/\{\{ \$burc\.slug \}\}/bugun/"',
    r'<a href="/gunluk/{{ $key }}/"',
    content
)

with open(gunluk_liste_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated gunluk-liste/single.html")

print("\n=== FIX 3: haftalik-liste/single.html ===")
haftalik_liste_file = os.path.join(layouts_dir, "haftalik-liste", "single.html")
with open(haftalik_liste_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Eski: href="/{{ $burc.slug }}/haftalik/"
# Yeni: href="/haftalik/{{ $key }}/"
content = re.sub(
    r'<a href="/\{\{ \$burc\.slug \}\}/haftalik/"',
    r'<a href="/haftalik/{{ $key }}/"',
    content
)

with open(haftalik_liste_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated haftalik-liste/single.html")

print("\n=== FIX 4: aylik-liste/single.html ===")
aylik_liste_file = os.path.join(layouts_dir, "aylik-liste", "single.html")
with open(aylik_liste_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Eski: href="/{{ $burc.slug }}/aylik/"
# Yeni: href="/aylik/{{ $key }}/"
content = re.sub(
    r'<a href="/\{\{ \$burc\.slug \}\}/aylik/"',
    r'<a href="/aylik/{{ $key }}/"',
    content
)

with open(aylik_liste_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated aylik-liste/single.html")

print("\n=== FIX 5: burc/single.html - Burç detay sayfası ===")
burc_single_file = os.path.join(layouts_dir, "burc", "single.html")
with open(burc_single_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Quick actions bölümünü tamamen yeniden yazalım
old_quick_actions = re.search(
    r'<div class="burc-quick-actions">.*?</div>',
    content,
    re.DOTALL
)

if old_quick_actions:
    new_quick_actions = '''<div class="burc-quick-actions">
            {{- if $burcSlug }}
            <a href="/gunluk/{{ $burcKey }}/" class="burc-action-btn burc-action-primary">
                <span class="action-icon">📅</span>
                <span class="action-text">Günlük Yorum</span>
            </a>
            <a href="/haftalik/{{ $burcKey }}/" class="burc-action-btn burc-action-secondary">
                <span class="action-icon">📊</span>
                <span class="action-text">Haftalık Yorum</span>
            </a>
            <a href="/aylik/{{ $burcKey }}/" class="burc-action-btn burc-action-secondary">
                <span class="action-icon">📈</span>
                <span class="action-text">Aylık Yorum</span>
            </a>
            {{- end }}
        </div>'''

    content = content.replace(old_quick_actions.group(0), new_quick_actions)

with open(burc_single_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated burc/single.html")

print("\n=== FIX 6: _default/single.html ===")
default_single_file = os.path.join(layouts_dir, "_default", "single.html")
with open(default_single_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Quick actions linklerini düzelt
content = re.sub(
    r'<a href="/\{\{ \$burcSlug \}\}/bugun/"',
    r'<a href="/gunluk/{{ $burcKey }}/"',
    content
)
content = re.sub(
    r'<a href="/\{\{ \$burcSlug \}\}/haftalik/"',
    r'<a href="/haftalik/{{ $burcKey }}/"',
    content
)

with open(default_single_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("[OK] Updated _default/single.html")

print("\n=== Tüm layout dosyaları güncellendi! ===")
