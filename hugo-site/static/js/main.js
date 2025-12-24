// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuClose = document.getElementById('mobileMenuClose');

    function closeMobileMenu() {
        mobileMenu.classList.remove('open');
        mobileMenuToggle.classList.remove('open');
        document.body.style.overflow = '';
    }

    function openMobileMenu() {
        mobileMenu.classList.add('open');
        mobileMenuToggle.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    if (mobileMenuToggle && mobileMenu) {
        // Toggle menu
        mobileMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Mobile menu toggle clicked!'); // Debug
            if (mobileMenu.classList.contains('open')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });

        // Close button
        if (mobileMenuClose) {
            mobileMenuClose.addEventListener('click', function(e) {
                e.stopPropagation();
                closeMobileMenu();
            });
        }

        // Close mobile menu when clicking the overlay (outside menu)
        mobileMenu.addEventListener('click', function(e) {
            // Only close if clicking the overlay background, not the nav itself
            if (e.target === mobileMenu) {
                closeMobileMenu();
            }
        });

        // Close menu when clicking a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                closeMobileMenu();
            });
        });

        // Close menu on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
                closeMobileMenu();
            }
        });
    }

    // Back to Top Button
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });

        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Burç Uyumu Hesaplama
function checkCompatibility() {
    const burc1 = document.getElementById('burc1').value;
    const burc2 = document.getElementById('burc2').value;

    if (!burc1 || !burc2) {
        alert('Lütfen her iki burcu da seçiniz.');
        return;
    }

    // Küçükten büyüğe sıralama (URL tutarlılığı için)
    const burclar = [burc1, burc2].sort();
    const url = `/burc-uyumu/${burclar[0]}-${burclar[1]}/`;

    window.location.href = url;
}

// Hero Search - Burç Arama
function searchZodiac() {
    const searchInput = document.getElementById('heroSearch');
    const searchTerm = searchInput.value.trim().toLowerCase();

    if (!searchTerm) {
        alert('Lütfen bir burç adı girin.');
        return;
    }

    // Burç isimleri ve slug'ları
    const zodiacMap = {
        'koç': 'koc-burcu',
        'koc': 'koc-burcu',
        'boğa': 'boga-burcu',
        'boga': 'boga-burcu',
        'ikizler': 'ikizler-burcu',
        'yengeç': 'yengec-burcu',
        'yengec': 'yengec-burcu',
        'aslan': 'aslan-burcu',
        'başak': 'basak-burcu',
        'basak': 'basak-burcu',
        'terazi': 'terazi-burcu',
        'akrep': 'akrep-burcu',
        'yay': 'yay-burcu',
        'oğlak': 'oglak-burcu',
        'oglak': 'oglak-burcu',
        'kova': 'kova-burcu',
        'balık': 'balik-burcu',
        'balik': 'balik-burcu'
    };

    const zodiacSlug = zodiacMap[searchTerm];

    if (zodiacSlug) {
        window.location.href = `/${zodiacSlug}/`;
    } else {
        alert('Burç bulunamadı. Lütfen geçerli bir burç adı girin (örn: Koç, Boğa, İkizler).');
    }
}

// Enter tuşu ile arama
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('heroSearch');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchZodiac();
            }
        });
    }
});

// ================================
// Interactive Zodiac Cards - Task #3
// ================================

document.addEventListener('DOMContentLoaded', function() {
    const zodiacCards = document.querySelectorAll('.zodiac-card');

    zodiacCards.forEach(card => {
        // Parallax effect on mouse move
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-15px) scale(1.03)`;
        });

        // Reset transform on mouse leave
        card.addEventListener('mouseleave', function() {
            card.style.transform = '';
        });

        // Ripple effect on click
        card.addEventListener('click', function(e) {
            // Create ripple element
            const ripple = document.createElement('div');
            ripple.className = 'ripple-effect';
            
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            card.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// ============================================
// ZODIAC DETAIL PAGE ENHANCEMENTS
// ============================================

// Smooth Scroll for Internal Links
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll behavior to all internal links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhance stat cards with sequential reveal animation
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length > 0) {
        statCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }

    // Add progressive reveal for zodiac content sections
    const contentSections = document.querySelectorAll('.zodiac-content h2');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateX(0)';
            }
        });
    }, observerOptions);

    contentSections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateX(-20px)';
        section.style.transition = 'all 0.6s ease-out';
        sectionObserver.observe(section);
    });

    // Enhanced share button interactions
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.pointerEvents = 'none';
            
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - 10;
            const y = e.clientY - rect.top - 10;
            
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.animation = 'ripple-share 0.6s ease-out';
            
            this.style.position = 'relative';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add FAQ accordion functionality
    const faqHeaders = document.querySelectorAll('.zodiac-content h3');
    faqHeaders.forEach(header => {
        // Check if this is in FAQ section
        const prevH2 = header.previousElementSibling;
        let isFAQ = false;
        let el = header.previousElementSibling;
        
        while (el) {
            if (el.tagName === 'H2' && el.textContent.includes('Sık Sorulan Sorular')) {
                isFAQ = true;
                break;
            }
            if (el.tagName === 'H2') {
                break;
            }
            el = el.previousElementSibling;
        }

        if (isFAQ) {
            header.style.cursor = 'pointer';
            header.style.userSelect = 'none';
            header.classList.add('faq-question');
            
            // Add toggle icon
            const icon = document.createElement('span');
            icon.className = 'faq-icon';
            icon.textContent = '▼';
            icon.style.marginLeft = '0.5rem';
            icon.style.fontSize = '0.8em';
            icon.style.transition = 'transform 0.3s ease';
            header.appendChild(icon);

            // Get the answer paragraph
            let answer = header.nextElementSibling;
            if (answer && answer.tagName === 'P') {
                answer.classList.add('faq-answer');
                answer.style.maxHeight = answer.scrollHeight + 'px';
                answer.style.overflow = 'hidden';
                answer.style.transition = 'all 0.3s ease';
                
                // Click handler
                header.addEventListener('click', function() {
                    const isOpen = answer.style.maxHeight !== '0px';
                    
                    if (isOpen) {
                        answer.style.maxHeight = '0px';
                        answer.style.opacity = '0';
                        answer.style.marginBottom = '0';
                        icon.style.transform = 'rotate(-90deg)';
                    } else {
                        answer.style.maxHeight = answer.scrollHeight + 'px';
                        answer.style.opacity = '1';
                        answer.style.marginBottom = '1.25rem';
                        icon.style.transform = 'rotate(0deg)';
                    }
                });
            }
        }
    });
});

// Add CSS animation for share button ripple
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple-share {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .faq-question:hover {
        color: #fbbf24 !important;
    }

    .faq-answer {
        opacity: 1;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
`;
document.head.appendChild(rippleStyle);

