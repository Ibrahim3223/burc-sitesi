/**
 * Lazy Loading System
 * Uses Intersection Observer for performance
 */

(function() {
    'use strict';

    // Configuration
    const config = {
        rootMargin: '50px 0px',
        threshold: 0.01
    };

    // Check for Intersection Observer support
    if (!('IntersectionObserver' in window)) {
        console.warn('IntersectionObserver not supported, loading all images immediately');
        loadAllImages();
        return;
    }

    // Initialize lazy loading
    function initLazyLoad() {
        const lazyImages = document.querySelectorAll('img[data-src], img[loading="lazy"]');
        const lazyBackgrounds = document.querySelectorAll('[data-bg]');
        const lazyIframes = document.querySelectorAll('iframe[data-src]');

        if (lazyImages.length > 0) {
            lazyLoadImages(lazyImages);
        }

        if (lazyBackgrounds.length > 0) {
            lazyLoadBackgrounds(lazyBackgrounds);
        }

        if (lazyIframes.length > 0) {
            lazyLoadIframes(lazyIframes);
        }
    }

    // Lazy load images
    function lazyLoadImages(images) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Load image
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    if (img.dataset.srcset) {
                        img.srcset = img.dataset.srcset;
                        img.removeAttribute('data-srcset');
                    }

                    // Add loaded class
                    img.classList.add('lazy-loaded');
                    
                    // Stop observing
                    observer.unobserve(img);
                }
            });
        }, config);

        images.forEach(img => imageObserver.observe(img));
    }

    // Lazy load background images
    function lazyLoadBackgrounds(elements) {
        const bgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.style.backgroundImage = `url('${element.dataset.bg}')`;
                    element.removeAttribute('data-bg');
                    element.classList.add('lazy-loaded');
                    observer.unobserve(element);
                }
            });
        }, config);

        elements.forEach(el => bgObserver.observe(el));
    }

    // Lazy load iframes (for videos, embeds)
    function lazyLoadIframes(iframes) {
        const iframeObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const iframe = entry.target;
                    iframe.src = iframe.dataset.src;
                    iframe.removeAttribute('data-src');
                    iframe.classList.add('lazy-loaded');
                    observer.unobserve(iframe);
                }
            });
        }, config);

        iframes.forEach(iframe => iframeObserver.observe(iframe));
    }

    // Fallback: load all images immediately
    function loadAllImages() {
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            }
            if (img.dataset.srcset) {
                img.srcset = img.dataset.srcset;
                img.removeAttribute('data-srcset');
            }
        });

        const backgrounds = document.querySelectorAll('[data-bg]');
        backgrounds.forEach(el => {
            el.style.backgroundImage = `url('${el.dataset.bg}')`;
            el.removeAttribute('data-bg');
        });

        const iframes = document.querySelectorAll('iframe[data-src]');
        iframes.forEach(iframe => {
            iframe.src = iframe.dataset.src;
            iframe.removeAttribute('data-src');
        });
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLazyLoad);
    } else {
        initLazyLoad();
    }

    // Export for external use
    window.LazyLoad = {
        init: initLazyLoad,
        loadAll: loadAllImages
    };
})();
