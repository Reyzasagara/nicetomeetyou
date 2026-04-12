// Service Worker for Japanese Coach - Offline Support
const CACHE_NAME = 'jcoach-v3';
const ASSETS = [
    './',
    './index.html',
    './style.css',
    './app.js',
    './kana.js',
    './mnemonics.js',
    './phrases.js',
];

// Install: cache all assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

// Activate: remove old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// Fetch: network-first for app files, cache as fallback for offline
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);
    if (url.hostname === 'api.github.com' || url.hostname === 'api.openai.com') {
        return;
    }

    event.respondWith(
        fetch(event.request).then(response => {
            // Got network response — update cache and return
            if (response && response.status === 200 && response.type !== 'opaque') {
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
            }
            return response;
        }).catch(() => {
            // Network failed — serve from cache (offline mode)
            return caches.match(event.request).then(cached => {
                if (cached) return cached;
                if (event.request.mode === 'navigate') {
                    return caches.match('./index.html');
                }
            });
        })
    );
});

// Listen for message to skip waiting (for update flow)
self.addEventListener('message', event => {
    if (event.data === 'skipWaiting') self.skipWaiting();
});
