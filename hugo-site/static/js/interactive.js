// ============================================
// INTERACTIVE ELEMENTS
// ============================================

// Reading Progress Bar
function initReadingProgress() {
    // Create progress bar if on article page
    if (document.querySelector('.article-content, .zodiac-content')) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        document.body.prepend(progressBar);

        window.addEventListener('scroll', function() {
            const winHeight = window.innerHeight;
            const docHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollPercent = (scrollTop / (docHeight - winHeight)) * 100;

            progressBar.style.width = Math.min(scrollPercent, 100) + '%';
        });
    }
}

// Star Rating Component
function createStarRating(container, rating, maxStars = 10) {
    if (!container) return;

    container.className = 'star-rating';
    container.innerHTML = '';

    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < maxStars; i++) {
        const star = document.createElement('span');
        star.className = 'star';
        star.textContent = '⭐';

        if (i < fullStars) {
            star.classList.add('filled');
        } else if (i === fullStars && hasHalfStar) {
            star.classList.add('half-filled');
        }

        container.appendChild(star);
    }
}

// Interactive Star Rating (clickable)
function initInteractiveStarRating(container, callback) {
    if (!container) return;

    container.classList.add('interactive');
    const stars = container.querySelectorAll('.star');

    stars.forEach(function(star, index) {
        star.addEventListener('click', function() {
            const rating = index + 1;

            // Update visual
            stars.forEach(function(s, i) {
                if (i < rating) {
                    s.classList.add('filled');
                } else {
                    s.classList.remove('filled');
                }
            });

            // Callback
            if (callback) callback(rating);
        });

        star.addEventListener('mouseenter', function() {
            stars.forEach(function(s, i) {
                if (i <= index) {
                    s.style.color = '#fbbf24';
                }
            });
        });

        star.addEventListener('mouseleave', function() {
            stars.forEach(function(s) {
                if (!s.classList.contains('filled')) {
                    s.style.color = '#4b5563';
                }
            });
        });
    });
}

// Tooltip System
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(function(el) {
        const wrapper = document.createElement('div');
        wrapper.className = 'tooltip-wrapper';
        el.parentNode.insertBefore(wrapper, el);
        wrapper.appendChild(el);

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = el.getAttribute('data-tooltip');
        wrapper.appendChild(tooltip);
    });
}

// Loading Overlay
function showLoading(text) {
    let overlay = document.getElementById('loadingOverlay');

    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="loading-content"><div class="loading-spinner"></div><div class="loading-text">' + (text || 'Yükleniyor...') + '</div></div>';
        document.body.appendChild(overlay);
    }

    setTimeout(function() {
        overlay.classList.add('active');
    }, 10);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
        setTimeout(function() {
            overlay.remove();
        }, 300);
    }
}

// Animated Counter
function animateCounter(element, target, duration) {
    if (!element) return;

    const start = parseInt(element.textContent) || 0;
    const range = target - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(function() {
        current += increment;
        if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

// Counter Observer (animate when visible)
function initCounterObserver() {
    const counters = document.querySelectorAll('.counter');

    if (counters.length === 0) return;

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const target = parseInt(entry.target.dataset.target) || 0;
                const duration = parseInt(entry.target.dataset.duration) || 2000;

                entry.target.dataset.animated = 'true';
                animateCounter(entry.target, target, duration);
            }
        });
    }, {
        threshold: 0.5
    });

    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

// Enhanced Back to Top Button
function initBackToTop() {
    let backToTop = document.getElementById('backToTop');

    if (!backToTop) {
        backToTop = document.createElement('button');
        backToTop.id = 'backToTop';
        backToTop.className = 'back-to-top';
        backToTop.innerHTML = '↑';
        backToTop.setAttribute('aria-label', 'Yukarı Çık');
        document.body.appendChild(backToTop);
    }

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
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

// Progress Bar Component
function updateProgressBar(element, value, max) {
    if (!element) return;

    const container = element.closest('.progress-bar-container');
    if (!container) return;

    const percentage = Math.min((value / max) * 100, 100);
    element.style.width = percentage + '%';

    const valueElement = container.querySelector('.progress-value');
    if (valueElement) {
        valueElement.textContent = Math.round(percentage) + '%';
    }
}

// Animated Progress Bars
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');

    if (progressBars.length === 0) return;

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const value = parseInt(entry.target.dataset.value) || 0;
                const max = parseInt(entry.target.dataset.max) || 100;

                entry.target.dataset.animated = 'true';
                setTimeout(function() {
                    updateProgressBar(entry.target, value, max);
                }, 100);
            }
        });
    }, {
        threshold: 0.5
    });

    progressBars.forEach(function(bar) {
        observer.observe(bar);
    });
}

// Toast Notification
function showToast(message, type, duration) {
    type = type || 'info';
    duration = duration || 3000;

    const toast = document.createElement('div');
    toast.className = 'toast ' + type;

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };

    toast.innerHTML = '<div class="toast-content"><div class="toast-icon">' + (icons[type] || icons.info) + '</div><div class="toast-message"><div class="toast-title">' + (type.charAt(0).toUpperCase() + type.slice(1)) + '</div><div class="toast-text">' + message + '</div></div></div>';

    document.body.appendChild(toast);

    setTimeout(function() {
        toast.classList.add('show');
    }, 10);

    setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() {
            toast.remove();
        }, 400);
    }, duration);
}

// Add pulse effect to element
function addPulse(element) {
    if (!element) return;
    element.classList.add('pulse');
    setTimeout(function() {
        element.classList.remove('pulse');
    }, 2000);
}

// Add shake effect to element
function addShake(element) {
    if (!element) return;
    element.classList.add('shake');
    setTimeout(function() {
        element.classList.remove('shake');
    }, 500);
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', function() {
    initReadingProgress();
    initTooltips();
    initBackToTop();
    initCounterObserver();
    initProgressBars();

    console.log('Interactive elements initialized');
});

// Export functions for global use
window.Interactive = {
    createStarRating: createStarRating,
    initInteractiveStarRating: initInteractiveStarRating,
    showLoading: showLoading,
    hideLoading: hideLoading,
    animateCounter: animateCounter,
    updateProgressBar: updateProgressBar,
    showToast: showToast,
    addPulse: addPulse,
    addShake: addShake
};
