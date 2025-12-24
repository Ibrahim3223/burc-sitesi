/**
 * Service Worker - Offline Support & Caching
 * Version: 1.0.0
 */

const CACHE_NAME = 'burc-sozlugu-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache on install
const PRECACHE_URLS = [
    '/',
    '/css/style.css',
    '/js/theme-toggle.js',
    '/js/lazy-load.js',
    '/js/main.js',
    '/js/compatibility.js',
    '/js/interactive.js',
    OFFLINE_URL
];

// Install event - precache essential assets
self.addEventListener('install', event => {
    console.log('[SW] Installing service worker...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW] Precaching assets');
                return cache.addAll(PRECACHE_URLS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('[SW] Activating service worker...');
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') return;

    // Skip cross-origin requests
    if (!event.request.url.startsWith(self.location.origin)) return;

    event.respondWith(
        caches.match(event.request)
            .then(cachedResponse => {
                // Return cached response if found
                if (cachedResponse) {
                    return cachedResponse;
                }

                // Clone request for caching
                const fetchRequest = event.request.clone();

                return fetch(fetchRequest).then(response => {
                    // Check if valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    // Clone response for caching
                    const responseToCache = response.clone();

                    // Cache response
                    caches.open(CACHE_NAME).then(cache => {
                        // Only cache HTML, CSS, JS, images
                        if (shouldCache(event.request.url)) {
                            cache.put(event.request, responseToCache);
                        }
                    });

                    return response;
                }).catch(error => {
                    console.log('[SW] Fetch failed, returning offline page', error);
                    
                    // Return offline page for HTML requests
                    if (event.request.headers.get('accept').includes('text/html')) {
                        return caches.match(OFFLINE_URL);
                    }
                });
            })
    );
});

// Helper: Check if URL should be cached
function shouldCache(url) {
    // Cache HTML, CSS, JS, images, fonts
    return url.endsWith('.html') ||
           url.endsWith('.css') ||
           url.endsWith('.js') ||
           url.endsWith('.jpg') ||
           url.endsWith('.jpeg') ||
           url.endsWith('.png') ||
           url.endsWith('.gif') ||
           url.endsWith('.svg') ||
           url.endsWith('.webp') ||
           url.endsWith('.woff') ||
           url.endsWith('.woff2') ||
           url.endsWith('.ttf') ||
           url.endsWith('/') ||
           !url.includes('.');
}

// Message handler
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CACHE_URLS') {
        event.waitUntil(
            caches.open(CACHE_NAME).then(cache => {
                return cache.addAll(event.data.urls);
            })
        );
    }
});
