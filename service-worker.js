const CACHE_NAME = 'nautilus-v482-core';
const RUNTIME_CACHE = 'nautilus-v482-runtime';
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

async function fallbackHtml(){
  return (await caches.match('./app.html')) || (await caches.match('./index.html')) || new Response('<!doctype html><meta charset="utf-8"><meta name="theme-color" content="#012544"><style>html,body{margin:0;min-height:100%;background:linear-gradient(180deg,#031522,#031b2f);color:#fff;font-family:Arial,Helvetica,sans-serif;display:flex;align-items:center;justify-content:center;text-align:center}.box{padding:24px}</style><title>Nautilus offline</title><body><div class="box"><h1>Nautilus</h1><p>App offline indisponível. Abra uma vez com internet para restaurar o cache.</p></div></body>', {headers:{'Content-Type':'text/html; charset=utf-8'}});
}

async function networkFirstHtml(request){
  try{
    const response = await fetch(new Request(request, {cache:'reload'}));
    if(response && response.ok){
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone()).catch(()=>{});
    }
    return response;
  }catch(e){
    return (await caches.match(request)) || await fallbackHtml();
  }
}

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
    return new Response('', {status:504, statusText:'Offline'});
  }
}

self.addEventListener('fetch', event => {
  if(event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if(url.origin !== self.location.origin) return;
  if(event.request.mode === 'navigate' || (event.request.headers.get('accept')||'').includes('text/html')){
    event.respondWith(networkFirstHtml(event.request));
    return;
  }
  event.respondWith(cacheFirst(event.request));
});

// v482-logo-fixa-sem-tremida
