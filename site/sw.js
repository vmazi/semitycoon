// Network-first, cache only as a fallback.
//
// The site is deliberately served with Cache-Control: no-store so that an edit
// is live on the next reload -- there is no build step and no fingerprinting.
// A cache-first worker would fight that and start serving yesterday's build,
// so the network always wins and the cache exists purely for offline play.

const CACHE = 'semitycoon-v1';
const SHELL = ['/', '/icons/icon-192.png', '/icons/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return;
  e.respondWith(
    fetch(r)
      .then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(r, copy));
        }
        return res;
      })
      .catch(() => caches.match(r).then(hit => hit || caches.match('/'))));
});
