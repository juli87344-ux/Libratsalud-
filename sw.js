const LIBRATSALUD_SW_VERSION = "libratsalud-sw-v4";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});


function leerConfiguracionSilencio(){
  return new Promise(resolve=>{
    try{
      const req=indexedDB.open("libratsalud-notificaciones",1);
      req.onupgradeneeded=()=>{try{req.result.createObjectStore("config")}catch(e){}};
      req.onsuccess=()=>{
        const db=req.result;
        try{
          const tx=db.transaction("config","readonly");
          const get=tx.objectStore("config").get("horario");
          get.onsuccess=()=>{const v=get.result||{activo:false};db.close();resolve(v);};
          get.onerror=()=>{db.close();resolve({activo:false});};
        }catch(e){db.close();resolve({activo:false});}
      };
      req.onerror=()=>resolve({activo:false});
    }catch(e){resolve({activo:false});}
  });
}
function notificacionesEnSilencio(c){
  if(!c) return false;
  if(c.ubicacion && c.ubicacion.activo && c.ubicacion.fuera) return true;
  if(!c.activo) return false;
  const ahora=new Date();
  if(c.hasta){
    const hasta=new Date(c.hasta).getTime();
    if(Number.isFinite(hasta)) return Date.now() < hasta;
  }
  const minutos=ahora.getHours()*60+ahora.getMinutes();
  const [ih,im]=(c.inicio||"22:00").split(":").map(Number);
  const [fh,fm]=(c.fin||"07:00").split(":").map(Number);
  const inicio=ih*60+im, fin=fh*60+fm;
  if(inicio===fin) return true;
  return inicio<fin ? minutos>=inicio && minutos<fin : minutos>=inicio || minutos<fin;
}

self.addEventListener("push", event => {
  let data = {};

  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = {
      title: "LibraCare",
      body: event.data ? event.data.text() : "Nueva actualización"
    };
  }

  event.waitUntil(
    leerConfiguracionSilencio().then(config=>{
      if(notificacionesEnSilencio(config)) return;
      return self.registration.showNotification(
      data.title || "LibraCare",
      {
        body: data.body || "Hay una actualización de habitación.",
        icon: "./icon-libracare.svg",
        badge: "./icon-192.png",
        tag: data.tag || "libratsalud",
        renotify: true,
        data: data.data || { url: "./" }
      }
    );
    })
  );
});

self.addEventListener("notificationclick", event => {
  event.notification.close();

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then(lista => {
      for (const cliente of lista) {
        if ("focus" in cliente) {
          return cliente.focus();
        }
      }
      return clients.openWindow((event.notification.data && event.notification.data.url) || "./");
    })
  );
});

const LIBRACARE_CACHE = "libracare-shell-v1";
const LIBRACARE_SHELL = ["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png"];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(LIBRACARE_CACHE)
      .then(cache => cache.addAll(LIBRACARE_SHELL))
      .catch(() => null)
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("libracare-shell-") && k !== LIBRACARE_CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        const copy = response.clone();
        caches.open(LIBRACARE_CACHE).then(cache => cache.put(event.request, copy)).catch(()=>{});
        return response;
      })
      .catch(() => caches.match(event.request).then(r => r || caches.match("./index.html")))
  );
});
