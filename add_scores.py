import os
import random

# Burç listesi
burclar = ['koc', 'boga', 'ikizler', 'yengec', 'aslan', 'basak',
           'terazi', 'akrep', 'yay', 'oglak', 'kova', 'balik']

for burc in burclar:
    gunluk_path = f'hugo-site/content/burc/{burc}/gunluk.md'

    if not os.path.exists(gunluk_path):
        print(f'[SKIP] {burc} icin gunluk.md bulunamadi')
        continue

    # Dosyayı oku
    with open(gunluk_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Eğer genel_puan zaten varsa atla
    if 'genel_puan:' in content:
        print(f'[OK] {burc} icin puanlar zaten mevcut')
        continue

    # Random puanlar oluştur
    genel = random.randint(6, 9)
    ask = random.randint(6, 9)
    kariyer = random.randint(6, 9)
    saglik = random.randint(6, 9)

    # aliases satırından önce puanları ekle
    new_content = content.replace(
        'aliases:',
        f'''genel_puan: {genel}
ask_puani: {ask}
kariyer_puani: {kariyer}
saglik_puani: {saglik}
aliases:'''
    )

    # Dosyayı yaz
    with open(gunluk_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'[DONE] {burc} icin puanlar eklendi (Genel: {genel}/10)')

print('\n[SUCCESS] Tum burclar icin puanlar eklendi!')
