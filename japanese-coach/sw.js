// Service Worker for Japanese Coach - Offline Support
const CACHE_NAME = 'jcoach-v1';
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

// Fetch: serve from cache, fallback to network
self.addEventListener('fetch', event => {
    // Only handle same-origin and GitHub Pages requests, not GitHub API
    const url = new URL(event.request.url);
    if (url.hostname === 'api.github.com' || url.hostname === 'api.openai.com') {
        // AI and sync calls — always go to network, don't cache
        return;
    }

    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            // Not in cache — try network and cache the result
            return fetch(event.request).then(response => {
                if (response && response.status === 200 && response.type !== 'opaque') {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            }).catch(() => {
                // Network failed and not cached — return offline fallback for HTML
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
