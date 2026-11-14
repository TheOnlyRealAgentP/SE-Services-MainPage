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
