(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var header = document.querySelector('.site-header');
  var menu = document.querySelector('[data-menu-toggle]');
  var labelOpen = menu ? menu.dataset.labelOpen || 'Open menu' : '';
  var labelClose = menu ? menu.dataset.labelClose || 'Close menu' : '';
  function closeMenu(restoreFocus) {
    header.classList.remove('nav-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', labelOpen);
    if (restoreFocus) menu.focus();
  }
  if (header && menu) {
    menu.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? labelClose : labelOpen);
    });
    header.querySelectorAll('.nav a').forEach(function (link) {
      link.addEventListener('click', function () { closeMenu(false); });
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && header.classList.contains('nav-open')) closeMenu(true);
    });
    document.addEventListener('click', function (event) {
      if (!header.contains(event.target) && header.classList.contains('nav-open')) closeMenu(false);
    });
    window.matchMedia('(min-width: 601px)').addEventListener('change', function (event) {
      if (event.matches) closeMenu(false);
    });
  }
  var filters = document.querySelector('.work-filters');
  if (filters) {
    var cards = Array.from(document.querySelectorAll('.project-card[data-domain]'));
    var status = document.querySelector('[data-filter-status]');
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    filters.hidden = false;
    filters.querySelectorAll('button').forEach(function (button) {
      button.addEventListener('click', function () {
        function apply() {
          filters.querySelectorAll('button').forEach(function (other) {
            other.setAttribute('aria-pressed', String(other === button));
          });
          var count = 0;
          cards.forEach(function (card) {
            var visible = button.dataset.filter === 'all' || card.dataset.domain === button.dataset.filter;
            card.hidden = !visible;
            if (visible) count++;
          });
          if (status) {
            var template = count === 1 ? status.dataset.one || '1 case study shown.' : status.dataset.many || '{n} case studies shown.';
            status.textContent = template.replace('{n}', count);
          }
        }
        if (document.startViewTransition && !reduceMotion.matches) {
          document.startViewTransition(apply);
        } else {
          apply();
        }
      });
    });
  }
})();
