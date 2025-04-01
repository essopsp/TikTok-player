const CACHE_NAME = 'tiktok-player-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
  // Add additional files like your icons if needed
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
