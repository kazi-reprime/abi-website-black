/* ============================================================
   ABI — Analytics & Ads integration
   ------------------------------------------------------------
   TO ACTIVATE: replace the two placeholder IDs below with your
   real GA4 Measurement ID and Meta (Facebook) Pixel ID.
     • GA4:   Admin → Data Streams → Web → "Measurement ID"  (G-XXXXXXXXXX)
     • Meta:  Events Manager → Data Sources → your Pixel → ID  (15-16 digits)
   Until real IDs are set, NO external tracking loads (no failed
   requests) — but conversion events are still wired and will start
   flowing the moment you add the IDs. Google Ads conversions: link
   your Google Ads account to GA4 and import these events as goals.
   ============================================================ */
(function () {
  var GA4_ID = "G-XXXXXXXXXX";   // ← replace with your GA4 Measurement ID
  var META_PIXEL_ID = "";        // ← replace with your Meta Pixel ID (digits only)

  // dataLayer + gtag shim (always available so events queue safely)
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  var gaLive = GA4_ID && GA4_ID.indexOf("XXXX") === -1;
  var pxLive = !!META_PIXEL_ID;

  // ---- Google Analytics 4 (gtag.js) ----
  if (gaLive) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", GA4_ID, { anonymize_ip: true });
  }

  // ---- Meta (Facebook) Pixel ----
  if (pxLive) {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = [];
      t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
    window.fbq("init", META_PIXEL_ID);
    window.fbq("track", "PageView");
  }

  // ---- Conversion event tracking (fires regardless; flows once IDs set) ----
  function track(name, params) {
    try { window.gtag("event", name, params || {}); } catch (e) {}
    try { if (window.fbq) window.fbq("track", name === "lead" ? "Lead" : name === "call" ? "Contact" : "CustomizeProduct"); } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a,button"); if (!a) return;
    var href = a.getAttribute("href") || "", txt = (a.textContent || "").trim().slice(0, 48);
    if (href.indexOf("tel:") === 0) track("call", { phone: href.replace("tel:", "") });
    else if (href.indexOf("mailto:") === 0) track("email_click");
    else if (/apply|reserve|enroll|get (my|info)|start barber|become a barber|request a call/i.test(txt)) track("lead", { cta: txt });
  }, true);
  document.addEventListener("submit", function () { track("lead", { source: "form" }); }, true);
})();
