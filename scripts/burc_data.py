"""
Burç veritabanı - Tüm burç bilgileri
"""

BURCLAR = {
    'koc': {
        'ad': 'Koç',
        'slug': 'koc-burcu',
        'tarih': '21 Mart - 20 Nisan',
        'element': 'Ateş',
        'nitelik': 'Öncü',
        'gezegen': 'Mars',
        'sans_gunu': 'Salı',
        'sans_sayilari': [1, 9, 19, 27],
        'sans_renkleri': ['Kırmızı', 'Turuncu'],
        'uyumlu_burclar': ['Aslan', 'Yay', 'İkizler'],
        'uyumsuz_burclar': ['Yengeç', 'Terazi'],
        'sans_taslari': ['Elmas', 'Ametist', 'Akik']
    },
    'boga': {
        'ad': 'Boğa',
        'slug': 'boga-burcu',
        'tarih': '21 Nisan - 21 Mayıs',
        'element': 'Toprak',
        'nitelik': 'Sabit',
        'gezegen': 'Venüs',
        'sans_gunu': 'Cuma',
        'sans_sayilari': [2, 6, 15, 24],
        'sans_renkleri': ['Yeşil', 'Pembe'],
        'uyumlu_burclar': ['Başak', 'Oğlak', 'Yengeç'],
        'uyumsuz_burclar': ['Aslan', 'Akrep'],
        'sans_taslari': ['Zümrüt', 'Yeşim', 'Safir']
    },
    'ikizler': {
        'ad': 'İkizler',
        'slug': 'ikizler-burcu',
        'tarih': '22 Mayıs - 21 Haziran',
        'element': 'Hava',
        'nitelik': 'Değişken',
        'gezegen': 'Merkür',
        'sans_gunu': 'Çarşamba',
        'sans_sayilari': [5, 14, 23, 32],
        'sans_renkleri': ['Sarı', 'Turuncu'],
        'uyumlu_burclar': ['Terazi', 'Kova', 'Koç'],
        'uyumsuz_burclar': ['Başak', 'Yay'],
        'sans_taslari': ['Akik', 'Sitrin', 'Kehribar']
    },
    'yengec': {
        'ad': 'Yengeç',
        'slug': 'yengec-burcu',
        'tarih': '22 Haziran - 22 Temmuz',
        'element': 'Su',
        'nitelik': 'Öncü',
        'gezegen': 'Ay',
        'sans_gunu': 'Pazartesi',
        'sans_sayilari': [2, 7, 11, 16],
        'sans_renkleri': ['Beyaz', 'Gümüş', 'Krem'],
        'uyumlu_burclar': ['Akrep', 'Balık', 'Boğa'],
        'uyumsuz_burclar': ['Koç', 'Terazi'],
        'sans_taslari': ['İnci', 'Ay Taşı', 'Sedef']
    },
    'aslan': {
        'ad': 'Aslan',
        'slug': 'aslan-burcu',
        'tarih': '23 Temmuz - 22 Ağustos',
        'element': 'Ateş',
        'nitelik': 'Sabit',
        'gezegen': 'Güneş',
        'sans_gunu': 'Pazar',
        'sans_sayilari': [1, 4, 10, 19],
        'sans_renkleri': ['Altın', 'Turuncu', 'Sarı'],
        'uyumlu_burclar': ['Koç', 'Yay', 'İkizler'],
        'uyumsuz_burclar': ['Boğa', 'Akrep'],
        'sans_taslari': ['Yakut', 'Kehribar', 'Sardoniks']
    },
    'basak': {
        'ad': 'Başak',
        'slug': 'basak-burcu',
        'tarih': '23 Ağustos - 22 Eylül',
        'element': 'Toprak',
        'nitelik': 'Değişken',
        'gezegen': 'Merkür',
        'sans_gunu': 'Çarşamba',
        'sans_sayilari': [5, 14, 23, 32],
        'sans_renkleri': ['Kahverengi', 'Bej', 'Yeşil'],
        'uyumlu_burclar': ['Boğa', 'Oğlak', 'Yengeç'],
        'uyumsuz_burclar': ['İkizler', 'Yay'],
        'sans_taslari': ['Sardoinks', 'Kuvars', 'Yeşim']
    },
    'terazi': {
        'ad': 'Terazi',
        'slug': 'terazi-burcu',
        'tarih': '23 Eylül - 22 Ekim',
        'element': 'Hava',
        'nitelik': 'Öncü',
        'gezegen': 'Venüs',
        'sans_gunu': 'Cuma',
        'sans_sayilari': [6, 15, 24, 33],
        'sans_renkleri': ['Pembe', 'Mavi', 'Yeşil'],
        'uyumlu_burclar': ['İkizler', 'Kova', 'Aslan'],
        'uyumsuz_burclar': ['Yengeç', 'Oğlak'],
        'sans_taslari': ['Opal', 'Lapis Lazuli', 'Kuvars']
    },
    'akrep': {
        'ad': 'Akrep',
        'slug': 'akrep-burcu',
        'tarih': '23 Ekim - 21 Kasım',
        'element': 'Su',
        'nitelik': 'Sabit',
        'gezegen': 'Plüton',
        'sans_gunu': 'Salı',
        'sans_sayilari': [9, 18, 27, 36],
        'sans_renkleri': ['Bordo', 'Siyah', 'Kırmızı'],
        'uyumlu_burclar': ['Yengeç', 'Balık', 'Oğlak'],
        'uyumsuz_burclar': ['Aslan', 'Kova'],
        'sans_taslari': ['Akik', 'Topaz', 'Obsidyen']
    },
    'yay': {
        'ad': 'Yay',
        'slug': 'yay-burcu',
        'tarih': '22 Kasım - 21 Aralık',
        'element': 'Ateş',
        'nitelik': 'Değişken',
        'gezegen': 'Jüpiter',
        'sans_gunu': 'Perşembe',
        'sans_sayilari': [3, 12, 21, 30],
        'sans_renkleri': ['Mor', 'Mavi', 'Turuncu'],
        'uyumlu_burclar': ['Koç', 'Aslan', 'Kova'],
        'uyumsuz_burclar': ['Başak', 'Balık'],
        'sans_taslari': ['Turkuaz', 'Ametist', 'Topaz']
    },
    'oglak': {
        'ad': 'Oğlak',
        'slug': 'oglak-burcu',
        'tarih': '22 Aralık - 20 Ocak',
        'element': 'Toprak',
        'nitelik': 'Öncü',
        'gezegen': 'Satürn',
        'sans_gunu': 'Cumartesi',
        'sans_sayilari': [8, 17, 26, 35],
        'sans_renkleri': ['Siyah', 'Gri', 'Kahverengi'],
        'uyumlu_burclar': ['Boğa', 'Başak', 'Akrep'],
        'uyumsuz_burclar': ['Terazi', 'Koç'],
        'sans_taslari': ['Garnet', 'Oniks', 'Kuvars']
    },
    'kova': {
        'ad': 'Kova',
        'slug': 'kova-burcu',
        'tarih': '21 Ocak - 18 Şubat',
        'element': 'Hava',
        'nitelik': 'Sabit',
        'gezegen': 'Uranüs',
        'sans_gunu': 'Cumartesi',
        'sans_sayilari': [4, 13, 22, 31],
        'sans_renkleri': ['Mavi', 'Gümüş', 'Mor'],
        'uyumlu_burclar': ['İkizler', 'Terazi', 'Yay'],
        'uyumsuz_burclar': ['Boğa', 'Akrep'],
        'sans_taslari': ['Ametist', 'Akuamarin', 'Safir']
    },
    'balik': {
        'ad': 'Balık',
        'slug': 'balik-burcu',
        'tarih': '19 Şubat - 20 Mart',
        'element': 'Su',
        'nitelik': 'Değişken',
        'gezegen': 'Neptün',
        'sans_gunu': 'Perşembe',
        'sans_sayilari': [3, 7, 12, 16],
        'sans_renkleri': ['Deniz Mavisi', 'Turkuaz', 'Mor'],
        'uyumlu_burclar': ['Yengeç', 'Akrep', 'Boğa'],
        'uyumsuz_burclar': ['İkizler', 'Yay'],
        'sans_taslari': ['Akuamarin', 'Ametist', 'İnci']
    }
}

def get_burc(key):
    """Belirli bir burç bilgisini getir"""
    return BURCLAR.get(key)

def get_all_burclar():
    """Tüm burçları getir"""
    return BURCLAR

def get_burc_by_slug(slug):
    """Slug'a göre burç bul"""
    for key, burc in BURCLAR.items():
        if burc['slug'] == slug:
            return burc
    return None
