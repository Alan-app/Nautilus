const METADRIVER_CACHE_VERSION = "metadriver-cache-v52";
self.addEventListener("install", (event) => { self.skipWaiting(); });
self.addEventListener("activate", (event) => {
  event.waitUntil((async()=>{
    try{ const keys = await caches.keys(); await Promise.all(keys.filter(k => k.indexOf("metadriver-") === 0 && k !== "metadriver-" + METADRIVER_CACHE_VERSION).map(k => caches.delete(k))); }catch(e){}
    await self.clients.claim();
  })());
});
self.addEventListener("fetch", (event) => { /* sem cache forçado: evita HTML/JS antigo preso no PWA */ });
