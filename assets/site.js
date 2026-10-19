// Banner cookie minimale: nessun cookie di tracciamento viene caricato finché l'utente non accetta.
(function () {
  var KEY = 'vg_cookie_choice';
  var banner = document.querySelector('.cookie');
  if (!banner) return;
  var choice = null;
  try { choice = localStorage.getItem(KEY); } catch (e) {}
  if (!choice) banner.classList.add('show');
  banner.querySelector('.ok').addEventListener('click', function () {
    try { localStorage.setItem(KEY, 'accept'); } catch (e) {}
    banner.classList.remove('show');
    // Qui si caricano eventuali script di analytics (es. Plausible, GA4) solo dopo il consenso.
  });
  banner.querySelector('.no').addEventListener('click', function () {
    try { localStorage.setItem(KEY, 'reject'); } catch (e) {}
    banner.classList.remove('show');
  });
})();
