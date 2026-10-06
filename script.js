const PROJECTS_URL = "./data/projetos.json";
const CATEGORY_LABELS = { esporte: "Esporte", dados: "Dados", trabalho: "Aplicações" };
const CATEGORY_ORDER = ["esporte", "dados", "trabalho"];
const FEATURED_IDS = ["modelo-de-chatbot-configuravel", "scout-trainer", "mapa-de-valores-imobiliarios-em-belo-horizonte"];

const grid = document.querySelector("#projects-grid");
const countLabel = document.querySelector("#project-count");
const dialog = document.querySelector("#project-dialog");
const dialogContent = document.querySelector("#project-dialog-content");
const filterButtons = [...document.querySelectorAll("[data-filter]")];
let projects = [];
let activeFilter = "todos";

createPortfolio();
document.querySelector("#year").textContent = new Date().getFullYear();

async function createPortfolio() {
  try {
    const response = await fetch(PROJECTS_URL);
    if (!response.ok) throw new Error(`Erro ${response.status} ao carregar os projetos.`);
    const data = await response.json();
    if (!Array.isArray(data) || !data.length) throw new Error("A lista de projetos está vazia.");
    const ids = new Set();
    data.forEach((project) => {
      if (!project.id || !project.titulo || !CATEGORY_LABELS[project.categoria] || ids.has(project.id)) {
        throw new Error("Há um projeto com dados incompletos ou identificador repetido.");
      }
      ids.add(project.id);
    });
    projects = data.sort((a, b) => CATEGORY_ORDER.indexOf(a.categoria) - CATEGORY_ORDER.indexOf(b.categoria) || Number(a.prioridade ?? 99) - Number(b.prioridade ?? 99));
    updateCounts();
    renderProjects();
  } catch (error) {
    grid.innerHTML = `<div class="load-error"><h3>Não foi possível carregar os projetos</h3><p>${escapeHtml(error.message)}</p><p>Se você abriu os arquivos no computador, use um servidor HTTP local.</p></div>`;
    countLabel.textContent = "Projetos indisponíveis";
    console.error(error);
  } finally {
    grid.setAttribute("aria-busy", "false");
  }
}

function updateCounts() {
  document.querySelectorAll("[data-count]").forEach((element) => {
    const category = element.dataset.count;
    element.textContent = category === "todos" ? projects.length : projects.filter((project) => project.categoria === category).length;
  });
}

function renderProjects() {
  const visible = activeFilter === "todos"
    ? [...projects].sort((a, b) => featuredRank(a) - featuredRank(b))
    : projects.filter((project) => project.categoria === activeFilter);
  grid.innerHTML = visible.map(renderProjectCard).join("");
  countLabel.textContent = `${visible.length} ${visible.length === 1 ? "projeto" : "projetos"}`;
}

function featuredRank(project) {
  const index = FEATURED_IDS.indexOf(project.id);
  return index === -1 ? FEATURED_IDS.length : index;
}

function renderProjectCard(project) {
  const cover = getCover(project);
  const technologies = Array.isArray(project.tecnologias) ? project.tecnologias.slice(0, 3) : [];
  const imageCount = Array.isArray(project.imagens) ? project.imagens.filter((item) => item?.src).length : 0;
  return `
    <article class="project-card">
      <button type="button" class="project-card__button" data-project-id="${escapeAttribute(project.id)}" aria-label="Conhecer o projeto ${escapeAttribute(project.titulo)}">
        <span class="project-card__media">
          ${cover ? `<img src="${escapeAttribute(cover.src)}" alt="" loading="lazy" decoding="async">` : `<span class="project-card__placeholder" aria-hidden="true">${escapeHtml(project.titulo.slice(0, 2).toUpperCase())}</span>`}
          ${imageCount > 1 ? `<span class="project-card__image-count">${imageCount} imagens</span>` : ""}
        </span>
        <span class="project-card__body">
          <span class="project-card__meta"><span>${escapeHtml(CATEGORY_LABELS[project.categoria])}</span><span class="project-card__meta-separator" aria-hidden="true">•</span><span>${escapeHtml(project.status || "Projeto")}</span></span>
          <span class="project-card__title">${escapeHtml(project.titulo)}</span>
          <span class="project-card__description">${escapeHtml(project.descricaoCurta || project.subtitulo || "")}</span>
          <span class="project-card__tags">${technologies.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</span>
          <span class="project-card__footer">Conhecer projeto <span aria-hidden="true">↗</span></span>
        </span>
      </button>
    </article>`;
}

function getCover(project) {
  if (project.capa?.src && isSafeMediaUrl(project.capa.src)) return project.capa;
  return Array.isArray(project.imagens) ? project.imagens.find((item) => item?.src && isSafeMediaUrl(item.src)) : null;
}

filterButtons.forEach((button) => button.addEventListener("click", () => {
  activeFilter = button.dataset.filter;
  filterButtons.forEach((item) => {
    const active = item === button;
    item.classList.toggle("is-active", active);
    item.setAttribute("aria-pressed", String(active));
  });
  renderProjects();
}));

grid.addEventListener("click", (event) => {
  const button = event.target.closest("[data-project-id]");
  if (!button) return;
  const project = projects.find((item) => item.id === button.dataset.projectId);
  if (project) openProject(project);
});

