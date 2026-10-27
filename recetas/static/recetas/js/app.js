// Abrir / cerrar modales
document.addEventListener("click", function (e) {
  const abrir = e.target.closest("[data-open]");
  if (abrir) {
    document.getElementById(abrir.dataset.open).classList.add("open");
    return;
  }
  const cerrar = e.target.closest("[data-close]");
  if (cerrar) {
    cerrar.closest(".overlay").classList.remove("open");
    return;
  }
  if (e.target.classList.contains("overlay")) {
    e.target.classList.remove("open");
  }
});

// Pestañas del perfil
document.querySelectorAll("[data-tab]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    mostrarTab(btn.dataset.tab);
  });
});

function mostrarTab(tab) {
  document.querySelectorAll("[data-tab]").forEach(function (b) {
    b.classList.toggle("active", b.dataset.tab === tab);
  });
  document.querySelectorAll("[data-panel]").forEach(function (p) {
    p.style.display = p.dataset.panel === tab ? "block" : "none";
  });
}

// Toast de mensajes
const toast = document.getElementById("toast");
if (toast) {
  requestAnimationFrame(function () {
    toast.classList.add("show");
  });
  setTimeout(function () {
    toast.classList.remove("show");
  }, 2600);
}

// Búsqueda en vivo (con pequeña espera)
const buscador = document.getElementById("search-input");
if (buscador) {
  let t;
  buscador.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(function () {
      buscador.form.submit();
    }, 450);
  });
  // dejar el cursor al final después de recargar
  if (buscador.value) {
    buscador.focus();
    buscador.setSelectionRange(buscador.value.length, buscador.value.length);
  }
}
