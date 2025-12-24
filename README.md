# Burç Sözlüğü

Türkiye'nin en kapsamlı burç ve astroloji sitesi. Hugo static site generator ile oluşturulmuş, Groq API ile otomatik içerik üretimi yapan ve Cloudflare Pages'de barındırılan bir projedir.

## Özellikler

- 12 burç detay sayfası
- Günlük burç yorumları (otomatik güncelleme)
- Haftalık burç yorumları (otomatik güncelleme)
- Aylık burç yorumları (otomatik güncelleme)
- 144 burç uyumu kombinasyonu
- 12 yükselen burç sayfası
- SEO optimizasyonu
- Mobile responsive tasarım

## Teknoloji Stack

- **Hugo** - Static site generator
- **Groq API** - İçerik üretimi
- **Python** - Otomasyon scriptleri
- **GitHub Actions** - Otomatik deployment
- **Cloudflare Pages** - Hosting

## Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/yourusername/burc-sitesi.git
cd burc-sitesi
```

### 2. Bağımlılıkları yükleyin

```bash
# Hugo yükleyin (https://gohugo.io/installation/)

# Python bağımlılıkları
pip install -r requirements.txt
```

### 3. Environment değişkenlerini ayarlayın

```bash
cp .env.example .env
# .env dosyasını düzenleyin ve API key'leri ekleyin
```

### 4. İçerik oluşturun

```bash
# Tüm statik sayfaları oluştur
python scripts/generate_all_static.py

# Burç uyumu sayfalarını oluştur
python scripts/generate_compatibility.py

# Günlük yorumları oluştur
python scripts/generate_daily.py
```

### 5. Hugo sunucusunu başlatın

```bash
cd hugo-site
hugo server -D
```

Site http://localhost:1313 adresinde çalışacaktır.

## GitHub Actions Kurulumu

### Secrets Ekleyin

Repository Settings > Secrets and variables > Actions:

- `GROQ_API_KEY` - Groq API anahtarınız
- `CLOUDFLARE_API_TOKEN` - Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID` - Cloudflare hesap ID

### Workflow'lar

- **Daily Horoscope** - Her gün saat 06:00'da çalışır
- **Weekly Horoscope** - Her Pazartesi saat 05:00'da çalışır
- **Monthly Horoscope** - Her ayın 1'i saat 04:00'da çalışır

## Proje Yapısı

```
burc-sitesi/
├── hugo-site/
│   ├── content/           # İçerik dosyaları
│   ├── layouts/           # Hugo template'leri
│   ├── static/            # Statik dosyalar (CSS, JS, images)
│   └── hugo.toml          # Hugo konfigürasyonu
├── scripts/               # Python scriptleri
│   ├── generate_daily.py
│   ├── generate_weekly.py
│   ├── generate_monthly.py
│   ├── generate_all_static.py
│   └── generate_compatibility.py
├── .github/
│   └── workflows/         # GitHub Actions
└── requirements.txt       # Python bağımlılıkları
```

## Lisans

MIT License

## İletişim

Web: https://burcsozlugu.com
