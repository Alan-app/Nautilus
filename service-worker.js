const CACHE_NAME = 'nautilus-v360-core';
const RUNTIME_CACHE = 'nautilus-v360-runtime';
const APP_ASSETS = [
  './',
  './index.html',
  './app.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './app_documento_oficial_impressao_direta_forcada.html'
];

async function precacheCore(){
  const cache = await caches.open(CACHE_NAME);
  await Promise.all(APP_ASSETS.map(async url => {
    try{
      const req = new Request(url, {cache:'reload'});
      const res = await fetch(req);
      if(res && (res.ok || res.type === 'opaque')) await cache.put(url, res.clone());
    }catch(e){
      try{ await cache.add(url); }catch(_e){}
    }
  }));
}

self.addEventListener('install', event => {
  event.waitUntil(precacheCore());
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil((async()=>{
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => ![CACHE_NAME, RUNTIME_CACHE].includes(k)).map(k => caches.delete(k)));
    await precacheCore();
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  if(event.data && event.data.type === 'PRECACHE_CORE') event.waitUntil(precacheCore());
});

async function cacheFirst(request){
  const cached = await caches.match(request);
  if(cached) return cached;
  try{
    const response = await fetch(request);
    if(response && response.ok && new URL(request.url).origin === self.location.origin){
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, response.clone()).catch(()=>{});
    }
    return response;
  }catch(e){
    if(request.mode === 'navigate' || (request.headers.get('accept')||'').includes('text/html')){
      return (await caches.match('./app.html')) || (await caches.match('./index.html')) || new Response('<!doctype html><meta charset="utf-8"><title>Nautilus offline</title><body><h1>Nautilus</h1><p>App offline indisponível. Abra uma vez com internet para restaurar o cache.</p></body>', {headers:{'Content-Type':'text/html; charset=utf-8'}});
    }
    return new Response('', {status:504, statusText:'Offline'});
  }
}

self.addEventListener('fetch', event => {
  if(event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if(url.origin !== self.location.origin) return;
  event.respondWith(cacheFirst(event.request));
});

// v360-lds-share-nativo
