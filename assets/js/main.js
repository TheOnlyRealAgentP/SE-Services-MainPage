/* Stewart Engineering Services: the only JavaScript on the site.
   1) mobile menu toggle  2) contact form: prefill + send without leaving the page.
   Everything works without JS too: the menu shows expanded and the form posts normally. */
(function () {
  'use strict';

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  var desktop = window.matchMedia('(min-width: 1200px)');

  var header = document.querySelector('.site-header');

  function setOpen(open) {
    if (!toggle || !nav) return;
    if (open) {
      // The phone menu fills the screen below the header, so start from the top.
      window.scrollTo(0, 0);
      var bottom = header ? header.getBoundingClientRect().bottom : 0;
      document.documentElement.style.setProperty('--menu-top', Math.max(0, bottom) + 'px');
    }
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    nav.classList.toggle('is-open', open);
    document.documentElement.classList.toggle('menu-open', open);
    var label = toggle.querySelector('.menu-label');
    if (label) label.textContent = open ? 'Close' : 'Menu';
  }

  // Phone menu: Septic & Aerobic / Engineering expand and collapse.
  Array.prototype.forEach.call(document.querySelectorAll('.sub-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentNode;
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      item.classList.toggle('is-open', open);
    });
  });

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true' && !desktop.matches) {
        setOpen(false);
        toggle.focus();
      }
    });
    var onChange = function () { if (desktop.matches) setOpen(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange);
    else if (desktop.addListener) desktop.addListener(onChange);
  }

  /* ---------- Review carousel ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-reviews]'), function (root) {
    var track = root.querySelector('.reviews-track');
    var slides = root.querySelectorAll('.review-slide');
    var dots = root.querySelectorAll('.rv-dot');
    var pauseBtn = root.querySelector('.rv-pause');
    if (!track || slides.length < 2) return;

    var DELAY = 7000;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var userPaused = reduce;          // people who prefer less motion start paused
    var hovering = false, focused = false, visible = true, touchHold = 0;
    var timer = null, index = 0;

    function current() { return Math.round(track.scrollLeft / track.clientWidth); }
    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.scrollTo({ left: index * track.clientWidth, behavior: reduce ? 'auto' : 'smooth' });
      mark(index);
    }
    function mark(i) {
      Array.prototype.forEach.call(dots, function (d, n) {
        if (n === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
      });
    }
    function running() { return !userPaused && !hovering && !focused && visible && !document.hidden && Date.now() > touchHold; }
    function tick() { if (running()) goTo(current() + 1); }
    function start() { stop(); timer = setInterval(tick, DELAY); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    function syncPause() {
      if (!pauseBtn) return;
      pauseBtn.setAttribute('aria-pressed', userPaused ? 'true' : 'false');
      pauseBtn.querySelector('.rv-pause-label').textContent = userPaused ? 'Play' : 'Pause';
      track.setAttribute('aria-live', userPaused ? 'polite' : 'off');
      root.classList.toggle('is-paused', userPaused);
    }

    root.querySelector('.rv-prev').addEventListener('click', function () { goTo(current() - 1); start(); });
    root.querySelector('.rv-next').addEventListener('click', function () { goTo(current() + 1); start(); });
    Array.prototype.forEach.call(dots, function (d, n) { d.addEventListener('click', function () { goTo(n); start(); }); });
    if (pauseBtn) pauseBtn.addEventListener('click', function () { userPaused = !userPaused; syncPause(); start(); });

    root.addEventListener('mouseenter', function () { hovering = true; });
    root.addEventListener('mouseleave', function () { hovering = false; });
    root.addEventListener('focusin', function () { focused = true; });
    root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) focused = false; });
    track.addEventListener('touchstart', function () { touchHold = Date.now() + 12000; }, { passive: true });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current() + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current() - 1); }
    });
    var settle;
    track.addEventListener('scroll', function () {
      clearTimeout(settle);
      settle = setTimeout(function () { index = current(); mark(index); }, 80);
    }, { passive: true });
    window.addEventListener('resize', function () { track.scrollLeft = index * track.clientWidth; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }, { threshold: 0.3 }).observe(root);
    }
    syncPause();
    start();
  });

  /* ---------- Contact form ---------- */
  var form = document.querySelector('[data-quote-form]');
  if (!form) return;

  // Prefill from links like /contact?service=maintenance&town=Crosby#quote
  try {
    var params = new URLSearchParams(window.location.search);
    [['service', 'f-service'], ['town', 'f-town']].forEach(function (pair) {
      var value = params.get(pair[0]);
      var select = document.getElementById(pair[1]);
      if (!value || !select) return;
      for (var i = 0; i < select.options.length; i++) {
        if (select.options[i].value === value) { select.value = value; break; }
      }
    });
  } catch (e) { /* old browser: no prefill, form still works */ }

  var success = form.querySelector('[data-form-success]');
  var failure = form.querySelector('[data-form-error]');
  var button = form.querySelector('button[type="submit"]');

  function show(el) {
    [success, failure].forEach(function (x) { if (x) x.hidden = (x !== el); });
    if (el) el.focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Spam trap: real people never fill the hidden field.
    var trap = form.querySelector('.hp input');
    if (trap && trap.value) { form.classList.add('is-sent'); show(success); return; }

    if (form.hasAttribute('data-unconfigured') || !form.getAttribute('action')) {
      show(failure);
      return;
    }

    form.classList.add('is-sending');
    if (button) button.disabled = true;

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    }).then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      form.classList.add('is-sent');
      form.reset();
      show(success);
    }).catch(function () {
      show(failure);
    }).then(function () {
      form.classList.remove('is-sending');
      if (button) button.disabled = false;
    });
  });
})();
