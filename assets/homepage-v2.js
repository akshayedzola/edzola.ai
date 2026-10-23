(() => {
  const header = document.querySelector('[data-header]');
  const menuTriggers = [...document.querySelectorAll('[data-menu-trigger]')];
  const menus = [...document.querySelectorAll('[data-menu]')];
  const localeTrigger = document.querySelector('[data-locale-trigger]');
  const localeMenu = document.querySelector('[data-locale-menu]');
  const mobileToggle = document.querySelector('[data-mobile-toggle]');
  const mobileNav = document.querySelector('[data-mobile-nav]');
  const mobileLabel = document.querySelector('[data-mobile-label]');
  const mobileDetails = [...mobileNav.querySelectorAll('details')];
  const carousel = document.querySelector('[data-carousel]');
  let activeMenu = null;
  let closeTimer = null;

  if (carousel) {
    const slides = [...carousel.querySelectorAll('[data-slide]')];
    const dots = [...carousel.querySelectorAll('[data-carousel-dot]')];
    const pauseButton = carousel.querySelector('[data-carousel-pause]');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let currentSlide = 0;
    let carouselTimer = null;
    let paused = prefersReducedMotion;

    const updatePauseButton = () => {
      pauseButton.setAttribute('aria-pressed', String(paused));
      pauseButton.innerHTML = paused
        ? '<span aria-hidden="true">▶</span> Play'
        : '<span aria-hidden="true">Ⅱ</span> Pause';
    };

    const showSlide = (index, restart = true) => {
      currentSlide = (index + slides.length) % slides.length;
      slides.forEach((slide, slideIndex) => {
        const active = slideIndex === currentSlide;
        slide.hidden = !active;
        slide.classList.toggle('is-active', active);
      });
      dots.forEach((dot, dotIndex) => {
        const active = dotIndex === currentSlide;
        dot.classList.toggle('is-active', active);
        if (active) dot.setAttribute('aria-current', 'true');
        else dot.removeAttribute('aria-current');
      });
      if (restart && !paused) startCarousel();
    };

    const startCarousel = () => {
      window.clearInterval(carouselTimer);
      if (paused) return;
      carouselTimer = window.setInterval(() => showSlide(currentSlide + 1, false), 8000);
    };

    dots.forEach((dot) => dot.addEventListener('click', () => showSlide(Number(dot.dataset.carouselDot))));
    pauseButton.addEventListener('click', () => {
      paused = !paused;
      updatePauseButton();
      startCarousel();
    });
    carousel.addEventListener('mouseenter', () => window.clearInterval(carouselTimer));
    carousel.addEventListener('mouseleave', startCarousel);
    carousel.addEventListener('focusin', () => window.clearInterval(carouselTimer));
    carousel.addEventListener('focusout', (event) => {
      if (!carousel.contains(event.relatedTarget)) startCarousel();
    });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) window.clearInterval(carouselTimer);
      else startCarousel();
    });
    updatePauseButton();
    startCarousel();
  }

  const reveal = (element) => {
    window.clearTimeout(closeTimer);
    element.hidden = false;
    window.requestAnimationFrame(() => element.classList.add('is-open'));
  };

  const conceal = (element, immediate = false) => {
    if (!element) return;
    element.classList.remove('is-open');
    if (immediate) {
      element.hidden = true;
      return;
    }
    closeTimer = window.setTimeout(() => {
      if (!element.classList.contains('is-open')) element.hidden = true;
    }, 190);
  };

  const closeDesktopMenus = (returnFocus = false) => {
    menuTriggers.forEach((trigger) => trigger.setAttribute('aria-expanded', 'false'));
    menus.forEach((menu) => conceal(menu));
    if (returnFocus && activeMenu) {
      document.querySelector(`[data-menu-trigger="${activeMenu}"]`)?.focus();
    }
    activeMenu = null;
  };

  const closeLocale = () => {
    localeTrigger.setAttribute('aria-expanded', 'false');
    localeMenu.hidden = true;
  };

  const openDesktopMenu = (name) => {
    const trigger = document.querySelector(`[data-menu-trigger="${name}"]`);
    const menu = document.querySelector(`[data-menu="${name}"]`);
    const wasOpen = activeMenu === name;

    closeDesktopMenus();
    closeLocale();
    if (wasOpen) return;

    activeMenu = name;
    trigger.setAttribute('aria-expanded', 'true');
    reveal(menu);
  };

  menuTriggers.forEach((trigger) => {
    trigger.addEventListener('click', () => openDesktopMenu(trigger.dataset.menuTrigger));
  });

  localeTrigger.addEventListener('click', () => {
    const willOpen = localeTrigger.getAttribute('aria-expanded') !== 'true';
    closeDesktopMenus();
    localeTrigger.setAttribute('aria-expanded', String(willOpen));
    localeMenu.hidden = !willOpen;
    if (willOpen) localeMenu.querySelector('a')?.focus({ preventScroll: true });
  });

  const setMobileTop = () => {
    const bottom = Math.max(0, Math.round(header.getBoundingClientRect().bottom));
    mobileNav.style.setProperty('--mobile-nav-top', `${bottom}px`);
  };

  const openMobile = () => {
    closeDesktopMenus();
    closeLocale();
    setMobileTop();
    mobileToggle.setAttribute('aria-expanded', 'true');
    mobileLabel.textContent = 'Close';
    document.body.classList.add('nav-open');
    reveal(mobileNav);
    window.setTimeout(() => mobileNav.querySelector('a, summary')?.focus({ preventScroll: true }), 80);
  };

  const closeMobile = (returnFocus = false) => {
    mobileToggle.setAttribute('aria-expanded', 'false');
    mobileLabel.textContent = 'Menu';
    document.body.classList.remove('nav-open');
    conceal(mobileNav);
    if (returnFocus) mobileToggle.focus({ preventScroll: true });
  };

  mobileToggle.addEventListener('click', () => {
    if (mobileToggle.getAttribute('aria-expanded') === 'true') closeMobile();
    else openMobile();
  });

  mobileNav.addEventListener('click', (event) => {
    if (event.target === mobileNav) closeMobile();
    if (event.target.closest('a')) closeMobile();
  });

  mobileDetails.forEach((detail) => {
    detail.addEventListener('toggle', () => {
      if (!detail.open) return;
      mobileDetails.forEach((other) => {
        if (other !== detail) other.open = false;
      });
    });
  });

  document.addEventListener('pointerdown', (event) => {
    if (!header.contains(event.target)) {
      closeDesktopMenus();
      closeLocale();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    if (mobileToggle.getAttribute('aria-expanded') === 'true') {
      closeMobile(true);
      return;
    }
    if (localeTrigger.getAttribute('aria-expanded') === 'true') {
      closeLocale();
      localeTrigger.focus();
      return;
    }
    if (activeMenu) closeDesktopMenus(true);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1080) closeMobile();
    else closeDesktopMenus();
  });

  window.addEventListener('scroll', () => {
    if (mobileToggle.getAttribute('aria-expanded') === 'true') setMobileTop();
  }, { passive: true });
})();
