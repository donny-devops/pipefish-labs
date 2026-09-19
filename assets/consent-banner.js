// PipeFish Labs - Cookie Consent Banner & Google Consent Mode v2
(function () {
  if (typeof window === "undefined") return;

  var STORAGE_KEY = "pfl_consent_mode";
  var currentConsent = localStorage.getItem(STORAGE_KEY);

  // If user already made a choice, do not render banner
  if (currentConsent) return;

  function updateConsent(status) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        ad_storage: status,
        ad_user_data: status,
        ad_personalization: status,
        analytics_storage: status,
      });
    }
    localStorage.setItem(STORAGE_KEY, status);
    var banner = document.getElementById("pfl-consent-banner");
    if (banner) {
      banner.style.opacity = "0";
      banner.style.transform = "translateY(20px)";
      setTimeout(function () {
        if (banner.parentNode) banner.parentNode.removeChild(banner);
      }, 300);
    }
  }

  function initBanner() {
    if (document.getElementById("pfl-consent-banner")) return;

    var banner = document.createElement("div");
    banner.id = "pfl-consent-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Cookie and Privacy Preferences");
    banner.setAttribute("aria-modal", "false");

    banner.innerHTML =
      '<div class="pfl-cb-card">' +
        '<div class="pfl-cb-header">' +
          '<span class="pfl-cb-icon">🔒</span>' +
          '<h3 class="pfl-cb-title">Privacy &amp; Analytics Consent</h3>' +
        '</div>' +
        '<p class="pfl-cb-desc">' +
          'PipeFish Labs uses cookies and telemetry to analyze web traffic and deliver tailored experiences in compliance with Google Consent Mode v2 and GDPR. ' +
          '<a href="/legal-privacy-policy/" class="pfl-cb-link" target="_blank" rel="noopener">Privacy Policy</a>.' +
        '</p>' +
        '<div class="pfl-cb-actions">' +
          '<button type="button" id="pfl-cb-accept" class="pfl-cb-btn pfl-cb-btn-accept">Accept All</button>' +
          '<button type="button" id="pfl-cb-decline" class="pfl-cb-btn pfl-cb-btn-decline">Essential Only</button>' +
        '</div>' +
      '</div>';

    var style = document.createElement("style");
    style.textContent =
      "#pfl-consent-banner {" +
        "position: fixed;" +
        "bottom: 24px;" +
        "right: 24px;" +
        "max-width: 440px;" +
        "width: calc(100% - 48px);" +
        "z-index: 99999;" +
        "font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;" +
        "transition: opacity 0.3s ease, transform 0.3s ease;" +
      "}" +
      ".pfl-cb-card {" +
        "background: rgba(10, 15, 25, 0.96);" +
        "border: 1px solid rgba(0, 212, 255, 0.35);" +
        "border-radius: 12px;" +
        "padding: 22px 24px;" +
        "box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6), 0 0 24px rgba(0, 212, 255, 0.15);" +
        "backdrop-filter: blur(12px);" +
        "-webkit-backdrop-filter: blur(12px);" +
        "color: #e6edf3;" +
      "}" +
      ".pfl-cb-header {" +
        "display: flex;" +
        "align-items: center;" +
        "gap: 10px;" +
        "margin-bottom: 10px;" +
      "}" +
      ".pfl-cb-icon {" +
        "font-size: 18px;" +
      "}" +
      ".pfl-cb-title {" +
        "margin: 0;" +
        "font-size: 15px;" +
        "font-weight: 700;" +
        "color: #00D4FF;" +
        "letter-spacing: 0.02em;" +
      "}" +
      ".pfl-cb-desc {" +
        "margin: 0 0 18px 0;" +
        "font-size: 13px;" +
        "line-height: 1.6;" +
        "color: #94a3b8;" +
      "}" +
      ".pfl-cb-link {" +
        "color: #00D4FF;" +
        "text-decoration: underline;" +
        "text-underline-offset: 3px;" +
      "}" +
      ".pfl-cb-actions {" +
        "display: flex;" +
        "gap: 12px;" +
        "align-items: center;" +
      "}" +
      ".pfl-cb-btn {" +
        "flex: 1;" +
        "padding: 10px 16px;" +
        "border-radius: 8px;" +
        "font-size: 13px;" +
        "font-weight: 600;" +
        "cursor: pointer;" +
        "transition: all 0.2s ease;" +
        "border: none;" +
      "}" +
      ".pfl-cb-btn-accept {" +
        "background: linear-gradient(135deg, #00D4FF, #0099CC);" +
        "color: #000;" +
        "box-shadow: 0 0 14px rgba(0, 212, 255, 0.4);" +
      "}" +
      ".pfl-cb-btn-accept:hover {" +
        "transform: translateY(-1px);" +
        "box-shadow: 0 0 20px rgba(0, 212, 255, 0.6);" +
      "}" +
      ".pfl-cb-btn-decline {" +
        "background: rgba(255, 255, 255, 0.06);" +
        "color: #cbd5e1;" +
        "border: 1px solid rgba(255, 255, 255, 0.15);" +
      "}" +
      ".pfl-cb-btn-decline:hover {" +
        "background: rgba(255, 255, 255, 0.12);" +
        "color: #fff;" +
      "}" +
      "@media (max-width: 600px) {" +
        "#pfl-consent-banner { bottom: 12px; right: 12px; width: calc(100% - 24px); }" +
        ".pfl-cb-actions { flex-direction: column; }" +
        ".pfl-cb-btn { width: 100%; text-align: center; }" +
      "}";

    document.head.appendChild(style);
    document.body.appendChild(banner);

    document.getElementById("pfl-cb-accept").addEventListener("click", function () {
      updateConsent("granted");
    });
    document.getElementById("pfl-cb-decline").addEventListener("click", function () {
      updateConsent("denied");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBanner);
  } else {
    initBanner();
  }
})();
