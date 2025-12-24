# GitHub Actions - Otomatik Burç Yorumu Güncellemesi

Bu dokümanda, günlük, haftalık ve aylık burç yorumlarının otomatik olarak oluşturulması ve arşivlenmesi için gerekli GitHub Actions yapılandırması açıklanmaktadır.

## Sistem Yapısı

### Mevcut Dosya Yapısı

```
hugo-site/
└── content/
    └── burc/
        ├── koc/
        │   ├── _index.md          # Burç detay sayfası
        │   ├── gunluk.md          # Güncel günlük yorum
        │   ├── haftalik.md        # Güncel haftalık yorum
        │   ├── aylik.md           # Güncel aylık yorum
        │   ├── gunluk/
        │   │   └── arsiv/
        │   │       ├── _index.md  # Arşiv liste sayfası
        │   │       └── [tarihli yorumlar buraya arşivlenir]
        │   ├── haftalik/
        │   │   └── arsiv/
        │   │       ├── _index.md
        │   │       └── [tarihli yorumlar buraya arşivlenir]
        │   └── aylik/
        │       └── arsiv/
        │           ├── _index.md
        │           └── [tarihli yorumlar buraya arşivlenir]
        ├── aslan/
        │   └── [aynı yapı]
        └── [diğer burçlar...]
```

### URL Yapısı

- **Güncel Yorumlar:**
  - `/koc-burcu/gunluk/` - Güncel günlük yorum
  - `/koc-burcu/haftalik/` - Güncel haftalık yorum
  - `/koc-burcu/aylik/` - Güncel aylık yorum

- **Arşiv Sayfaları:**
  - `/koc-burcu/gunluk/arsiv/` - Günlük yorumlar arşiv listesi
  - `/koc-burcu/haftalik/arsiv/` - Haftalık yorumlar arşiv listesi
  - `/koc-burcu/aylik/arsiv/` - Aylık yorumlar arşiv listesi

## Önemli Notlar

1. **Tüm burçlar için 12 ayrı klasör var:**
   - koc, boga, ikizler, yengec, aslan, basak, terazi, akrep, yay, oglak, kova, balik

2. **Her burç için 3 arşiv dizini var:**
   - gunluk/arsiv/, haftalik/arsiv/, aylik/arsiv/

3. **Toplam 36 arşiv dizini oluşturuldu ve kullanıma hazır.**

4. **Arşiv sayfaları şu anda boş.** GitHub Actions ile yeni yorumlar eklendiğinde, eski yorumlar bu dizinlere taşınacak.

5. **Tüm arşiv sayfalarına erişim:**
   - http://localhost:1313/{burc-slug}/gunluk/arsiv/
   - http://localhost:1313/{burc-slug}/haftalik/arsiv/
   - http://localhost:1313/{burc-slug}/aylik/arsiv/

## Arşivleme Mantığı

GitHub Actions workflow'ları şunları yapmalı:

1. **Her gün (günlük için):** 
   - Mevcut gunluk.md'yi `gunluk/arsiv/YYYY-MM-DD/_index.md` olarak kopyala
   - URL parametresini `/koc-burcu/gunluk/arsiv/YYYY-MM-DD/` olarak güncelle
   - Yeni gunluk.md oluştur

2. **Her hafta (haftalık için):**
   - Mevcut haftalik.md'yi `haftalik/arsiv/YYYY-MM-DD-DD/_index.md` olarak kopyala
   - Yeni haftalik.md oluştur

3. **Her ay (aylık için):**
   - Mevcut aylik.md'yi `aylik/arsiv/YYYY-MM/_index.md` olarak kopyala
   - Yeni aylik.md oluştur

## Gelecek Adımlar

1. GitHub Actions workflow dosyalarını oluştur
2. AI yorum oluşturma scriptlerini yaz
3. Test et ve gerekirse düzenle
