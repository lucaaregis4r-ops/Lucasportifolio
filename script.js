const PROJECTS_URL = "./data/projetos.json";

const CATEGORIES = [
  {
    id: "software",
    titulo: "Desenvolvimento de Software & Aplicações",
    descricao: "Produtos, jogos e ferramentas construídos para experiências e fluxos de trabalho específicos."
  },
  {
    id: "dados",
    titulo: "Dados & Analytics",
    descricao: "Projetos de tratamento, modelagem e visualização de dados para apoiar análises."
  },
  {
    id: "automacao",
    titulo: "Automação, IA & Sistemas de Dados",
    descricao: "Sistemas locais e pipelines que integram fontes, regras, revisão humana e automação."
  }
];

const introContent = {
  kicker: "Apresentação",
  titulo: "Desenvolvimento, dados e automação",
  foto: { src: "./assets/imagens/foto-lucas.jpg", alt: "Foto de Lucas Regis" },
  paragrafos: [
    "Olá, meu nome é Lucas Regis.",
    "Sou psicólogo formado pela UFMG e venho direcionando minha trajetória profissional para tecnologia, desenvolvimento de software e análise de dados.",
    "Construo aplicações, visualizações e sistemas de dados a partir de problemas concretos. Minha experiência no esporte aparece em parte dos projetos, mas o foco do portfólio está nas competências transferíveis: programação, modelagem, integração de fontes, automação, análise e comunicação de informações.",
    "Neste espaço, reúno projetos em diferentes estágios de desenvolvimento e documento com clareza o que já está implementado, o que está em evolução e quais decisões técnicas orientaram cada solução.",
    "Estou aberto a oportunidades em TI, desenvolvimento de software e dados."
  ],
  contato: { label: "Contato", email: "lucaaregis4r@gmail.com" }
};

const projectsList = document.querySelector("#projects-list");
const projectDetails = document.querySelector("#project-details");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

document.addEventListener("DOMContentLoaded", () => {
  renderIntro();
  loadProjects();
});

async function loadProjects() {
  try {
    const response = await fetch(PROJECTS_URL);
    if (!response.ok) throw new Error(`Falha ao carregar os projetos (${response.status}).`);

    const projects = await response.json();
    validateProjects(projects);
    renderProjectCategories(projects);
  } catch (error) {
    renderProjectsError(error);
    console.error(error);
  } finally {
    projectsList.setAttribute("aria-busy", "false");
  }
}

function validateProjects(projects) {
  if (!Array.isArray(projects) || projects.length === 0) {
    throw new Error("O arquivo JSON não contém uma lista válida de projetos.");
  }

  const allowedCategories = new Set(CATEGORIES.map((category) => category.id));
  const invalidProject = projects.find((project) => !project.id || !project.titulo || !allowedCategories.has(project.categoria));
  if (invalidProject) throw new Error("Há um projeto sem título, identificador ou categoria válida.");
}

function renderProjectCategories(projects) {
  projectsList.innerHTML = CATEGORIES.map((category) => {
    const categoryProjects = projects
      .filter((project) => project.categoria === category.id)
      .sort((a, b) => Number(a.prioridade ?? 999) - Number(b.prioridade ?? 999));

    if (!categoryProjects.length) return "";

    return `
      <section id="${category.id}" class="project-category" aria-labelledby="${category.id}-title">
        <div class="category-heading">
          <p class="category-heading__count">${categoryProjects.length} ${categoryProjects.length === 1 ? "projeto" : "projetos"}</p>
          <h3 id="${category.id}-title">${escapeHtml(category.titulo)}</h3>
          <p>${escapeHtml(category.descricao)}</p>
        </div>
        <div class="projects-grid" role="list">
          ${categoryProjects.map((project) => renderProjectCard(project)).join("")}
        </div>
      </section>
    `;
  }).join("");

  projectsList.querySelectorAll(".project-card").forEach((card) => {
    card.addEventListener("click", () => selectProject(card.dataset.projectId, projects));
  });
}

function renderProjectCard(project) {
  const cover = Array.isArray(project.imagens) ? project.imagens.find((image) => image?.src) : null;

  return `
    <button
      type="button"
      class="project-card${cover ? " project-card--with-cover" : ""}"
      role="listitem"
      aria-label="Abrir detalhes do projeto ${escapeAttribute(project.titulo)}"
      aria-pressed="false"
      data-project-id="${escapeAttribute(project.id)}"
    >
      ${cover ? `
        <span class="project-card__media" aria-hidden="true">
          <img src="${escapeAttribute(cover.src)}" alt="" loading="lazy">
        </span>
      ` : ""}
      <span class="project-card__content">
        <span class="project-card__status">${escapeHtml(project.status || "Projeto")}</span>
        <h4>${escapeHtml(project.titulo)}</h4>
        <span class="project-card__summary">${escapeHtml(project.descricaoCurta || project.subtitulo || "")}</span>
        <span class="project-card__footer">Ver detalhes <span aria-hidden="true">→</span></span>
      </span>
    </button>
  `;
}

function selectProject(projectId, projects) {
  const project = projects.find((item) => item.id === projectId);
  if (!project) return;
  setActiveCard(projectId);
  renderProjectDetails(project);
}

