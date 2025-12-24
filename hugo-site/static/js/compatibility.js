// ============================================
// BURÇ UYUMU HESAPLAYICI
// ============================================

// Burç veritabanı
const zodiacData = {
    'koc-burcu': { name: 'Koç', element: 'Ateş', slug: 'koc-burcu' },
    'boga-burcu': { name: 'Boğa', element: 'Toprak', slug: 'boga-burcu' },
    'ikizler-burcu': { name: 'İkizler', element: 'Hava', slug: 'ikizler-burcu' },
    'yengec-burcu': { name: 'Yengeç', element: 'Su', slug: 'yengec-burcu' },
    'aslan-burcu': { name: 'Aslan', element: 'Ateş', slug: 'aslan-burcu' },
    'basak-burcu': { name: 'Başak', element: 'Toprak', slug: 'basak-burcu' },
    'terazi-burcu': { name: 'Terazi', element: 'Hava', slug: 'terazi-burcu' },
    'akrep-burcu': { name: 'Akrep', element: 'Su', slug: 'akrep-burcu' },
    'yay-burcu': { name: 'Yay', element: 'Ateş', slug: 'yay-burcu' },
    'oglak-burcu': { name: 'Oğlak', element: 'Toprak', slug: 'oglak-burcu' },
    'kova-burcu': { name: 'Kova', element: 'Hava', slug: 'kova-burcu' },
    'balik-burcu': { name: 'Balık', element: 'Su', slug: 'balik-burcu' }
};

// Element uyum matrisi
const elementCompatibility = {
    'Ateş': {
        'Ateş': 8, 'Hava': 9, 'Toprak': 5, 'Su': 4
    },
    'Toprak': {
        'Toprak': 8, 'Su': 9, 'Ateş': 5, 'Hava': 4
    },
    'Hava': {
        'Hava': 8, 'Ateş': 9, 'Su': 5, 'Toprak': 4
    },
    'Su': {
        'Su': 8, 'Toprak': 9, 'Hava': 5, 'Ateş': 4
    }
};

