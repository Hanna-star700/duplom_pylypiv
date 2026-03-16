/**
 * LearnCode — глобальні анімації та поведінка
 */

(function () {
  'use strict';

  // ——— Перемикач теми (світлий/темний режим) ———
  var THEME_KEY = 'learncode-theme';
  var html = document.documentElement;
  function getTheme() {
    try {
      return localStorage.getItem(THEME_KEY) || 'dark';
    } catch (e) { return 'dark'; }
  }
  function setTheme(theme) {
    theme = theme === 'light' ? 'light' : 'dark';
    html.setAttribute('data-theme', theme);
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
    var btn = document.getElementById('theme-toggle');
    if (btn) btn.setAttribute('aria-label', theme === 'light' ? 'Темний режим' : 'Світлий режим');
  }
  setTheme(getTheme());
  var themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      setTheme(html.getAttribute('data-theme') === 'light' ? 'dark' : 'light');
    });
  }

  // ——— Scroll reveal ——— 
  var revealEls = document.querySelectorAll('.reveal');
  var observerOptions = {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.1
  };

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, observerOptions);

  revealEls.forEach(function (el) {
    observer.observe(el);
  });

  // ——— Плавне прокручування для якорів ———
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      if (id === '#') return;
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ——— Підсвітка активного пункту навігації при скролі ———
  var navLinks = document.querySelectorAll('.nav a[href^="#"]');
  var sections = [];

  navLinks.forEach(function (link) {
    var id = link.getAttribute('href');
    if (id && id.length > 1) {
      var section = document.querySelector(id);
      if (section) sections.push({ id: id, section: section, link: link });
    }
  });

  function updateActiveNav() {
    var scrollY = window.pageYOffset;
    var headerHeight = 80;

    for (var i = sections.length - 1; i >= 0; i--) {
      var top = sections[i].section.getBoundingClientRect().top + scrollY - headerHeight;
      if (scrollY >= top - 100) {
        sections.forEach(function (s) { s.link.classList.remove('active'); });
        sections[i].link.classList.add('active');
        break;
      }
    }
  }

  if (sections.length) {
    window.addEventListener('scroll', function () {
      requestAnimationFrame(updateActiveNav);
    });
    updateActiveNav();
  }

  // ——— Мобільне меню (гамбургер) ———
  var navToggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('nav');
  var header = document.getElementById('site-header');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = header && header.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (header) header.classList.remove('nav-open');
        if (navToggle) navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
})();