function renderProjectDetails(project) {
  const learnings = Array.isArray(project.aprendizados) ? project.aprendizados : [];
  const technologies = Array.isArray(project.tecnologias) ? project.tecnologias : [];
  const images = Array.isArray(project.imagens) ? project.imagens : [];
  const actions = buildActionButtons(project);

  const content = `
    <div class="project-details__content">
      <button id="back-button" type="button" class="back-button" aria-label="Voltar para a apresentação inicial">Voltar</button>
      <p class="project-details__kicker">${escapeHtml(project.status || "Projeto selecionado")}</p>
      <h2 id="details-title">${escapeHtml(project.titulo)}</h2>
      <div class="project-details__intro">${renderParagraphs(project.descricaoCompleta || project.descricaoCurta || "")}</div>

      ${technologies.length ? `
        <section aria-labelledby="technologies-title">
          <h3 id="technologies-title">Tecnologias e conceitos</h3>
          <ul class="technology-list">${technologies.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
      ` : ""}

      ${learnings.length ? `
        <section aria-labelledby="learnings-title">
          <h3 id="learnings-title">Aprendizados e frentes de estudo</h3>
          <ul>${learnings.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        </section>
      ` : ""}

      ${actions ? `<section aria-labelledby="links-title"><h3 id="links-title">Links</h3><div class="actions-list">${actions}</div></section>` : ""}

      ${images.length ? `
        <section aria-labelledby="gallery-title">
          <h3 id="gallery-title">Imagens do projeto</h3>
          <div class="gallery">${images.map(renderImageItem).join("")}</div>
        </section>
      ` : ""}
    </div>
  `;

  document.body.classList.add("has-selected-project");
  updateDetailsContent(content);
}

function renderIntro() {
  const content = `
    <div class="project-details__content">
      <p class="project-details__kicker">${escapeHtml(introContent.kicker)}</p>
      <img class="profile-photo" src="${escapeAttribute(introContent.foto.src)}" alt="${escapeAttribute(introContent.foto.alt)}" loading="eager">
      <h2 id="details-title">${escapeHtml(introContent.titulo)}</h2>
      ${introContent.paragrafos.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
      <div class="contact-block"><p><strong>${escapeHtml(introContent.contato.label)}:</strong> <a href="mailto:${escapeAttribute(introContent.contato.email)}">${escapeHtml(introContent.contato.email)}</a></p></div>
    </div>
  `;

  document.body.classList.remove("has-selected-project");
  updateDetailsContent(content, false);
}

function renderProjectsError(error) {
  projectsList.innerHTML = `
    <article class="project-card project-card--error">
      <h3>Não foi possível carregar os projetos</h3>
      <p>${escapeHtml(error.message)}</p>
      <p>A apresentação continua disponível. Para ver os cards localmente, abra o site por um servidor HTTP.</p>
    </article>
  `;
}

function buildActionButtons(project) {
  const links = [
    { url: project.linkRepositorio, label: "Ver repositório", className: "action-button--ghost" },
    { url: project.linkDemo, label: "Ver demonstração", className: "" },
    { url: project.linkDownload, label: "Baixar versão portátil", className: "" }
  ];

  return links
    .filter((link) => isSafeExternalUrl(link.url))
    .map((link) => `
      <a class="action-button ${link.className}" href="${escapeAttribute(link.url)}" target="_blank" rel="noreferrer noopener" aria-label="${escapeAttribute(link.label)} de ${escapeAttribute(project.titulo)} em nova aba">
        ${escapeHtml(link.label)}
      </a>
    `).join("");
}

function isSafeExternalUrl(value) {
  if (!value) return false;
  try {
    return new URL(value).protocol === "https:";
  } catch {
    return false;
  }
}

function renderImageItem(image) {
  if (!image?.src) return "";
  const alt = image.alt || "Imagem do projeto";
  const caption = image.legenda ? `<figcaption>${escapeHtml(image.legenda)}</figcaption>` : "";
  return `<figure class="gallery__item"><img src="${escapeAttribute(image.src)}" alt="${escapeAttribute(alt)}" loading="lazy">${caption}</figure>`;
}

function renderParagraphs(value) {
  return String(value).split(/\n{2,}/).map((paragraph) => paragraph.trim()).filter(Boolean).map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("");
}

function setActiveCard(projectId) {
  projectsList.querySelectorAll(".project-card").forEach((card) => {
    const isActive = card.dataset.projectId === projectId;
    card.classList.toggle("project-card--active", isActive);
    card.setAttribute("aria-pressed", String(isActive));
  });
}

function clearActiveCards() {
  projectsList.querySelectorAll(".project-card").forEach((card) => {
    card.classList.remove("project-card--active");
    card.setAttribute("aria-pressed", "false");
  });
}

function updateDetailsContent(content, animate = true) {
  if (!animate || prefersReducedMotion.matches) {
    projectDetails.innerHTML = content;
    bindBackButton();
    return;
  }

  projectDetails.classList.add("is-transitioning");
  window.setTimeout(() => {
    projectDetails.innerHTML = content;
    projectDetails.classList.remove("is-transitioning");
    bindBackButton();
    projectDetails.focus({ preventScroll: true });
  }, 170);
}

function bindBackButton() {
  const backButton = projectDetails.querySelector("#back-button");
  if (!backButton) return;
  backButton.addEventListener("click", () => {
    clearActiveCards();
    renderIntro();
    document.querySelector("#projects-title")?.focus?.({ preventScroll: true });
  });
}

function escapeHtml(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#96;");
}