// Detaylı burç uyum matrisi
const zodiacCompatibilityMatrix = {
    'koc-burcu': {
        'aslan-burcu': 9, 'yay-burcu': 9, 'ikizler-burcu': 8, 'kova-burcu': 8,
        'koc-burcu': 7, 'terazi-burcu': 6, 'basak-burcu': 5, 'boga-burcu': 5,
        'yengec-burcu': 4, 'akrep-burcu': 4, 'oglak-burcu': 5, 'balik-burcu': 5
    },
    'boga-burcu': {
        'basak-burcu': 9, 'oglak-burcu': 9, 'yengec-burcu': 8, 'balik-burcu': 8,
        'boga-burcu': 7, 'akrep-burcu': 6, 'koc-burcu': 5, 'ikizler-burcu': 5,
        'aslan-burcu': 4, 'kova-burcu': 4, 'yay-burcu': 5, 'terazi-burcu': 6
    },
    'ikizler-burcu': {
        'terazi-burcu': 9, 'kova-burcu': 9, 'koc-burcu': 8, 'aslan-burcu': 8,
        'ikizler-burcu': 7, 'yay-burcu': 6, 'boga-burcu': 5, 'yengec-burcu': 5,
        'basak-burcu': 4, 'balik-burcu': 4, 'akrep-burcu': 5, 'oglak-burcu': 5
    },
    'yengec-burcu': {
        'akrep-burcu': 9, 'balik-burcu': 9, 'boga-burcu': 8, 'basak-burcu': 8,
        'yengec-burcu': 7, 'oglak-burcu': 6, 'ikizler-burcu': 5, 'aslan-burcu': 5,
        'koc-burcu': 4, 'terazi-burcu': 4, 'yay-burcu': 5, 'kova-burcu': 5
    },
    'aslan-burcu': {
        'koc-burcu': 9, 'yay-burcu': 9, 'ikizler-burcu': 8, 'terazi-burcu': 8,
        'aslan-burcu': 7, 'kova-burcu': 6, 'boga-burcu': 4, 'akrep-burcu': 4,
        'basak-burcu': 5, 'yengec-burcu': 5, 'oglak-burcu': 5, 'balik-burcu': 5
    },
    'basak-burcu': {
        'boga-burcu': 9, 'oglak-burcu': 9, 'yengec-burcu': 8, 'akrep-burcu': 8,
        'basak-burcu': 7, 'balik-burcu': 6, 'koc-burcu': 5, 'aslan-burcu': 5,
        'ikizler-burcu': 4, 'yay-burcu': 4, 'terazi-burcu': 5, 'kova-burcu': 5
    },
    'terazi-burcu': {
        'ikizler-burcu': 9, 'kova-burcu': 9, 'aslan-burcu': 8, 'yay-burcu': 8,
        'terazi-burcu': 7, 'koc-burcu': 6, 'boga-burcu': 6, 'basak-burcu': 5,
        'yengec-burcu': 4, 'oglak-burcu': 4, 'akrep-burcu': 5, 'balik-burcu': 5
    },
    'akrep-burcu': {
        'yengec-burcu': 9, 'balik-burcu': 9, 'basak-burcu': 8, 'oglak-burcu': 8,
        'akrep-burcu': 7, 'boga-burcu': 6, 'ikizler-burcu': 5, 'terazi-burcu': 5,
        'koc-burcu': 4, 'aslan-burcu': 4, 'yay-burcu': 5, 'kova-burcu': 4
    },
    'yay-burcu': {
        'koc-burcu': 9, 'aslan-burcu': 9, 'terazi-burcu': 8, 'kova-burcu': 8,
        'yay-burcu': 7, 'ikizler-burcu': 6, 'boga-burcu': 5, 'basak-burcu': 4,
        'yengec-burcu': 5, 'akrep-burcu': 5, 'oglak-burcu': 5, 'balik-burcu': 4
    },
    'oglak-burcu': {
        'boga-burcu': 9, 'basak-burcu': 9, 'akrep-burcu': 8, 'balik-burcu': 8,
        'oglak-burcu': 7, 'yengec-burcu': 6, 'koc-burcu': 5, 'ikizler-burcu': 5,
        'aslan-burcu': 5, 'yay-burcu': 5, 'terazi-burcu': 4, 'kova-burcu': 4
    },
    'kova-burcu': {
        'ikizler-burcu': 9, 'terazi-burcu': 9, 'koc-burcu': 8, 'yay-burcu': 8,
        'kova-burcu': 7, 'aslan-burcu': 6, 'boga-burcu': 4, 'yengec-burcu': 5,
        'basak-burcu': 5, 'akrep-burcu': 4, 'oglak-burcu': 4, 'balik-burcu': 5
    },
    'balik-burcu': {
        'yengec-burcu': 9, 'akrep-burcu': 9, 'boga-burcu': 8, 'oglak-burcu': 8,
        'balik-burcu': 7, 'basak-burcu': 6, 'koc-burcu': 5, 'ikizler-burcu': 4,
        'aslan-burcu': 5, 'terazi-burcu': 5, 'yay-burcu': 4, 'kova-burcu': 5
    }
};

// Uyum açıklamaları
const compatibilityDescriptions = {
    9: "Mükemmel bir uyum! Bu iki burç birbirini çok iyi tamamlıyor. Güçlü bir bağ kurabilirler.",
    8: "Harika bir uyum! Aralarında doğal bir çekim ve anlayış var. Başarılı bir ilişki kurabilirler.",
    7: "İyi bir uyum! Birbirlerini anlamak için çaba gösterdiklerinde güzel bir ilişki kurabilirler.",
    6: "Orta düzey uyum. Bazı zorluklarla karşılaşabilirler ama karşılıklı anlayışla aşabilirler.",
    5: "Karışık bir uyum. İlişkide dengeyi bulmak için çaba gerekir. Farklılıklar zenginlik katabilir.",
    4: "Zor bir uyum. Önemli farklılıklar var. Başarılı olmak için çok çaba ve anlayış gerekir.",
    3: "Çok zor bir uyum. Temel değerler farklı olabilir. Uzun vadede zorluklar yaşanabilir."
};

