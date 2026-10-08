'use strict';

// Os textos e os links funcionam sem JavaScript. Os controles abaixo são opcionais.
const toolbar = document.querySelector('.lab-toolbar');
if (toolbar) {
  toolbar.hidden = false;
  const rows = [...document.querySelectorAll('.lab-row')];
  const filters = [...toolbar.querySelectorAll('[data-filter]')];
  filters.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.filter;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    let count = 0;
    rows.forEach(row => {
      row.hidden = category !== 'todos' && row.dataset.category !== category;
      if (!row.hidden) count++;
    });
    document.getElementById('lab-count').textContent = `${count} ${count === 1 ? 'projeto' : 'projetos'}`;
  }));
}

for (const gallery of document.querySelectorAll('[data-gallery]')) {
  const media = JSON.parse(gallery.dataset.gallery);
  const picture = gallery.querySelector('.gallery-image');
  const caption = gallery.querySelector('.gallery-caption');
  const counter = gallery.querySelector('.gallery-counter');
  const original = gallery.querySelector('.gallery-original');
  const toggle = gallery.querySelector('.motion-toggle');
  const thumbs = [...gallery.querySelectorAll('[data-slide]')];
  let index = 0;
  let playing = false;
  const assetUrl = src => `../${src.replace(/^\.\//, '')}`;
  const isAnimated = item => /\.gif$/i.test(item.src);

  function show(next) {
    index = (next + media.length) % media.length;
    const item = media[index];
    playing = false;
    picture.src = assetUrl(item.poster || item.src);
    picture.alt = item.alt;
    caption.textContent = item.legenda;
    counter.textContent = `${String(index + 1).padStart(2, '0')} / ${String(media.length).padStart(2, '0')}`;
    original.href = assetUrl(item.poster || item.src);
    toggle.hidden = !isAnimated(item);
    toggle.textContent = 'Reproduzir demonstração';
    toggle.setAttribute('aria-pressed', 'false');
    thumbs.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
  }

  thumbs.forEach(button => button.addEventListener('click', () => show(Number(button.dataset.slide))));
  gallery.querySelectorAll('[data-direction]').forEach(button => button.addEventListener('click', () => show(index + Number(button.dataset.direction))));
  toggle.addEventListener('click', () => {
    const item = media[index];
    playing = !playing;
    picture.src = assetUrl(playing ? item.src : item.poster);
    toggle.textContent = playing ? 'Parar demonstração' : 'Reproduzir demonstração';
    toggle.setAttribute('aria-pressed', String(playing));
  });
  // GIFs só são carregados após uma ação explícita, inclusive com movimento reduzido.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && playing) show(index);
  });
  gallery.querySelector('.gallery-controls').hidden = false;
  show(0);
}
