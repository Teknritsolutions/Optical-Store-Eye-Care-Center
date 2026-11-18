/* Oculis — buildless, dependency-free interactions. */
(() => {
  'use strict';
  const siteRoot = new URL('../../', document.currentScript.src);
  const assetBase = new URL('assets/', siteRoot).href;
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const safeStorage = {
    get(key) {
      try {
        return localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, value);
      } catch {
        /* Preferences remain session-local. */
      }
    }
  };
  const root = document.documentElement;
  const themeButton = $('#theme-toggle');
  const directionButton = $('#rtl-toggle');

  function syncPreferences() {
    themeButton.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
    themeButton.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    directionButton.setAttribute('aria-pressed', String(root.dir === 'rtl'));
    if (!directionButton.dataset.iconOnly) directionButton.textContent = root.dir === 'rtl' ? 'LTR' : 'RTL';
    directionButton.setAttribute('aria-label', root.dir === 'rtl' ? 'Switch to left-to-right layout' : 'Switch to right-to-left layout');
  }
  if (!root.dataset.theme) root.dataset.theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  themeButton.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    safeStorage.set('oculis-theme', root.dataset.theme);
    syncPreferences();
  });
  directionButton.addEventListener('click', () => {
    root.dir = root.dir === 'rtl' ? 'ltr' : 'rtl';
    safeStorage.set('oculis-dir', root.dir);
    syncPreferences();
  });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (!safeStorage.get('oculis-theme')) {
      root.dataset.theme = event.matches ? 'dark' : 'light';
      syncPreferences();
    }
  });
  syncPreferences();
  if ($('#primary-nav')) {
  const menuButton = $('#menu-toggle');
  const navigation = $('#primary-nav');
  const homeButton = $('.nav-home');
  const homeMenu = $('#home-menu');
  const drawerHeading = document.createElement('div');
  drawerHeading.className = 'nav-drawer-heading';
  drawerHeading.innerHTML = '<h2 id="navigation-title">Navigation</h2><button type="button" class="icon-button nav-close" aria-label="Close navigation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button>';
  navigation.prepend(drawerHeading);
  const drawerClose = $('.nav-close', navigation);
  const drawerBackdrop = document.createElement('div');
  drawerBackdrop.className = 'nav-drawer-backdrop';
  drawerBackdrop.hidden = true;
  drawerBackdrop.setAttribute('aria-hidden', 'true');
  navigation.before(drawerBackdrop);
  const inertDuringNavigation = [...document.querySelectorAll('body>main,body>footer,body>.topbar,.header-inner>.logo,.header-inner>.header-tools')];
  function setDrawerState(open) {
    drawerBackdrop.hidden = !open;
    inertDuringNavigation.forEach(element => element.inert = open);
    menuButton.inert = open;
    if (open) {
      navigation.setAttribute('role', 'dialog');
      navigation.setAttribute('aria-modal', 'true');
      navigation.setAttribute('aria-labelledby', 'navigation-title');
    } else {
      navigation.removeAttribute('role');
      navigation.removeAttribute('aria-modal');
      navigation.removeAttribute('aria-labelledby');
    }
  }
  drawerClose.addEventListener('click', () => closeMenu(true));
  drawerBackdrop.addEventListener('click', () => closeMenu(true));
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu(true);
  });

  function closeHome() {
    homeMenu.hidden = true;
    homeButton.setAttribute('aria-expanded', 'false');
  }

  function closeMenu(restoreFocus = false) {
    navigation.classList.remove('open');
    setDrawerState(false);
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Open navigation');
    document.body.classList.remove('menu-open');
    closeHome();
    if (restoreFocus) menuButton.focus();
  }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    document.body.classList.toggle('menu-open', open);
    setDrawerState(open);
    if (open) requestAnimationFrame(() => drawerClose.focus());
  });
  const homeDropdown = homeButton.closest('.home-dropdown');
  homeDropdown.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse' && matchMedia('(min-width:1200px)').matches) {
      homeMenu.hidden = false;
      homeButton.setAttribute('aria-expanded', 'true');
    }
  });
  homeDropdown.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse' && !homeDropdown.contains(document.activeElement)) closeHome();
  });
  homeDropdown.addEventListener('focusout', event => {
    if (!homeDropdown.contains(event.relatedTarget)) closeHome();
  });
  homeButton.addEventListener('click', () => {
    const open = homeMenu.hidden;
    homeMenu.hidden = !open;
    homeButton.setAttribute('aria-expanded', String(open));
  });
  homeButton.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      homeMenu.hidden = false;
      homeButton.setAttribute('aria-expanded', 'true');
      $('a', homeMenu).focus();
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.home-dropdown')) closeHome();
    if (navigation.classList.contains('open') && !event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      if (!homeMenu.hidden) {
        closeHome();
        homeButton.focus();
      } else if (navigation.classList.contains('open')) closeMenu(true);
    }
  });
  navigation.addEventListener('keydown', event => {
    if (event.key === 'Tab' && navigation.classList.contains('open')) {
      const controls = $('a,button', navigation).filter(x => x.getClientRects().length);
      const first = controls[0],
        last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      }
      if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });
  matchMedia('(min-width: 1200px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });
  }
  const header = $('.site-header');
  // Size inner-page introductions to the space below shared navigation.
  function sizePageIntro() {
    const occupied = [header, $('.topbar')]
      .reduce((height, element) => height + (element ? element.getBoundingClientRect().height : 0), 0);
    root.style.setProperty('--intro-available-height', Math.max(320, innerHeight - occupied) + 'px');
  }
  sizePageIntro();
  addEventListener('resize', sizePageIntro, { passive: true });
  document.fonts.ready.then(sizePageIntro);

  const updateScroll = () => header?.classList.toggle('scrolled', scrollY > 10);
  addEventListener('scroll', updateScroll, {
    passive: true
  });
  updateScroll();
  const params = new URLSearchParams(location.search);
  // Filter the already rendered, accessible catalogue without rebuilding its markup.
  if ($('#product-grid')) {
    const data = window.OCULIS_PRODUCTS;
    const grid = $('#product-grid');
    const controls = {
      search: $('#product-search'),
      category: $('#filter-category'),
      style: $('#filter-style'),
      lens: $('#filter-lens'),
      sort: $('#product-sort')
    };
    for (const name of ['category', 'style', 'lens'])
      if (params.get(name)) controls[name].value = params.get(name);

    function filterProducts() {
      const query = controls.search.value.trim().toLowerCase();
      const matching = data.filter(p => (!query || `${p.name} ${p.color} ${p.style} ${p.category}`.toLowerCase().includes(query)) && ['category', 'style', 'lens'].every(k => !controls[k].value || p[k] === controls[k].value));
      if (controls.sort.value === 'price-asc') matching.sort((a, b) => a.price - b.price);
      if (controls.sort.value === 'price-desc') matching.sort((a, b) => b.price - a.price);
      if (controls.sort.value === 'name') matching.sort((a, b) => a.name.localeCompare(b.name));
      const ids = new Set(matching.map(p => p.id));
      $$('.product-card', grid).forEach(card => {
        card.hidden = !ids.has(card.dataset.id);
      });
      matching.forEach(p => grid.append($(`[data-id="${p.id}"]`, grid)));
      $('#product-count').textContent = `${matching.length} ${matching.length === 1 ? 'frame' : 'frames'}`;
      $('#product-empty').hidden = matching.length > 0;
      $$('[data-preset]').forEach(button => {
        const active = controls[button.dataset.filter].value === button.dataset.preset;
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
      });
    }
    Object.values(controls).forEach(control => control.addEventListener(control.type === 'search' ? 'input' : 'change', filterProducts));
    $('#reset-products').addEventListener('click', () => {
      Object.entries(controls).forEach(([key, control]) => {
        control.value = key === 'sort' ? 'featured' : '';
      });
      filterProducts();
    });
    $$('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const control = controls[button.dataset.filter];
      control.value = control.value === button.dataset.preset ? '' : button.dataset.preset;
      filterProducts();
      $('#catalogue').scrollIntoView({
        behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'
      });
    }));
    filterProducts();
    if (params.has('style') || params.has('lens') || params.has('category')) {
      requestAnimationFrame(() => $('#catalogue').scrollIntoView({ behavior: 'instant', block: 'start' }));
    }
  } else {
    $$('[data-preset]').forEach(button => button.addEventListener('click', () => {
      location.href = `${new URL("pages/products.html", siteRoot).href}?${button.dataset.filter}=${encodeURIComponent(button.dataset.preset)}`;
    }));
  }
  // Manual carousel: no auto-advance, preserving reading time and reduced-motion preferences.
  if ($('#testimonials')) {
    const track = $('#testimonials');
    const stories = $$('.quote-card', track);
    const mobile = matchMedia('(max-width: 640px)');
    let position = 0;
    const updateStories = () => {
      const count = mobile.matches ? 1 : (matchMedia('(max-width: 820px)').matches ? 2 : 3);
      stories.forEach(story => {
        story.hidden = true;
      });
      for (let i = 0; i < count; i++) {
        const story = stories[(position + i) % stories.length];
        story.hidden = false;
        track.append(story);
      }
      $('#testimonial-status').textContent = `Story ${position + 1} of ${stories.length}`;
    };
    $('#testimonial-prev').addEventListener('click', () => {
      position = (position - 1 + stories.length) % stories.length;
      updateStories();
    });
    $('#testimonial-next').addEventListener('click', () => {
      position = (position + 1) % stories.length;
      updateStories();
    });
    addEventListener('resize', updateStories);
    updateStories();
  }
  // Brand directory.
  if ($('#brand-grid')) {
    const updateBrands = () => {
      const query = $('#brand-search').value.trim().toLowerCase(),
        material = $('#brand-filter').value;
      let count = 0;
      $$('#brand-grid .brand-card').forEach(card => {
        const show = card.dataset.name.includes(query) && (!material || card.dataset.material === material);
        card.hidden = !show;
        if (show) count++;
      });
      $('#brand-count').textContent = `${count} ${count === 1 ? 'label' : 'labels'}`;
      $('#brand-empty').hidden = count > 0;
    };
    $('#brand-search').addEventListener('input', updateBrands);
    $('#brand-filter').addEventListener('change', updateBrands);
  }
  // Gallery and routed product overview.
  if ($('.gallery-main')) {
    const selected = window.OCULIS_PRODUCTS.find(p => p.id === params.get('id'));
    if (selected && selected.id !== 'harper') {
      $('#detail-name').textContent = selected.name;
      $('#detail-description').textContent = `${selected.color}. A considered ${selected.style.toLowerCase()} silhouette for your everyday perspective. Explore this original demo frame and ask about your lens options.`;
      $('#detail-price').innerHTML = `$${selected.price} <span class="small">Frame-only demo price</span>`;
      $('#detail-color').textContent = selected.color;
      $('#detail-material').textContent = /titanium|metal|silver/.test(selected.color.toLowerCase()) ? 'Metal' : 'Acetate';
      const main = $('.gallery-main img');
      main.src = `${assetBase}images/${selected.image}.webp`;
      main.removeAttribute('srcset');
      main.alt = `${selected.name} — ${selected.color}`;
      // The three alternate views represent the default Harper frame only.
      $('.gallery-thumbs').hidden = true;
      document.title = `${selected.name} — frame details | Oculis`;
    }
    $$('.gallery-thumb').forEach(button => button.addEventListener('click', () => {
      const main = $('.gallery-main img');
      main.src = `${assetBase}images/${button.dataset.gallery}.webp`;
      main.srcset = `${assetBase}images/${button.dataset.gallery}-480.webp 480w, ${assetBase}images/${button.dataset.gallery}.webp 1200w`;
      main.alt = button.getAttribute('aria-label').replace('Show ', 'Honey acetate eyeglasses — ');
      $$('.gallery-thumb').forEach(b => {
        b.classList.toggle('selected', b === button);
        b.setAttribute('aria-pressed', String(b === button));
      });
    }));
  }
  // Journal filters and load-more interaction.
  if ($('#blog-grid')) {
    let category = 'All articles',
      limit = 3;
    const articles = $$('#blog-grid .article-card');

    function updateBlog() {
      const query = $('#blog-search').value.trim().toLowerCase();
      const matches = articles.filter((card, i) => {
        const a = window.OCULIS_ARTICLES[i];
        return (category === 'All articles' || a.category === category) && `${a.title} ${a.desc} ${a.category}`.toLowerCase().includes(query);
      });
      articles.forEach(card => {
        card.hidden = true;
      });
      matches.slice(0, limit).forEach(card => {
        card.hidden = false;
      });
      $('#blog-count').textContent = `${matches.length} ${matches.length === 1 ? 'story' : 'stories'}`;
      $('#blog-empty').hidden = matches.length > 0;
      $('#blog-more').hidden = matches.length <= limit;
    }
    $$('[data-blog-category]').forEach(button => button.addEventListener('click', () => {
      category = button.dataset.blogCategory;
      limit = 3;
      $$('[data-blog-category]').forEach(b => {
        b.classList.toggle('active', b === button);
        b.setAttribute('aria-pressed', String(b === button));
      });
      updateBlog();
      $('#blog-grid').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
    }));
    $('#blog-search').addEventListener('input', () => {
      limit = 3;
      updateBlog();
    });
    $('#blog-more').addEventListener('click', () => {
      limit += 3;
      updateBlog();
    });
    updateBlog();
  }
  if ($('#article-title')) {
    const articles = window.OCULIS_ARTICLES;
    const article = articles.find(a => a.id === params.get('id')) || articles[0];
    const stories = {
      'comfortable-fit': [
        ['Start with the bridge.', 'A comfortable bridge helps your glasses sit without pinching or sliding. Different nose-pad and bridge designs suit different faces. Ask for a fitting rather than choosing from appearance alone.'],
        ['Consider the width.', 'Your frame should feel balanced across your face. The temples should sit comfortably without pressing into the sides of your head.'],
        ['Notice the small details.', 'Pay attention to the fit behind your ears and the position of the lenses. A careful adjustment may make a noticeable difference in comfort.'],
        ['Make room for professional guidance.', 'Bring your glasses to an optical professional if they begin to feel loose or uneven. Avoid bending frames yourself.']
      ],
      'lens-guide': [
        ['Start with your everyday needs.', 'Tell your eye-care professional how you spend your day, from reading and computer work to time outdoors. A useful lens discussion begins with your prescription and routine.'],
        ['Understand the options.', 'Single vision lenses provide one prescription across the lens. Progressive designs provide a range of viewing distances. Suitability depends on your prescription and fitting.'],
        ['Ask about finishes.', 'Discuss anti-reflective coatings, scratch-resistant treatments and appropriate UV protection. Ask what each option is intended to do and how it should be cared for.'],
        ['Choose with guidance.', 'A personalised lens recommendation should account for your eyes, frame and daily needs. This general article cannot replace an individual assessment.']
      ],
      'screen-breaks': [
        ['Look beyond your screen.', 'Long periods of concentrated near work can feel tiring. Build regular opportunities to pause and look farther away into your workday.'],
        ['Consider the light.', 'Adjust your screen and surroundings to reduce distracting glare. A comfortable screen position and readable text can make a desk feel easier to use.'],
        ['Make breaks part of the routine.', 'Use natural transitions between tasks as reminders to take a short pause. Blink normally and make room for movement throughout your day.'],
        ['Ask about persistent discomfort.', 'If discomfort continues, speak with an eye-care professional. A professional assessment can consider your vision needs and working environment.']
      ],
      'sun-protection': [
        ['Start with UV protection.', 'When choosing sunglasses, ask about verified UV protection rather than relying on the darkness of the tint. Lens colour alone does not establish protection.'],
        ['Consider fit and coverage.', 'Look for a comfortable fit and a shape that suits your outdoor activities. Discuss how the frame coverage and lens design work together.'],
        ['Ask about your prescription.', 'Prescription sunglasses and other sun lens options may suit different needs. Ask an optical professional which options are appropriate for you.'],
        ['Care for your sun lenses.', 'Use a protective case and follow the lens supplier’s cleaning guidance. Keep your sunglasses away from excessive heat.']
      ]
    };
    if (article) {
      $('#article-title').textContent = article.title;
      $('#article-description').textContent = article.desc;
      $('#article-category').textContent = `${article.category} / THE OCULIS JOURNAL`;
      $('#article-date').textContent = article.date;
      $('#article-read').textContent = article.read;
      document.title = `${article.title} | Oculis`;
      $('#article-breadcrumb').textContent = article.title;
      $('meta[name="description"]').content = article.desc;
      const heroImage = $('.signature-media > img');
      heroImage.src = assetBase + 'images/' + article.image + '.webp';
      heroImage.srcset = assetBase + 'images/' + article.image + '-480.webp 480w, ' + assetBase + 'images/' + article.image + '.webp 1200w';
      heroImage.alt = article.title;
      const index = articles.indexOf(article);
      const navigation = $$('.article-navigation a');
      navigation[0].href = 'blog-details.html?id=' + articles[(index + articles.length - 1) % articles.length].id;
      navigation[1].href = 'blog-details.html?id=' + articles[(index + 1) % articles.length].id;
      const related = articles.filter(a => a.id !== article.id).slice(0,3);
      $$('.article-card').forEach((card,i) => {
        const story = related[i];
        if (!story) return;
        $$('a',card).forEach(a => a.href = 'blog-details.html?id=' + story.id);
        const image = $('img',card);
        image.src = assetBase + 'images/' + story.image + '.webp';
        image.srcset = assetBase + 'images/' + story.image + '-480.webp 480w, ' + assetBase + 'images/' + story.image + '.webp 1200w';
        image.alt = story.title;
        $('h3 a',card).textContent = story.title;
        $('.article-body > p:not(.eyebrow)',card).textContent = story.desc;
        $('.eyebrow',card).textContent = story.category + ' - ' + story.read;
      });
      if (stories[article.id]) {
        const checklist = $('#article-checklist');
        checklist.replaceChildren();
        stories[article.id].forEach(([heading]) => {
          const item = document.createElement('li');
          item.textContent = heading;
          checklist.append(item);
        });
      }

      if (stories[article.id]) {
        const ids = ['clean', 'store', 'fit', 'routine'];
        const prose = $('#article-prose');
        prose.replaceChildren();
        stories[article.id].forEach(([heading, paragraph], i) => {
          const h = document.createElement('h2');
          h.id = ids[i];
          h.textContent = heading;
          const p = document.createElement('p');
          p.textContent = paragraph;
          prose.append(h, p);
          const nav = $(`.article-sidebar a[href="#${ids[i]}"]`);
          if (nav) nav.textContent = heading;
        });
        const note = document.createElement('p');
        note.className = 'small';
        note.textContent = 'Original general information for a fictional demonstration journal. Speak with an eye-care professional for individual advice.';
        prose.append(note);
      }
    }
  }
  // Integration boundary: replace a handler with your own API adapter. No personal data is persisted.
  window.OculisForms = window.OculisForms || {
    booking: null,
    contact: null,
    newsletter: null
  };
  const today = new Date();
  const localDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  if ($('#date')) $('#date').min = localDate;
  if ($('#subject') && params.get('subject')) {
    const option = [...$('#subject').options].find(o => o.value === params.get('subject'));
    if (option) $('#subject').value = option.value;
  }
  $$('.demo-form').forEach(form => {
    const inputs = $$('input,select,textarea', form);

    function validate(input) {
      let message = '';
      const value = input.value.trim();
      if (input.required && !value) message = 'Please complete this field.';
      else if (input.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) message = 'Enter a valid email address.';
      else if (input.name === 'name' && value.length < 2) message = 'Enter at least two characters.';
      else if (input.type === 'tel' && value && (!/^[+()\d\s.-]+$/.test(value) || value.replace(/\D/g, '').length < 7 || value.replace(/\D/g, '').length > 15)) message = 'Enter a valid phone number (7–15 digits).';
      else if (input.type === 'date' && value && value < localDate) message = 'Choose today or a future date.';
      const error = document.getElementById(`${input.id}-error`);
      if (error) error.textContent = message;
      input.setAttribute('aria-invalid', String(Boolean(message)));
      if (error) input.setAttribute('aria-describedby', error.id);
      return !message;
    }
    inputs.forEach(input => {
      input.addEventListener('blur', () => validate(input));
      input.addEventListener('input', () => {
        if (input.getAttribute('aria-invalid') === 'true') validate(input);
      });
    });
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const results = inputs.map(validate);
      const status = $('.form-status', form);
      status.textContent = '';
      status.classList.remove('has-message');
      if (results.some(result => !result)) {
        inputs[results.indexOf(false)].focus();
        return;
      }
      const handler = window.OculisForms[form.dataset.kind];
      const submit = $('button[type="submit"]', form);
      if (typeof handler === 'function') {
        submit.disabled = true;
        submit.setAttribute('aria-busy', 'true');
        try {
          const response = await handler(Object.fromEntries(new FormData(form)));
          status.textContent = response && response.message ? response.message : 'Your request has been received by the connected service.';
          form.reset();
        } catch {
          status.textContent = 'Your request could not be sent. Please try again or contact the store.';
        } finally {
          submit.disabled = false;
          submit.removeAttribute('aria-busy');
        }
      } else {
        status.textContent = form.dataset.kind === 'booking' ? `Demo request preview complete for ${$('#date', form).value} at ${$('#time', form).value}. No appointment has been booked, and no information was sent or stored.` : form.dataset.kind === 'newsletter' ? 'Demo subscription preview complete. Your email has not been stored or sent.' : 'Demo enquiry preview complete. Your message has not been sent or stored.';
        form.reset();
        inputs.forEach(input => input.removeAttribute('aria-invalid'));
      }
      status.classList.add('has-message');
      status.tabIndex = -1;
      status.focus({
        preventScroll: true
      });
    });
  });
})();
