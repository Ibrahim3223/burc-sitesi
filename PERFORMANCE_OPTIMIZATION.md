# ⚡ Performans Optimizasyonu Rehberi

## 📊 Genel Bakış

Bu dokümantasyon, Burç Sözlüğü sitesinde uygulanan tüm performans optimizasyonlarını detaylandırır.

## 🎯 Performans Hedefleri

- **Lighthouse Score**: 90+ (Mobile & Desktop)
- **First Contentful Paint (FCP)**: <1.5s
- **Largest Contentful Paint (LCP)**: <2.5s
- **Time to Interactive (TTI)**: <3.5s
- **Cumulative Layout Shift (CLS)**: <0.1
- **Total Blocking Time (TBT)**: <300ms

## ✅ Uygulanan Optimizasyonlar

### 1. HTML/CSS/JS Minification

Hugo'nun yerleşik minifikasyon özelliği aktif edildi.

**Fayda**: ~30-40% dosya boyutu azalması

### 2. Asset Caching

Build cache sistemi optimize edildi. Images ve assets kalıcı olarak cache'lenir.

**Fayda**: Daha hızlı build süreleri, tekrar build'de %80 hızlanma

### 3. Image Optimization

- CatmullRom resample filter
- Quality 85 (optimal kalite/boyut dengesi)
- Smart anchor (akıllı kırpma)

**Fayda**: %20-30 boyut azalması, görsel kalite korunur

### 4. Lazy Loading

**Dosya**: `static/js/lazy-load.js` (4.5KB)

**Özellikler**:
- Intersection Observer API
- 50px rootMargin (önceden yükleme)
- Resimler, background images, iframe desteği
- Fallback: IntersectionObserver yoksa tüm resimler yüklenir

**Fayda**: %40-60 ilk sayfa yükleme hızlanması

### 5. Resource Hints

- **DNS Prefetch**: Google Fonts için DNS çözümleme
- **Preconnect**: Google Fonts bağlantısı
- **Preload**: Kritik CSS ve JS

**Fayda**: 200-500ms ağ gecikmesi azalması

### 6. Font Loading Optimization

Asenkron font yükleme:
- Non-blocking yükleme
- `display=swap`: FOIT önleme
- Fallback: noscript tag

**Fayda**: ~500-800ms FCP iyileşmesi

### 7. Service Worker & Offline Support

**Dosyalar**:
- `static/sw.js`: Service worker (5.2KB)
- `static/offline.html`: Çevrimdışı sayfa (3.8KB)

**Özellikler**:
- Precaching kritik assetler
- Cache-first stratejisi
- Offline fallback
- Otomatik cache versiyonlama

**Fayda**:
- Çevrimdışı erişim
- %90+ hızlı tekrar ziyaret
- Düşük veri kullanımı

### 8. Script Loading Optimization

- **theme-toggle.js**: Senkron (FOUC önleme için)
- **Diğer scriptler**: Deferred (non-blocking)

**Fayda**: ~300-500ms TTI iyileşmesi

### 9. CSS Optimizations

- CSS Custom Properties (theming için)
- GPU-accelerated animations (`transform`, `opacity`)
- Modern selectors
- Minimize reflows/repaints

**Fayda**: 60 FPS animasyonlar

### 10. JavaScript Performance

- Event delegation
- Passive event listeners
- Intersection Observer (scroll events yerine)
- LocalStorage caching
- Debounce/throttle

**Fayda**: Daha düşük CPU kullanımı, akıcı scroll

## 📁 Optimizasyon Dosyaları

| Dosya | Boyut | Açıklama |
|-------|-------|----------|
| `hugo.toml` | +60 satır | Minifikasyon, caching, image config |
| `layouts/partials/head.html` | Güncellendi | Resource hints, preload |
| `static/js/lazy-load.js` | 4.5KB | Lazy loading sistemi |
| `static/sw.js` | 5.2KB | Service worker |
| `static/offline.html` | 3.8KB | Offline fallback |

## 📈 Beklenen Sonuçlar

### Lighthouse Scores (Hedef)

| Kategori | Desktop | Mobile |
|----------|---------|--------|
| Performance | 95-100 | 90-95 |
| Accessibility | 95-100 | 95-100 |
| Best Practices | 95-100 | 95-100 |
| SEO | 100 | 100 |

### Core Web Vitals

| Metrik | Hedef | Açıklama |
|--------|-------|----------|
| **LCP** | <2.5s | En büyük içerik boyası |
| **FID** | <100ms | İlk giriş gecikmesi |
| **CLS** | <0.1 | Kümülatif düzen kayması |
| **FCP** | <1.5s | İlk içerik boyası |
| **TTI** | <3.5s | Etkileşime hazır olma |

### Dosya Boyutları

| Asset | Önce | Sonra | Kazanç |
|-------|------|-------|--------|
| HTML | ~8KB | ~5KB | %37 |
| CSS | ~80KB | ~50KB | %37 |
| JS | ~35KB | ~30KB | %14 |
| **Toplam** | ~123KB | ~85KB | **%31** |

## 🚀 Hugo Build Komutları

```bash
# Development
hugo server --disableFastRender

# Production (optimized)
hugo --minify --gc --cleanDestinationDir

# Production + gzip
hugo --minify --gc && find public -type f -exec gzip -k {} \;
```

### Build Flags

- `--minify`: HTML/CSS/JS/JSON/XML minification
- `--gc`: Garbage collection
- `--cleanDestinationDir`: public/ temizleme

## 🧪 Test Etme

### Lighthouse Audit

```bash
# Chrome DevTools
1. F12 → Lighthouse sekmesi
2. "Generate report"

# CLI
npm install -g lighthouse
lighthouse https://burcsozlugu.com --view
```

### Diğer Araçlar

- **PageSpeed Insights**: https://pagespeed.web.dev/
- **WebPageTest**: https://www.webpagetest.org/
- **GTmetrix**: https://gtmetrix.com/

## 📊 Performans Checklist

- [x] HTML/CSS/JS minification
- [x] Image optimization
- [x] Lazy loading
- [x] Resource hints (dns-prefetch, preconnect, preload)
- [x] Font optimization
- [x] Service Worker
- [x] Offline support
- [x] Script defer/async
- [x] CSS custom properties
- [x] GPU-accelerated animations
- [x] Event delegation
- [x] Intersection Observer
- [ ] WebP images (TODO)
- [ ] HTTP/2 Server Push (TODO)
- [ ] Brotli compression (TODO)

## 🎯 Sonraki Adımlar

1. **WebP Conversion**: JPEG/PNG → WebP dönüşümü
2. **Critical CSS**: Above-the-fold CSS inline
3. **HTTP/2 Push**: Kritik kaynaklar
4. **Brotli**: Gzip yerine Brotli
5. **CDN**: Static asset delivery
6. **Prefetch**: Next page prefetching
7. **RUM**: Real User Monitoring

## 🔗 Kaynaklar

- [Web.dev Performance](https://web.dev/performance/)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [WebPageTest](https://www.webpagetest.org/)
- [Hugo Performance](https://gohugo.io/troubleshooting/build-performance/)
- [MDN Performance](https://developer.mozilla.org/en-US/docs/Web/Performance)