function calculateCompatibility() {
    const burc1Select = document.getElementById('burc1');
    const burc2Select = document.getElementById('burc2');

    const burc1 = burc1Select.value;
    const burc2 = burc2Select.value;

    if (!burc1 || !burc2) {
        alert('Lütfen her iki burcu da seçiniz!');
        return;
    }

    if (burc1 === burc2) {
        alert('Aynı burcu seçtiniz! Farklı iki burç seçiniz.');
        return;
    }

    const data1 = zodiacData[burc1];
    const data2 = zodiacData[burc2];

    // Genel uyum puanı hesapla
    const overallScore = zodiacCompatibilityMatrix[burc1][burc2];

    // Kategori puanları hesapla (element uyumuna göre varyasyonlar)
    const elementScore = elementCompatibility[data1.element][data2.element];

    const loveScore = Math.min(10, Math.round(overallScore * 1.1));
    const friendshipScore = Math.min(10, Math.round((overallScore + elementScore) / 2));
    const workScore = Math.min(10, Math.round(elementScore * 0.9));

    // Sonuçları göster
    displayResults(data1.name, data2.name, overallScore, loveScore, friendshipScore, workScore, burc1, burc2);
}

function displayResults(name1, name2, overall, love, friendship, work, slug1, slug2) {
    const resultDiv = document.getElementById('compatibilityResult');
    const resultTitle = document.getElementById('resultTitle');
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreCircle = document.getElementById('scoreCircle');

    const loveScore = document.getElementById('loveScore');
    const friendshipScore = document.getElementById('friendshipScore');
    const workScore = document.getElementById('workScore');

    const loveFill = document.getElementById('loveFill');
    const friendshipFill = document.getElementById('friendshipFill');
    const workFill = document.getElementById('workFill');

    const resultDescription = document.getElementById('resultDescription');
    const detailLink = document.getElementById('detailLink');

    // Başlık
    resultTitle.textContent = name1 + ' & ' + name2;

    // Ana puan
    scoreNumber.textContent = overall;

    // SVG gradient oluştur (eğer yoksa)
    if (!document.getElementById('scoreGradient')) {
        const svg = document.querySelector('.score-svg');
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'scoreGradient');
        gradient.innerHTML = '<stop offset="0%" stop-color="#f59e0b" /><stop offset="100%" stop-color="#fbbf24" />';
        defs.appendChild(gradient);
        svg.insertBefore(defs, svg.firstChild);
    }

    // Dairesel progress animasyonu
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (overall / 10) * circumference;

    setTimeout(function() {
        scoreCircle.style.strokeDashoffset = offset;
    }, 100);

    // Kategori puanları ve bar animasyonları
    loveScore.textContent = love + '/10';
    friendshipScore.textContent = friendship + '/10';
    workScore.textContent = work + '/10';

    setTimeout(function() {
        loveFill.style.width = ((love / 10) * 100) + '%';
        friendshipFill.style.width = ((friendship / 10) * 100) + '%';
        workFill.style.width = ((work / 10) * 100) + '%';
    }, 300);

    // Açıklama
    resultDescription.textContent = compatibilityDescriptions[overall] || compatibilityDescriptions[5];

    // Detay linki
    const sortedSlugs = [slug1, slug2].sort();
    const detailSlug = sortedSlugs[0].replace('-burcu', '') + '-' + sortedSlugs[1].replace('-burcu', '');
    detailLink.href = '/burc-uyumu/' + detailSlug + '/';

    // Sonucu göster
    resultDiv.style.display = 'block';

    // Smooth scroll
    setTimeout(function() {
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}
