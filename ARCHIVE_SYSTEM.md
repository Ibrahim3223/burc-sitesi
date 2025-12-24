# Burç Arşiv Sistemi

## 🎯 Genel Bakış

Yeni arşiv sistemi ile günlük, haftalık ve aylık burç yorumları artık **ÜZERİNE YAZILMAK YERİNE** her zaman yeni bir sayfa olarak oluşturulmaktadır. Bu sayede:

- ✅ Her gün/hafta/ay için ayrı SEO-dostu URL
- ✅ Geçmiş yorumlar kaybolmaz
- ✅ Kullanıcılar eski yorumlara erişebilir
- ✅ Google için daha fazla indexlenebilir sayfa

## 📁 Dosya Yapısı

### Günlük Yorumlar
```
/hugo-site/content/burc/koc/
├── gunluk/
│   ├── _index.md           # Arşiv index sayfası
│   ├── 2025-12-23.md       # Bugünün yorumu
│   ├── 2025-12-24.md       # Yarının yorumu
│   └── ...
└── gunluk.md               # "Latest" sayfası (her gün güncellenir)
```

**URL Yapısı:**
- Arşiv index: `/koc-burcu/gunluk/`
- Bugünün yorumu: `/koc-burcu/gunluk/2025-12-23/`
- Latest redirect: `/koc-burcu/gunluk.html` → güncel yorum gösterir

### Haftalık Yorumlar
```
/hugo-site/content/burc/koc/
├── haftalik/
│   ├── _index.md           # Arşiv index sayfası
│   ├── 2025-W51.md         # Bu haftanın yorumu (ISO hafta numarası)
│   ├── 2025-W52.md         # Gelecek hafta
│   └── ...
└── haftalik.md             # "Latest" sayfası
```

**URL Yapısı:**
- Arşiv index: `/koc-burcu/haftalik/`
- Bu haftanın yorumu: `/koc-burcu/haftalik/2025-W51/`

### Aylık Yorumlar
```
/hugo-site/content/burc/koc/
├── aylik/
│   ├── _index.md           # Arşiv index sayfası
│   ├── 2025-12.md          # Bu ayın yorumu
│   ├── 2026-01.md          # Gelecek ay
│   └── ...
└── aylik.md                # "Latest" sayfası
```

**URL Yapısı:**
- Arşiv index: `/koc-burcu/aylik/`
- Bu ayın yorumu: `/koc-burcu/aylik/2025-12/`

## 🚀 Kullanım

### Günlük Yorum Oluşturma
```bash
cd scripts
python generate_daily_archive.py
```

**Ne yapar:**
- 12 burç için bugünkü tarihli yeni sayfa oluşturur
- Format: `YYYY-MM-DD.md` (örn: `2025-12-23.md`)
- `gunluk.md` dosyasını güncel yorumla günceller
- İlk çalıştırmada `_index.md` arşiv sayfası oluşturur

### Haftalık Yorum Oluşturma
```bash
cd scripts
python generate_weekly_archive.py
```

**Ne yapar:**
- 12 burç için bu haftanın yorumunu oluşturur
- Format: `YYYY-WWW.md` (örn: `2025-W51.md`)
- ISO 8601 hafta numarası kullanır
- `haftalik.md` dosyasını günceller

### Aylık Yorum Oluşturma
```bash
cd scripts
python generate_monthly_archive.py
```

**Ne yapar:**
- 12 burç için bu ayın yorumunu oluşturur
- Format: `YYYY-MM.md` (örn: `2025-12.md`)
- `aylik.md` dosyasını günceller

## 🤖 Otomasyonlar

### GitHub Actions

Günlük yorumlar için GitHub Actions kullanarak otomatik üretim yapılabilir:

```yaml
name: Günlük Burç Yorumları

on:
  schedule:
    - cron: '0 3 * * *'  # Her gün saat 03:00 UTC
  workflow_dispatch:      # Manuel tetikleme

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd scripts
          pip install -r requirements.txt

      - name: Generate daily horoscopes
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        run: |
          cd scripts
          python generate_daily_archive.py

      - name: Commit and push
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add .
          git commit -m "Günlük burç yorumları: $(date +'%Y-%m-%d')"
          git push
```

### Cron Jobs (Sunucu)

