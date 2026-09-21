const LIBRATSALUD_SW_VERSION = "libratsalud-sw-v3";

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
  if(!c || !c.activo) return false;
  const ahora=new Date();
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
      title: "Libratsalud",
      body: event.data ? event.data.text() : "Nueva actualización"
    };
  }

  event.waitUntil(
    leerConfiguracionSilencio().then(config=>{
      if(notificacionesEnSilencio(config)) return;
      return self.registration.showNotification(
      data.title || "Libratsalud",
      {
        body: data.body || "Hay una actualización de habitación.",
        icon: "./icon-192.png",
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