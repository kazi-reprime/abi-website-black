/* ABI Landing Pages — shared behavior */
(function () {
  'use strict';

  var LANG = document.documentElement.lang === 'es' ? 'es' : 'en';
  document.documentElement.classList.add('js');

  /* ── CONFIG ──────────────────────────────────────────────
     Set your Formspree (or other) endpoint once, here.
     Create a free form at https://formspree.io → replace the ID.
     Leads can also be forwarded by Formspree to admission@abi.edu
     and into the LeadConnector CRM via Zapier/webhook.            */
  var FORM_ENDPOINT = 'https://formspree.io/f/REPLACE_WITH_FORM_ID';

  /* ── Next start date: first Monday of next month ───────── */
  function nextFirstMonday() {
    var now = new Date();
    var d = new Date(now.getFullYear(), now.getMonth(), 1);
    // first Monday of current month
    while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
    if (d <= now) {
      d = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
    }
    return d;
  }
  var startDate = nextFirstMonday();
  var fmt = new Intl.DateTimeFormat(LANG === 'es' ? 'es-US' : 'en-US', {
    weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
  });
  var dateStr = fmt.format(startDate);
  if (LANG === 'es') dateStr = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
  document.querySelectorAll('[data-next-start]').forEach(function (el) {
    el.textContent = dateStr;
  });

  /* ── Countdown ──────────────────────────────────────────── */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var cells = {
      d: cd.querySelector('[data-cd-d]'), h: cd.querySelector('[data-cd-h]'),
      m: cd.querySelector('[data-cd-m]'), s: cd.querySelector('[data-cd-s]')
    };
    var tick = function () {
      var diff = startDate.getTime() - Date.now();
      if (diff < 0) diff = 0;
      var s = Math.floor(diff / 1000);
      cells.d.textContent = Math.floor(s / 86400);
      cells.h.textContent = Math.floor((s % 86400) / 3600);
      cells.m.textContent = Math.floor((s % 3600) / 60);
      cells.s.textContent = s % 60;
    };
    tick(); setInterval(tick, 1000);
  }

  /* ── Hamburger ──────────────────────────────────────────── */
  var burger = document.querySelector('.hamburger');
  var drawer = document.querySelector('.nav-drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ── Accordion ──────────────────────────────────────────── */
  document.querySelectorAll('.acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.parentElement.classList.toggle('open');
    });
  });

  /* ── Reveal on scroll ───────────────────────────────────── */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
  }

  /* ── Lead form submit (AJAX) ────────────────────────────── */
  document.querySelectorAll('form.leadform').forEach(function (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('.btn-submit');
      var err = form.querySelector('.form-error');
      btn.disabled = true;
      btn.textContent = LANG === 'es' ? 'ENVIANDO…' : 'SENDING…';
      err.style.display = 'none';

      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      }).then(function (r) {
        if (!r.ok) throw new Error('bad status');
        form.style.display = 'none';
        var ok = form.parentElement.querySelector('.form-success');
        if (ok) ok.classList.add('show');
        try { if (window.gtag) gtag('event', 'generate_lead'); } catch (e) {}
        try { if (window.fbq) fbq('track', 'Lead'); } catch (e) {}
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = LANG === 'es' ? 'ENVIAR' : 'SUBMIT';
        err.style.display = 'block';
      });
    });
  });

  /* ── Chat-style bubble → scroll to form ─────────────────── */
  var bubble = document.querySelector('.bubble');
  var tip = document.querySelector('.bubble-tip');
  if (bubble) {
    setTimeout(function () { if (tip) tip.classList.add('show'); }, 6000);
    bubble.addEventListener('click', function () {
      if (tip) tip.classList.remove('show');
      var f = document.querySelector('.formcard');
      if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'center' });
        var first = f.querySelector('input'); if (first) setTimeout(function(){ first.focus(); }, 600); }
    });
    var x = document.querySelector('.bubble-tip .tip-x');
    if (x) x.addEventListener('click', function () { tip.classList.remove('show'); });
  }

  /* ── Exit intent (desktop, once per session) ────────────── */
  var exit = document.querySelector('.exit');
  if (exit && !sessionStorage.getItem('abiExitShown') && window.matchMedia('(pointer:fine)').matches) {
    document.addEventListener('mouseout', function handler(e) {
      if (e.clientY <= 0 && !e.relatedTarget) {
        exit.classList.add('show');
        sessionStorage.setItem('abiExitShown', '1');
        document.removeEventListener('mouseout', handler);
      }
    });
    exit.addEventListener('click', function (e) {
      if (e.target === exit || e.target.closest('.exit-x')) exit.classList.remove('show');
    });
    var go = exit.querySelector('[data-exit-cta]');
    if (go) go.addEventListener('click', function () {
      exit.classList.remove('show');
      var f = document.querySelector('.formcard');
      if (f) f.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
})();
