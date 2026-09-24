/* Evidence deck runtime: scale the fixed stage, switch slides, draw the Sankey.
   Every number comes from the page markup, so the deck degrades to readable
   HTML when this script does not run. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var stage = document.getElementById('stage');
  var slides = [].slice.call(document.querySelectorAll('.deck-slide'));
  if (!stage || !slides.length) return;

  /* ---------------------------------------------------------------- scale */
  function fit() {
    var w = window.innerWidth / 1600;
    var h = window.innerHeight / 900;
    var s = Math.min(w, h);
    stage.style.transform =
      'translate(' + (window.innerWidth - 1600 * s) / 2 + 'px,' +
      (window.innerHeight - 900 * s) / 2 + 'px) scale(' + s + ')';
  }
  fit();
  window.addEventListener('resize', fit);

  var STILL = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- slides */
  var buttons = [].slice.call(document.querySelectorAll('.deck-nav button'));
  var progress = document.querySelector('.deck-progress');
  var count = document.querySelector('.deck-count');
  var current = -1;

  function show(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    if (i === current) return;
    current = i;
    slides.forEach(function (s, n) {
      if (n === i) s.setAttribute('data-on', '');
      else s.removeAttribute('data-on');
    });
    buttons.forEach(function (b, n) {
      if (n === i) b.setAttribute('aria-current', 'true');
      else b.removeAttribute('aria-current');
    });
    if (progress) progress.style.width = ((i + 1) / slides.length) * 100 + '%';
    if (count) count.textContent = (i + 1) + ' / ' + slides.length;
    grow(slides[i]);
    slides[i].querySelectorAll('[data-count]').forEach(countUp);
    stageLabels(slides[i]);
  }

  function grow(slide) {
    slide.querySelectorAll('.bar i[data-w]').forEach(function (el) {
      el.style.width = '0';
      requestAnimationFrame(function () {
        el.style.width = el.getAttribute('data-w') + '%';
      });
    });
  }

  /* Count a figure up from zero, keeping its thousands separator and any
     prefix or suffix the markup asked for. */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var pre = el.getAttribute('data-prefix') || '';
    var post = el.getAttribute('data-suffix') || '';
    var sep = el.getAttribute('data-sep') || '';
    var decimals = (el.getAttribute('data-count').split('.')[1] || '').length;

    function render(v) {
      var text = decimals ? v.toFixed(decimals) : String(Math.round(v));
      if (sep) {
        var parts = text.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, sep);
        text = parts.join(sep === ',' ? '.' : ',');
      }
      el.textContent = pre + text + post;
    }

    if (STILL) { render(target); return; }
    var started = null;
    var dur = 1100;
    function step(now) {
      if (started === null) started = now;
      var p = Math.min(1, (now - started) / dur);
      render(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    render(0);
    requestAnimationFrame(step);
  }

  /* Sankey labels and flow particles arrive after the ribbons have drawn. */
  function stageLabels(slide) {
    var labels = slide.querySelectorAll('.sk-lab, .sk-parts');
    labels.forEach(function (g, n) {
      g.classList.remove('on');
      if (STILL) { g.classList.add('on'); return; }
      setTimeout(function () { g.classList.add('on'); }, 420 + n * 130);
    });
  }

  buttons.forEach(function (b, n) {
    b.addEventListener('click', function () { show(n); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') show(current + 1);
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') show(current - 1);
  });

  /* ---------------------------------------------------------------- sankey */
  function el(tag, attrs, parent) {
    var node = document.createElementNS(NS, tag);
    for (var k in attrs) node.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(node);
    return node;
  }

  function text(parent, x, y, value, cls, size, fill) {
    var node = el('text', { x: x, y: y, class: cls, 'font-size': size, fill: fill }, parent);
    node.textContent = value;
    return node;
  }

  function sankey(host) {
    var spec = JSON.parse(host.getAttribute('data-sankey'));
    var W = spec.width, H = spec.height, NW = spec.nodeWidth || 13;
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'presentation' }, host);
    var defs = el('defs', {}, svg);
    var hatch = el('pattern', {
      id: 'sk-hatch', width: 10, height: 10,
      patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)'
    }, defs);
    el('rect', { width: 10, height: 10, fill: '#fff' }, hatch);
    el('rect', { width: 4, height: 10, fill: '#dbe1e5' }, hatch);

    var nodes = {};
    var top = spec.top || 0;
    spec.nodes.forEach(function (n) {
      n.h = Math.max(spec.minHeight || 3, n.value * spec.scale);
      n.y = n.y === undefined ? top : n.y;
      n.ins = []; n.outs = [];
      nodes[n.id] = n;
    });
    spec.links.forEach(function (l) {
      l.from = nodes[l.s]; l.to = nodes[l.t];
      l.from.outs.push(l); l.to.ins.push(l);
    });
    spec.nodes.forEach(function (n) {
      var out = n.outs.reduce(function (a, l) { return a + l.value; }, 0);
      var into = n.ins.reduce(function (a, l) { return a + l.value; }, 0);
      var acc = 0;
      n.outs.forEach(function (l) { l.w0 = n.h * l.value / out; l.y0 = n.y + acc; acc += l.w0; });
      acc = 0;
      n.ins.forEach(function (l) { l.w1 = n.h * l.value / into; l.y1 = n.y + acc; acc += l.w1; });
    });

    var ribbons = el('g', {}, svg);
    spec.links.forEach(function (l) {
      var x0 = l.from.x + NW, x1 = l.to.x, xm = (x0 + x1) / 2;
      var d = 'M' + x0 + ',' + l.y0 +
        ' C' + xm + ',' + l.y0 + ' ' + xm + ',' + l.y1 + ' ' + x1 + ',' + l.y1 +
        ' L' + x1 + ',' + (l.y1 + l.w1) +
        ' C' + xm + ',' + (l.y1 + l.w1) + ' ' + xm + ',' + (l.y0 + l.w0) + ' ' + x0 + ',' + (l.y0 + l.w0) + ' Z';
      el('path', {
        d: d,
        fill: l.blind ? 'url(#sk-hatch)' : (spec.colors[l.color || l.to.type] || '#355c7d'),
        opacity: l.blind ? 1 : (spec.linkOpacity || 0.45)
      }, ribbons);
    });

    var bars = el('g', {}, svg);
    spec.nodes.forEach(function (n) {
      el('rect', {
        x: n.x, y: n.y, width: NW, height: n.h, rx: Math.min(4, n.h / 2),
        fill: n.type === 'blind' ? 'url(#sk-hatch)' : (spec.colors[n.type] || '#355c7d'),
        stroke: n.type === 'blind' ? '#c7ced4' : 'none'
      }, bars);
    });

    var notes = el('g', { class: 'sk-lab' }, svg);
    (spec.notes || []).forEach(function (n) {
      var node = text(notes, n.x, n.y, n.text, 'sk-l', n.size || 14, '#8a949d');
      node.setAttribute('text-anchor', 'middle');
    });

    var parts = el('g', { class: 'sk-parts' }, svg);
    if (!STILL) {
      spec.links.forEach(function (l) {
        if (!l.flow) return;
        var x0 = l.from.x + NW, x1 = l.to.x, xm = (x0 + x1) / 2;
        var c0 = l.y0 + l.w0 / 2, c1 = l.y1 + l.w1 / 2;
        var path = 'M' + x0 + ',' + c0 + ' C' + xm + ',' + c0 + ' ' + xm + ',' + c1 + ' ' + x1 + ',' + c1;
        for (var k = 0; k < l.flow; k++) {
          var dot = el('circle', {
            r: spec.dotRadius || 3,
            fill: spec.colors[l.color || l.to.type] || '#355c7d',
            opacity: 0.9
          }, parts);
          el('animateMotion', {
            dur: (2.6 + Math.random() * 0.7) + 's',
            repeatCount: 'indefinite',
            path: path,
            begin: (-k * 2.8 / l.flow) + 's'
          }, dot);
        }
      });
    }

    var labels = el('g', { class: 'sk-lab' }, svg);
    spec.nodes.forEach(function (n) {
      var right = n.side !== 'left';
      var x = right ? n.x + NW + 11 : n.x - 11;
      var anchor = right ? 'start' : 'end';
      var lines = [
        { v: n.display || String(n.value), cls: 'sk-v', size: n.big || 26, fill: spec.labelColors[n.type] || '#20272d' },
        { v: n.label, cls: 'sk-l', size: 14, fill: '#20272d' }
      ];
      if (n.sub) lines.push({ v: n.sub, cls: 'sk-c', size: 12.5, fill: '#66737e' });
      var height = lines.reduce(function (a, l) { return a + l.size * 1.16; }, 0);
      var y = n.y + n.h / 2 - height / 2 + lines[0].size;
      lines.forEach(function (l) {
        var node = text(labels, x, y, l.v, l.cls, l.size, l.fill);
        node.setAttribute('text-anchor', anchor);
        y += l.size * 1.16;
      });
    });
  }

  document.querySelectorAll('[data-sankey]').forEach(sankey);
  var start = parseInt(new URLSearchParams(location.search).get('slide'), 10);
  show(isFinite(start) ? start - 1 : 0);
})();
