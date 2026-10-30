/* Oconomowoc Garage Door — motion & interactions */
(() => {
  const d = document, root = d.documentElement;
  root.classList.remove('no-js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];

  /* split headings into words for the rise-in reveal */
  $$('[data-words]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
            const w = d.createElement('span'); w.className = 'w';
            const s = d.createElement('span'); s.textContent = part; s.style.setProperty('--i', i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
  });

  /* reveal on scroll */
  const targets = $$('[data-reveal],[data-words]');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    targets.forEach(t => io.observe(t));
  } else targets.forEach(t => t.classList.add('in'));

  /* count up */
  const counters = $$('[data-count]');
  const cio = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return;
    const el = en.target, end = +el.dataset.count, t0 = performance.now(), dur = 1400;
    const step = t => { const p = Math.min((t - t0) / dur, 1); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    if (!reduce) requestAnimationFrame(step);
    cio.unobserve(el);
  }), { threshold: .6 });
  counters.forEach(c => cio.observe(c));

  /* scroll-driven: progress bar, header state, parallax, steps line, back-to-top ring */
  const header = $('.header'), totop = $('.totop');
  const par = $$('[data-parallax]'), parEl = $$('[data-parallax-el]'), stepLists = $$('.steps');
  let ticking = false;
  const onScroll = () => {
    const y = scrollY, h = root.scrollHeight - innerHeight, p = h > 0 ? y / h : 0;
    root.style.setProperty('--p', p.toFixed(4));
    header && header.classList.toggle('is-scrolled', y > 30);
    totop && totop.classList.toggle('show', y > 700);
    if (!reduce) {
      par.forEach(img => {
        const r = img.parentElement.getBoundingClientRect();
        if (r.bottom < -100 || r.top > innerHeight + 100) return;
        const lim = r.height * .08, off = Math.max(-lim, Math.min(lim, (r.top + r.height / 2 - innerHeight / 2) * -(+img.dataset.parallax)));
        img.style.transform = `translate3d(0,${off.toFixed(1)}px,0) scale(1.06)`;
      });
      parEl.forEach(el => {
        const r = el.getBoundingClientRect();
        el.style.transform = `translate3d(0,${((r.top - innerHeight / 2) * +el.dataset.parallaxEl).toFixed(1)}px,0)`;
      });
    }
    stepLists.forEach(l => {
      const r = l.getBoundingClientRect();
      const sp = Math.min(Math.max((innerHeight * .7 - r.top) / r.height, 0), 1);
      l.style.setProperty('--sp', sp.toFixed(3));
    });
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();

  /* cursor glow on cards + magnetic buttons */
  if (matchMedia('(hover:hover)').matches && !reduce) {
    $$('[data-glow]').forEach(c => c.addEventListener('pointermove', ev => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--gx', ev.clientX - r.left + 'px'); c.style.setProperty('--gy', ev.clientY - r.top + 'px');
    }));
    $$('[data-magnetic]').forEach(b => {
      b.addEventListener('pointermove', ev => {
        const r = b.getBoundingClientRect(), x = ev.clientX - r.left, y = ev.clientY - r.top;
        b.style.setProperty('--mx', x + 'px'); b.style.setProperty('--my', y + 'px');
        b.style.transform = `translate(${((x - r.width / 2) * .12).toFixed(1)}px,${((y - r.height / 2) * .2).toFixed(1)}px)`;
      });
      b.addEventListener('pointerleave', () => { b.style.transform = ''; });
    });
  }

  /* mobile nav + dropdowns */
  const burger = $('.burger'), nav = $('nav');
  burger && burger.addEventListener('click', () => {
    const open = burger.getAttribute('aria-expanded') !== 'true';
    burger.setAttribute('aria-expanded', open); nav.classList.toggle('open', open);
    d.body.style.overflow = open ? 'hidden' : '';
  });
  $$('.has-dd>button').forEach(btn => btn.addEventListener('click', () => {
    const li = btn.parentElement, open = !li.classList.contains('open');
    $$('.has-dd.open').forEach(o => { if (o !== li) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); } });
    li.classList.toggle('open', open); btn.setAttribute('aria-expanded', open);
  }));
  d.addEventListener('click', ev => { if (!ev.target.closest('.has-dd') && innerWidth > 1020) $$('.has-dd.open').forEach(o => o.classList.remove('open')); });
  $$('nav a').forEach(a => a.addEventListener('click', () => { if (nav.classList.contains('open')) burger.click(); }));
  d.addEventListener('keydown', ev => { if (ev.key === 'Escape') { $$('.has-dd.open').forEach(o => o.classList.remove('open')); if (nav && nav.classList.contains('open')) burger.click(); } });

  /* service filters */
  $$('.filter').forEach(f => f.addEventListener('click', () => {
    $$('.filter').forEach(x => { x.classList.toggle('is-on', x === f); x.setAttribute('aria-selected', x === f); });
    const cat = f.dataset.cat;
    f.closest('.sec').querySelector('.bento').classList.toggle('is-filtered', cat !== 'all');
    $$('.bento .svc').forEach((c, i) => {
      const show = cat === 'all' || c.dataset.cat === cat;
      c.classList.toggle('is-hidden', !show);
      c.classList.toggle('svc--big', show && cat === 'all' && i === 0);
      if (show && !reduce) c.animate([{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }], { duration: 500, delay: i * 25, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'backwards' });
    });
  }));

  /* faq: one open at a time per list */
  $$('.faq').forEach(list => list.addEventListener('toggle', ev => {
    if (ev.target.open) $$('details', list).forEach(x => { if (x !== ev.target) x.open = false; });
  }, true));

  /* quote form */
  $$('.quote-form').forEach(form => form.addEventListener('submit', async ev => {
    ev.preventDefault();
    if (form.company && form.company.value) return;
    let ok = true;
    ['name', 'phone', 'zip'].forEach(n => {
      const f = form[n], bad = !f.value.trim() || (n === 'phone' && f.value.replace(/\D/g, '').length < 10);
      f.parentElement.classList.toggle('err', bad); if (bad) ok = false;
    });
    if (!ok) { form.querySelector('.err input').focus(); return; }
    const ep = form.dataset.endpoint, btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    if (ep) {
      try { await fetch(ep, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) }); } catch (e) { /* still confirm */ }
    }
    form.closest('.quote').classList.add('done');
  }));
  $$('.field input').forEach(i => i.addEventListener('input', () => i.parentElement.classList.remove('err')));

  $$('[data-year]').forEach(y => y.textContent = new Date().getFullYear());
})();