Eğer kendi sunucunuzda çalıştırıyorsanız:

```bash
# Günlük - Her gün saat 03:00
0 3 * * * cd /path/to/burc-sitesi/scripts && python generate_daily_archive.py

# Haftalık - Her Pazartesi saat 04:00
0 4 * * 1 cd /path/to/burc-sitesi/scripts && python generate_weekly_archive.py

# Aylık - Her ayın 1'i saat 05:00
0 5 1 * * cd /path/to/burc-sitesi/scripts && python generate_monthly_archive.py
```

## 📊 SEO Avantajları

### 1. Unique URLs
Her yorum için benzersiz URL:
- `/koc-burcu/gunluk/2025-12-23/`
- `/koc-burcu/gunluk/2025-12-24/`
- vs.

### 2. Arşiv Sayfaları
Her burç için arşiv index sayfaları:
- `/koc-burcu/gunluk/` - Tüm günlük yorumları listeler
- `/koc-burcu/haftalik/` - Tüm haftalık yorumları listeler
- `/koc-burcu/aylik/` - Tüm aylık yorumları listeler

### 3. Internal Linking
- Latest sayfalardan arşive link
- Arşiv sayfalarından her bir yoruma link
- Breadcrumb navigation

## 🔄 Eski Sistemden Geçiş

### Önceki Sistem (Problem)
```
/burc/koc/gunluk.md    → Her gün ÜZERİNE yazılıyor ❌
/burc/koc/haftalik.md  → Her hafta ÜZERİNE yazılıyor ❌
/burc/koc/aylik.md     → Her ay ÜZERİNE yazılıyor ❌
```

### Yeni Sistem (Çözüm)
```
/burc/koc/gunluk/2025-12-23.md  → Yeni sayfa ✅
/burc/koc/gunluk/2025-12-24.md  → Yeni sayfa ✅
/burc/koc/gunluk.md             → Latest (opsiyonel) ✅
```

## 📝 Frontmatter Yapısı

### Günlük Arşiv
```yaml
---
title: "Koç Burcu Günlük Yorum - 23 Aralık 2025"
slug: "2025-12-23"
date: 2025-12-23T10:31:58+03:00
lastmod: 2025-12-23T10:31:58+03:00
description: "Koç burcu için 23 Aralık 2025 günlük burç yorumu."
keywords: ["Koç günlük", "günlük Koç", "Koç bugün"]
layout: "single"
type: "gunluk"
burc: "Koç"
tarih: "23 Aralık 2025"
tarih_slug: "2025-12-23"
draft: false
---
```

### Haftalık Arşiv
```yaml
---
title: "Koç Burcu Haftalık Yorum - 16 Aralık - 22 Aralık 2025"
slug: "2025-W51"
date: 2025-12-23T10:40:00+03:00
description: "Koç burcu için haftalık burç yorumu."
type: "haftalik"
burc: "Koç"
tarih_araligi: "16 Aralık - 22 Aralık 2025"
week_slug: "2025-W51"
draft: false
---
```

### Aylık Arşiv
```yaml
---
title: "Koç Burcu Aylık Yorum - Aralık 2025"
slug: "2025-12"
date: 2025-12-23T10:45:00+03:00
description: "Koç burcu için Aralık 2025 aylık burç yorumu."
type: "aylik"
burc: "Koç"
ay_tam: "Aralık 2025"
month_slug: "2025-12"
draft: false
---
```

## 🔍 Sorun Giderme

### Arşiv sayfası oluşturulmadı
- `_index.md` dosyası otomatik oluşturulur ilk çalıştırmada
- Eğer yoksa manuel olarak oluşturabilirsiniz

### Tarih formatı hataları
- Günlük: `YYYY-MM-DD` (2025-12-23)
- Haftalık: `YYYY-Www` (2025-W51)
- Aylık: `YYYY-MM` (2025-12)

### Hugo build hatası
```bash
# Hugo cache temizle
hugo --gc

# Yeniden build
hugo --minify
```

## 📈 Gelecek Geliştirmeler

- [ ] Arşiv sayfalarında pagination
- [ ] Takvim view (달력 görünümü)
- [ ] Tarih arama filtresi
- [ ] RSS feeds için arşiv desteği
- [ ] Sitemap otomasyonu
