# 🌗 Dark/Light Mode Toggle - Kullanım Rehberi

## 📋 Özellikler

✅ **Koyu/Açık Mod Geçişi** - Tek tıkla tema değiştirme
✅ **LocalStorage Hafızası** - Kullanıcı tercihi kalıcı olarak saklanır
✅ **Sistem Tercihi Desteği** - `prefers-color-scheme` medya sorgusunu destekler
✅ **Animasyonlu Geçiş** - Yumuşak renk geçişleri
✅ **Erişilebilirlik** - ARIA etiketleri ve klavye desteği
✅ **Performans** - FOUC (Flash of Unstyled Content) önleme
✅ **Mobil Uyumlu** - Responsive tasarım

## 🎨 Tema Özellikleri

### Koyu Tema (Varsayılan)
- Mistik mor-siyah gradient arka plan
- Yüksek kontrast beyaz metin
- Parlak mor-turuncu vurgular
- Tam yoğunlukta yıldız animasyonu

### Açık Tema
- Temiz beyaz-gri gradient arka plan
- Koyu gri metin (okunabilirlik için)
- Canlı mor-turuncu vurgular
- Azaltılmış yıldız animasyonu (%30 opaklık)

## 📁 Dosyalar

| Dosya | Açıklama | Boyut |
|-------|----------|-------|
| `js/theme-toggle.js` | Tema değiştirme mantığı | 3.7KB |
| `css/style.css` | Tema CSS değişkenleri ve stilleri | ~250 satır eklendi |
| `layouts/partials/header.html` | Tema toggle butonu HTML | Güncellendi |
| `layouts/partials/head.html` | Script yükleme | Güncellendi |

## 🔧 Teknik Detaylar

### CSS Custom Properties

Tema sistemi CSS custom properties (CSS değişkenleri) kullanır:

```css
:root[data-theme="dark"] {
  --bg-primary: linear-gradient(...);
  --text-primary: #ffffff;
  --accent-primary: #8b5cf6;
  /* ... */
}

:root[data-theme="light"] {
  --bg-primary: linear-gradient(...);
  --text-primary: #1a1a1a;
  --accent-primary: #7c3aed;
  /* ... */
}
```

### JavaScript API

Tema toggle sistemi global API sağlar:

```javascript
// Tema değiştir
window.ThemeToggle.toggle();

// Belirli tema uygula
window.ThemeToggle.setTheme('dark');
window.ThemeToggle.setTheme('light');

// Mevcut temayı al
const currentTheme = window.ThemeToggle.getTheme();
```

### LocalStorage

Kullanıcı tercihi `localStorage` içinde saklanır:

```javascript
localStorage.setItem('burc-theme', 'dark'); // veya 'light'
```

### FOUC Önleme

Script `<head>` içinde senkron yüklenerek sayfa yüklenmeden önce doğru tema uygulanır:

```html
<script src="/js/theme-toggle.js"></script>
```

## 🎯 Kullanım

### Kullanıcı Tarafı

1. Sağ üst köşedeki tema toggle butonuna tıklayın
2. Buton simgesi ve metni değişecektir:
   - Koyu modda: ☀️ "Aydınlık Mod"
   - Açık modda: 🌙 "Karanlık Mod"
3. Tercih otomatik olarak kaydedilir
4. Sayfayı yenilediğinizde seçiminiz korunur

### Klavye Erişilebilirliği

- `Tab` ile butona odaklan
- `Enter` veya `Space` ile temayı değiştir

### Sistem Tercihi

Kullanıcı manuel seçim yapmadıysa:
- Sistem koyu mod tercih ediyorsa → Koyu tema
- Sistem açık mod tercih ediyorsa → Açık tema
- Manuel seçim yapıldıktan sonra sistem tercihi göz ardı edilir

## 🎨 Özelleştirme

### Tema Renklerini Değiştirme

`style.css` dosyasında CSS custom properties'i düzenleyin:

```css
:root[data-theme="light"] {
    --bg-primary: /* Kendi renginiz */;
    --text-primary: /* Kendi renginiz */;
    /* ... */
}
```

### Buton Konumunu Değiştirme

Theme toggle butonu header içinde `margin-left: auto` ile sağa hizalanmıştır.
Konumu değiştirmek için `#theme-toggle` CSS'ini güncelleyin.

### Geçiş Süresini Ayarlama

```css
* {
    transition: background-color 0.3s ease, color 0.3s ease, ...;
}
```

`0.3s` değerini değiştirerek geçiş hızını ayarlayabilirsiniz.

## ♿ Erişilebilirlik

- **ARIA Labels**: Ekran okuyucular için açıklayıcı etiketler
- **Klavye Navigasyonu**: Tab ve Enter/Space tuş desteği
- **Yüksek Kontrast**: Her iki temada da WCAG AA uyumlu kontrast oranları
- **Reduced Motion**: `prefers-reduced-motion` tercihi desteklenir

## 🖨️ Yazdırma Desteği

Yazdırma sırasında otomatik olarak açık tema uygulanır:

```css
@media print {
    :root {
        --bg-primary: #ffffff;
        --text-primary: #000000;
    }
}
```

## 📱 Responsive Tasarım

### Desktop (≥768px)
- İkon + metin gösterilir
- "☀️ Aydınlık Mod" / "🌙 Karanlık Mod"

### Mobile (<768px)
- Sadece ikon gösterilir
- Daha büyük ikon (24px)
- Kompakt tasarım

## 🐛 Sorun Giderme

### Tema değişmiyor

**Kontrol edin:**
1. `theme-toggle.js` yükleniyor mu? (DevTools → Network)
2. Console'da hata var mı?
3. LocalStorage aktif mi?

**Çözüm:**
```javascript
// LocalStorage'ı temizle
localStorage.removeItem('burc-theme');
// Sayfayı yenile
location.reload();
```

### Sayfa yüklenirken tema "yanıp sönüyor" (FOUC)

**Kontrol edin:**
1. `theme-toggle.js` `<head>` içinde mi?
2. Script `defer` veya `async` ile yüklenmiyor olmalı

**Doğru:**
```html
<script src="/js/theme-toggle.js"></script>
```

**Yanlış:**
```html
<script src="/js/theme-toggle.js" defer></script>
```

### Renkler doğru uygulanmıyor

**Kontrol edin:**
1. CSS custom properties tanımlı mı?
2. `data-theme` attribute HTML'e uygulanıyor mu?

**DevTools'da kontrol:**
```javascript
document.documentElement.getAttribute('data-theme');
// "dark" veya "light" dönmeli
```

## 🚀 Performans

- **Script boyutu**: 3.7KB (minify edilmemiş)
- **CSS eklentisi**: ~250 satır
- **Geçiş süresi**: 0.3s
- **localStorage okuma**: <1ms
- **Tema değiştirme**: <10ms

## 📊 Tarayıcı Desteği

✅ Chrome 88+
✅ Firefox 85+
✅ Safari 14+
✅ Edge 88+
✅ Opera 74+

**Not:** CSS custom properties desteği gereklidir (IE11 desteklenmez)

## 🔄 Gelecek İyileştirmeler

- [ ] Otomatik gündoğumu/günbatımı modu
- [ ] Renk şeması özelleştirme paneli
- [ ] Daha fazla tema seçeneği (serephia, ocean, forest)
- [ ] Tema önizleme
- [ ] Tema geçiş animasyonları

## 📚 Kaynaklar

- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme)
- [localStorage API](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- [WCAG Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
