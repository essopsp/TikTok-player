// service-worker.js - Enhanced for better PWA performance

const CACHE_NAME = 'tiktok-player-cache-v1';
const ASSETS_CACHE_NAME = 'tiktok-player-assets-v1';
const OFFLINE_URL = '/index.html';

// Resources to pre-cache
const APP_SHELL_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-72x72.png',
  '/icons/icon-96x96.png',
  '/icons/icon-128x128.png',
  '/icons/icon-144x144.png',
  '/icons/icon-152x152.png',
  '/icons/icon-192x192.png',
  '/icons/icon-384x384.png',
  '/icons/icon-512x512.png',
  'https://fonts.googleapis.com/icon?family=Material+Icons'
];

// Install event - Cache app shell assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing Service Worker', event);
  
  // Skip waiting to ensure the new service worker activates immediately
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(ASSETS_CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching App Shell Assets');
        return cache.addAll(APP_SHELL_ASSETS);
      })
      .catch(error => {
        console.error('[Service Worker] Pre-caching failed:', error);
      })
  );
});

// Activate event - Clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating Service Worker', event);
  
  // Claim clients to ensure the service worker takes control immediately
  event.waitUntil(self.clients.claim());
  
  // Remove old caches
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.filter(cacheName => {
            return cacheName !== CACHE_NAME && cacheName !== ASSETS_CACHE_NAME;
          }).map(cacheName => {
            console.log('[Service Worker] Removing old cache:', cacheName);
            return caches.delete(cacheName);
          })
        );
      })
  );
});

// Helper function to determine if request is for an API or external resource
const isApiRequest = (url) => {
  return url.includes('tiktok.com') || 
         url.includes('api.') || 
         url.includes('/api/');
};

// Fetch event - Network-first strategy for API requests, Cache-first for assets
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // Handle different fetch strategies based on the request type
  if (isApiRequest(event.request.url)) {
    // For API requests, use network-first strategy
    event.respondWith(networkFirstStrategy(event.request));
  } else {
    // For static assets and HTML, use cache-first strategy
    event.respondWith(cacheFirstStrategy(event.request));
  }
});

// Network-first strategy for dynamic content
async function networkFirstStrategy(request) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    // If successful, clone and cache the response
    if (networkResponse && networkResponse.ok) {
      const responseClone = networkResponse.clone();
      
      caches.open(CACHE_NAME)
        .then(cache => {
          cache.put(request, responseClone);
        });
      
      return networkResponse;
    }
  } catch (error) {
    console.log('[Service Worker] Network request failed, trying cache', error);
  }
  
  // If network fails, try the cache
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // If no cache for specific request, return the offline page for navigation requests
  if (request.mode === 'navigate') {
    return caches.match(OFFLINE_URL);
  }
  
  // Otherwise, return a fallback response
  return new Response('Network error happened', {
    status: 408,
    headers: { 'Content-Type': 'text/plain' }
  });
}

// Cache-first strategy for static assets
async function cacheFirstStrategy(request) {
  // Try cache first
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  // If not in cache, try network
  try {
    const networkResponse = await fetch(request);
    
    // If successful, clone and cache the response
    if (networkResponse && networkResponse.ok) {
      const responseClone = networkResponse.clone();
      
      caches.open(ASSETS_CACHE_NAME)
        .then(cache => {
          cache.put(request, responseClone);
        });
      
      return networkResponse;
    }
  } catch (error) {
    console.log('[Service Worker] Failed to fetch from network:', error);
    
    // If request is for a page, return offline page
    if (request.mode === 'navigate') {
      return caches.match(OFFLINE_URL);
    }
  }
  
  // If all else fails, return a simple response
  return new Response('Resource not available offline', {
    status: 404,
    headers: { 'Content-Type': 'text/plain' }
  });
}

// Background sync for pending operations
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Background Sync', event);
  if (event.tag === 'sync-tiktok-data') {
    event.waitUntil(syncTikTokData());
  }
});

// Function to sync data when online
async function syncTikTokData() {
  // Here you would implement any data synchronization needed
  // when the device comes back online
  console.log('[Service Worker] Syncing TikTok data');
}

// Push notification handler
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Push Received', event);
  
  let title = 'TikTok Player';
  let options = {
    body: 'New content available!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-96x96.png'
  };
  
  if (event.data) {
    const data = event.data.json();
    title = data.title || title;
    options.body = data.body || options.body;
  }
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] Notification click', event);
  
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({ type: 'window' })
      .then(windowClients => {
        // If a window client is already open, focus it
        for (const client of windowClients) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        // Otherwise open a new window
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
  );
});