function openProject(project) {
  const images = Array.isArray(project.imagens) ? project.imagens.filter((item) => item?.src && isSafeMediaUrl(item.src)) : [];
  if (!images.length && getCover(project)) images.push(getCover(project));
  const technologies = Array.isArray(project.tecnologias) ? project.tecnologias : [];
  const learnings = Array.isArray(project.aprendizados) ? project.aprendizados : [];
  const links = [
    { url: project.linkDemo, label: "Abrir demonstração", primary: true },
    { url: project.linkDownload, label: project.linkDownloadLabel || "Baixar versão", primary: true },
    { url: project.linkRepositorio, label: "Ver código no GitHub", primary: false }
  ].filter((link) => isSafeExternalUrl(link.url));

  dialogContent.innerHTML = `
    <div class="detail-header"><p class="eyebrow"><span class="eyebrow__line" aria-hidden="true"></span> ${escapeHtml(CATEGORY_LABELS[project.categoria])}</p><p class="detail-header__status">${escapeHtml(project.status || "Projeto")}</p><h2 id="dialog-title">${escapeHtml(project.titulo)}</h2><p class="detail-header__lead">${escapeHtml(project.subtitulo || project.descricaoCurta || "")}</p></div>
    ${renderGallery(images, project)}
    <div class="detail-content"><div class="detail-content__main"><section aria-labelledby="story-title"><h3 id="story-title">Sobre o projeto</h3>${renderParagraphs(project.descricaoCompleta || project.descricaoCurta || "")}</section>${learnings.length ? `<section aria-labelledby="learnings-title"><h3 id="learnings-title">O que aprendi</h3><ul class="learning-list">${learnings.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>` : ""}</div><aside class="detail-content__aside">${technologies.length ? `<section aria-labelledby="tech-title"><h3 id="tech-title">Tecnologias e métodos</h3><div class="detail-tags">${technologies.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div></section>` : ""}${links.length ? `<section aria-labelledby="links-title"><h3 id="links-title">Explore</h3><div class="detail-links">${links.map((link) => `<a class="button ${link.primary ? "button--primary" : "button--outline"}" href="${escapeAttribute(link.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label)} <span aria-hidden="true">↗</span></a>`).join("")}</div></section>` : ""}</aside></div>`;

  dialog._galleryImages = images;
  dialog.showModal();
  document.body.classList.add("dialog-open");
}


function renderGallery(images, project) {
  if (!images.length) return "";
  const first = images[0];
  const thumbs = images.length > 1
    ? `<div class="detail-gallery__thumbs" role="group" aria-label="Selecionar imagem">${images.map((image, index) => `<button type="button" class="gallery-thumb${index === 0 ? " is-active" : ""}" data-image-index="${index}" aria-label="Mostrar imagem ${index + 1}: ${escapeAttribute(image.legenda || image.alt || project.titulo)}" aria-pressed="${index === 0}"><img src="${escapeAttribute(displayMediaSrc(image))}" alt="" loading="lazy"></button>`).join("")}</div>`
    : "";
  return `<section class="detail-gallery" aria-label="Imagens do projeto"><figure class="detail-gallery__main"><img id="gallery-main-image" src="${escapeAttribute(displayMediaSrc(first))}" alt="${escapeAttribute(first.alt || project.titulo)}"><figcaption id="gallery-caption">${escapeHtml(first.legenda || "Imagem do projeto")}</figcaption></figure>${thumbs}<a id="gallery-open" class="gallery-open" href="${escapeAttribute(first.src)}" target="_blank" rel="noopener noreferrer">Abrir imagem em tamanho original ↗</a></section>`;
}

function displayMediaSrc(image) {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches && image.src.toLowerCase().endsWith(".gif") && isSafeMediaUrl(image.poster)) return image.poster;
  return image.src;
}

dialogContent.addEventListener("click", (event) => {
  const button = event.target.closest("[data-image-index]");
  if (!button) return;
  const image = dialog._galleryImages?.[Number(button.dataset.imageIndex)];
  if (!image) return;
  const main = document.querySelector("#gallery-main-image");
  main.src = displayMediaSrc(image);
  main.alt = image.alt || "Imagem do projeto";
  document.querySelector("#gallery-caption").textContent = image.legenda || "Imagem do projeto";
  document.querySelector("#gallery-open").href = image.src;
  dialogContent.querySelectorAll("[data-image-index]").forEach((item) => {
    const active = item === button;
    item.classList.toggle("is-active", active);
    item.setAttribute("aria-pressed", String(active));
  });
});

document.querySelector("#dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
dialog.addEventListener("close", () => { document.body.classList.remove("dialog-open"); dialogContent.innerHTML = ""; });

function renderParagraphs(value) {
  return String(value).replace(/\\n/g, "\n").split(/\n\s*\n/).map((paragraph) => paragraph.trim()).filter(Boolean).map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("");
}

function isSafeExternalUrl(value) {
  if (!value) return false;
  try { return new URL(value).protocol === "https:"; } catch { return false; }
}

function isSafeMediaUrl(value) {
  if (!value) return false;
  try { const url = new URL(value, location.href); return url.protocol === "https:" || url.origin === location.origin; } catch { return false; }
}

function escapeHtml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}
function escapeAttribute(value) { return escapeHtml(value).replaceAll("`", "&#96;"); }
