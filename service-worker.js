const CACHE_NAME = 'livro-historico-fixed-js-and-sigla-20260327-1';
const APP_ASSETS = ['./','./index.html','./app.html','./manifest.webmanifest','./icon-192.png','./icon-512.png'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))));
  self.clients.claim();
});
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      const cloned = response.clone();
      if (event.request.url.startsWith(self.location.origin)) caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
      return response;
    }).catch(() => caches.match('./index.html')))
  );
});
