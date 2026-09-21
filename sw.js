const LIBRATSALUD_SW_VERSION = "libratsalud-sw-v6";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil((async()=>{
    await self.clients.claim();
    const lista=await self.clients.matchAll({type:"window",includeUncontrolled:true});
    for(const cliente of lista){
      try{
        const u=new URL(cliente.url);
        if(u.origin===self.location.origin && u.searchParams.get("appv")!=="6"){
          u.searchParams.set("appv","6");
          await cliente.navigate(u.toString());
        }
      }catch(e){}
    }
  })());
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
  return !!(c.ubicacion && c.ubicacion.activo && c.ubicacion.fuera);
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
