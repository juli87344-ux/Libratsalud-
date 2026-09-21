const LIBRATSALUD_SW_VERSION = "libratsalud-sw-v3";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});

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
    self.registration.showNotification(
      data.title || "Libratsalud",
      {
        body: data.body || "Hay una actualización de habitación.",
        icon: "./icon-192.png",
        badge: "./icon-192.png",
        tag: data.tag || "libratsalud",
        renotify: true,
        data: data.data || { url: "./" }
      }
    )
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
      return clients.openWindow("./");
    })
  );
});