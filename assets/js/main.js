/*
 * SYJ Mining Platform — main.js
 * Vanilla JS only. No build step. No external dependencies.
 * Progressive enhancement: all core content is readable with JS disabled.
 */
(function () {
  "use strict";

  var doc = document;
  var header = doc.querySelector(".site-header");
  var toggle = doc.querySelector(".nav-toggle");
  var links = doc.querySelector(".nav-links");

  /* Mobile nav toggle */
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var isOpen = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    links.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Close mobile nav on Escape */
  doc.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && links && links.classList.contains("is-open")) {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.focus();
    }
  });

  /* Active nav link highlighting via IntersectionObserver */
  var sections = doc.querySelectorAll("main section[id]");
  var navAnchors = doc.querySelectorAll(".nav-links a[href^='#']");

  if ("IntersectionObserver" in window && sections.length && navAnchors.length) {
    var byId = {};
    navAnchors.forEach(function (a) {
      byId[a.getAttribute("href").slice(1)] = a;
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var anchor = byId[entry.target.id];
          if (!anchor) return;
          if (entry.isIntersecting) {
            navAnchors.forEach(function (a) { a.removeAttribute("aria-current"); });
            anchor.setAttribute("aria-current", "true");
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px", threshold: 0 }
    );

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* Header shadow-on-scroll (cheap, no layout thrash) */
  var lastScrolled = false;
  function onScroll() {
    var scrolled = window.scrollY > 4;
    if (scrolled !== lastScrolled && header) {
      header.style.borderBottomColor = scrolled
        ? "rgba(230,238,240,0.16)"
        : "rgba(230,238,240,0.09)";
      lastScrolled = scrolled;
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Footer year */
  var yearEl = doc.getElementById("current-year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* Respect prefers-reduced-motion for anything driven from JS (currently
     none of the motion here is JS-driven, but this guards future additions) */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    doc.documentElement.setAttribute("data-reduced-motion", "true");
  }
})();
