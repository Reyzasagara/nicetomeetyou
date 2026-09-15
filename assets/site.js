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

  // PowerSync explorer: group filter, search, expand all, and links that open a module.
  var explorer = document.querySelector('[data-ps-explorer]');
  if (explorer) {
    var psModules = Array.from(explorer.querySelectorAll('.ps-module'));
    var psGroups = Array.from(explorer.querySelectorAll('.ps-cluster'));
    var psChips = Array.from(explorer.querySelectorAll('[data-cluster-filter]'));
    var psSearch = explorer.querySelector('#ps-search');
    var psStatus = explorer.querySelector('[data-ps-status]');
    var psEmpty = explorer.querySelector('[data-ps-empty]');
    var psToggle = explorer.querySelector('[data-expand-all]');
    var psReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var activeGroup = 'all';

    function psTransition(fn) {
      if (document.startViewTransition && !psReduce.matches) document.startViewTransition(fn);
      else fn();
    }

    function psApply() {
      var query = (psSearch.value || '').trim().toLowerCase();
      var shown = 0;
      psModules.forEach(function (m) {
        var inGroup = activeGroup === 'all' || m.dataset.cluster === activeGroup;
        var matches = !query || m.textContent.toLowerCase().indexOf(query) !== -1;
        m.hidden = !(inGroup && matches);
        if (!m.hidden) {
          shown++;
          if (query) m.open = true;
        }
      });
      psGroups.forEach(function (g) {
        g.hidden = !g.querySelector('.ps-module:not([hidden])');
      });
      if (psEmpty) psEmpty.hidden = shown !== 0;
      if (psStatus) psStatus.textContent = (psStatus.dataset.many || '{n} modules shown.').replace('{n}', shown);
    }

    psChips.forEach(function (chipBtn) {
      chipBtn.addEventListener('click', function () {
        activeGroup = chipBtn.dataset.clusterFilter;
        psChips.forEach(function (other) {
          other.setAttribute('aria-pressed', String(other === chipBtn));
        });
        psTransition(psApply);
      });
    });

    var psTimer;
    psSearch.addEventListener('input', function () {
      clearTimeout(psTimer);
      psTimer = setTimeout(psApply, 150);
    });

    psToggle.addEventListener('click', function () {
      var open = psToggle.getAttribute('aria-pressed') !== 'true';
      psModules.forEach(function (m) {
        if (!m.hidden) m.open = open;
      });
      psToggle.setAttribute('aria-pressed', String(open));
      psToggle.textContent = open ? psToggle.dataset.labelCollapse : psToggle.dataset.labelExpand;
    });

    function psOpen(id) {
      var target = document.getElementById(id);
      if (!target || !target.classList.contains('ps-module')) return;
      if (target.hidden) {
        activeGroup = 'all';
        psSearch.value = '';
        psChips.forEach(function (c) {
          c.setAttribute('aria-pressed', String(c.dataset.clusterFilter === 'all'));
        });
        psApply();
      }
      target.open = true;
      target.classList.remove('is-flash');
      void target.offsetWidth;
      target.classList.add('is-flash');
      target.scrollIntoView({ behavior: psReduce.matches ? 'auto' : 'smooth', block: 'start' });
      var summary = target.querySelector('summary');
      if (summary) summary.focus({ preventScroll: true });
    }

    document.addEventListener('click', function (event) {
      var link = event.target.closest('[data-open-module]');
      if (!link) return;
      event.preventDefault();
      var id = 'm-' + link.dataset.openModule;
      if (location.hash !== '#' + id) history.pushState(null, '', '#' + id);
      psOpen(id);
    });

    window.addEventListener('hashchange', function () {
      psOpen(decodeURIComponent(location.hash.slice(1)));
    });

    psApply();
    if (location.hash.indexOf('#m-') === 0) psOpen(decodeURIComponent(location.hash.slice(1)));
  }
})();
