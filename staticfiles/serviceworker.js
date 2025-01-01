const CACHE_NAME = 'webmap-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/styles.css',  // Update with your actual CSS path
    '/static/js/scripts.js',   // Update with your actual JS path
    '/static/images/icons/icon-192x192.png', // Add all icons and assets needed for offline use
    '/static/images/icons/icon-512x512.png',
    //'/base.html',             // Example if you want to cache index.html
    // Add other URLs for assets that need to be available offline
    '/myapp/templates/base.html',             // Example if you want to cache index.html
    '/myapp/templates/login.html',             // Example if you want to cache index.html
    '/myapp/templates/register.html',             // Example if you want to cache index.html
    '/myapp/templates/profile.html',             // Example if you want to cache index.html




];



// Install event: caches necessary resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching essential resources');
                return cache.addAll(urlsToCache);  // Cache essential resources
            })
    );
});

// Activate event: Clean up old caches
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];  // Only keep the current cache

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        console.log('Service Worker: Deleting old cache', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch event: Serve cached content when offline or fetch new content if available
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            // Return cached response if available, otherwise fetch it
            return cachedResponse || fetch(event.request).then(freshResponse => {
                // Optionally, cache new content on the fly
                return caches.open(CACHE_NAME).then(cache => {
                    cache.put(event.request, freshResponse.clone());
                    return freshResponse;
                });
            });
        })
    );
});
