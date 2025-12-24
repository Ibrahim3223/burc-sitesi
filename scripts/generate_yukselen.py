"""
12 Yükselen Burç Sayfası Üretimi
"""

import os
from datetime import datetime
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
CONTENT_DIR = PROJECT_ROOT / 'hugo-site' / 'content' / 'yukselen-burc'

def create_yukselen_prompt(burc_data):
    """Yükselen burç içerik promptu"""
    return f"""Sen profesyonel bir astrologsun. Yükselen {burc_data['ad']} özellikleri hakkında detaylı bir rehber yaz.

YÜKSELEN BURÇ: {burc_data['ad']}
ELEMENT: {burc_data['element']}
YÖNETİCİ GEZEGEN: {burc_data['gezegen']}

YAZIYI ŞU FORMATTA YAZ:

## Yükselen Burç Nedir?
2-3 cümle ile yükselen burcun ne olduğunu genel olarak açıkla

## Yükselen {burc_data['ad']} Genel Özellikleri
4-5 cümle ile yükselen {burc_data['ad']} olanların genel kişilik özelliklerini anlat

## Fiziksel Görünüm ve İlk İzlenim
3-4 cümle ile yükselen {burc_data['ad']} olanların fiziksel özellikleri ve insanlara verdikleri ilk izlenim

## Kişilik ve Davranış Şekli
4-5 cümle ile sosyal hayatta nasıl davrandıkları, dış dünyaya nasıl göründükleri

## Aşk ve İlişkilerde Yükselen {burc_data['ad']}
3-4 cümle ile ilişkilerdeki tavırları, flört ederken nasıl oldukları

## Kariyerde Yükselen {burc_data['ad']}
3-4 cümle ile iş hayatındaki yaklaşımları, profesyonel imajları

## Güneş Burcu ile Farkı
3 cümle ile güneş burcu ve yükselen burç arasındaki farkı açıkla

## Yükselen {burc_data['ad']} ile Uyumlu Yükselenler
2-3 cümle ile hangi yükselen burçlarla uyumlu olduklarını anlat

## Yükselen Burcunuzu Nasıl Öğrenirsiniz?
2-3 cümle ile yükselen burç hesaplama hakkında bilgi ver (doğum saati gerekli)

ÖNEMLİ:
- Tamamen Türkçe yaz
- Profesyonel ama samimi bir dil kullan
- Güneş burcu ile yükselen burç farkını vurgula
- Sadece içeriği yaz, başka açıklama ekleme
- Markdown formatında yaz
- Her bölümü ## ile başlat"""

def generate_content_with_groq(prompt, max_retries=3):
    """Groq API ile içerik üret"""
    for attempt in range(max_retries):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen profesyonel bir astrolog ve yükselen burç uzmanısın."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0.7,
                max_tokens=2500,
                top_p=0.9
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"❌ Hata (Deneme {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"⏳ {wait_time} saniye bekleniyor...")
                time.sleep(wait_time)
            else:
                return None

    return None

def create_yukselen_markdown(burc_key, burc_data, content):
    """Yükselen burç markdown dosyası oluştur"""
    # Klasör oluştur
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    # Frontmatter
    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    slug = f"yukselen-{burc_key}"

    frontmatter = f"""---
title: "Yükselen {burc_data['ad']} Özellikleri - Kişilik ve Davranış"
slug: "{slug}"
date: {date_str}
lastmod: {date_str}
description: "Yükselen {burc_data['ad']} olanların kişilik özellikleri, fiziksel görünüm, ilişkiler ve kariyer yaklaşımları hakkında detaylı bilgiler."
keywords: ["yükselen {burc_data['ad']}", "yükselen {burc_key}", "ascendant {burc_data['ad']}", "rising {burc_data['ad']}"]
element: "{burc_data['element']}"
gezegen: "{burc_data['gezegen']}"
type: "yukselen"
burc: "{burc_data['ad']}"
draft: false
---

# Yükselen {burc_data['ad']} Özellikleri

"""

    # Tam içerik
    full_content = frontmatter + content

    # Dosyaya yaz
    file_path = CONTENT_DIR / f'{slug}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"✅ Yükselen {burc_data['ad']} sayfası oluşturuldu")

def create_main_yukselen_page():
    """Ana yükselen burç sayfası oluştur"""
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone()
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    date_str = date_str[:-2] + ':' + date_str[-2:]

    content = f"""---
title: "Yükselen Burç Nedir? Yükselen Burç Hesaplama"
date: {date_str}
lastmod: {date_str}
description: "Yükselen burç nedir, nasıl hesaplanır? 12 yükselen burç özellikleri ve kişiliğinize etkileri hakkında detaylı bilgiler."
keywords: ["yükselen burç", "yükselen burç hesaplama", "ascendant", "rising sign", "yükselen burç nedir"]
layout: "list"
---

# Yükselen Burç Nedir?

Yükselen burç (ascending veya rising sign), doğduğunuz anda doğu ufkunda yükselmekte olan burçtur. Güneş burcunuz sizin iç dünyanızı temsil ederken, yükselen burcunuz dış dünyaya yansıttığınız kişiliğinizi, fiziksel görünümünüzü ve insanlara verdiğiniz ilk izlenimi belirler.

## Yükselen Burç Nasıl Hesaplanır?

Yükselen burcunuzu öğrenmek için şunlara ihtiyacınız var:
- Doğum tarihiniz
- Doğum saatiniz (dakikaya kadar doğru)
- Doğum yeriniz

Yükselen burç her 2 saatte bir değiştiği için doğum saatinizin doğru olması çok önemlidir.

## Yükselen Burç ve Güneş Burcu Farkı

- **Güneş Burcu:** İç dünyamız, gerçek benliğimiz, öz karakterimiz
- **Yükselen Burç:** Dış görünüşümüz, davranış şeklimiz, ilk izlenimimiz

Yükselen burç bir maske gibidir - insanların sizi ilk gördüklerinde algıladıkları özelliklerdir.

## 12 Yükselen Burç Özellikleri

Aşağıda her yükselen burcun detaylı özelliklerini bulabilirsiniz:
"""

    file_path = CONTENT_DIR / '_index.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Ana yükselen burç sayfası oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("🌟 Yükselen Burç Sayfaları Üretimi Başlıyor...\n")

    # Ana sayfa oluştur
    create_main_yukselen_page()

    success_count = 0
    failed_count = 0

    for burc_key, burc_data in BURCLAR.items():
        print(f"📝 Yükselen {burc_data['ad']} içeriği üretiliyor...")

        # Prompt oluştur
        prompt = create_yukselen_prompt(burc_data)

        # İçerik üret
        content = generate_content_with_groq(prompt)

        if content:
            # Markdown dosyası oluştur
            create_yukselen_markdown(burc_key, burc_data, content)
            success_count += 1
        else:
            failed_count += 1
            print(f"❌ Yükselen {burc_data['ad']} üretilemedi!")

        # Rate limiting
        if burc_key != list(BURCLAR.keys())[-1]:
            time.sleep(2)

    # Özet
    print(f"\n{'='*60}")
    print(f"📊 ÖZET")
    print(f"{'='*60}")
    print(f"✅ Başarılı: {success_count}")
    print(f"❌ Başarısız: {failed_count}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
