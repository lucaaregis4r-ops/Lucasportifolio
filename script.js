const PROJECTS_URL = "./data/projetos.json";

const introContent = {
  kicker: "Apresentação",
  titulo: "Dados, psicologia, esporte e soluções",
  foto: {
    src: "./assets/imagens/foto-lucas.jpg",
    alt: "Foto de Lucas Regis"
  },
  paragrafos: [
    "Olá, meu nome é Lucas.",
    "Criei este espaço para reunir alguns projetos que venho desenvolvendo e, principalmente, para organizar melhor minhas ideias, aprendizados e experimentos.",
    "Sou psicólogo formado pela UFMG e trabalho hoje no contexto esportivo. Por isso, muitos projetos aqui têm relação com esporte, atletas, dados de treino, organização de informações e ferramentas para facilitar a rotina de trabalho.",
    "Ao mesmo tempo, tenho me interessado cada vez mais por tecnologia, dados, automações e desenvolvimento de soluções digitais. Nem tudo aqui é necessariamente sobre psicologia ou esporte; essas áreas são parte da minha trajetória, mas também têm sido um ponto de partida para aprender coisas novas e explorar outros caminhos.",
    "Este repositório é um pouco disso: um lugar para mostrar o que venho construindo, testar ideias e compartilhar projetos que podem fazer sentido em diferentes contextos.",
    "Estou aberto a conversas, sugestões, trocas de ideias e oportunidades."
  ],
  contato: {
    label: "Contato",
    email: "lucaaregis4r@gmail.com"
  }
};

const projectsList = document.querySelector("#projects-list");
const projectDetails = document.querySelector("#project-details");

document.addEventListener("DOMContentLoaded", () => {
  // Exibe a apresentação geral enquanto os projetos ainda estão sendo carregados.
  renderIntro();
  loadProjects();
});

async function loadProjects() {
  try {
    const response = await fetch(PROJECTS_URL);

    if (!response.ok) {
      throw new Error(`Falha ao carregar os projetos (${response.status}).`);
    }

    const projects = await response.json();

    if (!Array.isArray(projects) || projects.length === 0) {
      throw new Error("O arquivo JSON não contém uma lista válida de projetos.");
    }

    renderProjectCards(projects);
  } catch (error) {
    renderProjectsError(error);
    console.error(error);
  } finally {
    projectsList.setAttribute("aria-busy", "false");
  }
}

function renderProjectCards(projects) {
  projectsList.innerHTML = "";

  projects.forEach((project) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "project-card";
    card.setAttribute("role", "listitem");
    card.setAttribute("aria-label", `Abrir detalhes do projeto ${project.titulo}`);
    card.dataset.projectId = project.id;

    card.innerHTML = `
      <h3>${escapeHtml(project.titulo)}</h3>
      <p class="project-card__summary">${escapeHtml(project.descricaoCurta || project.subtitulo || "")}</p>
      <span class="project-card__footer">Clique para ver mais</span>
    `;

    card.addEventListener("click", () => {
      setActiveCard(project.id);
      renderProjectDetails(project);
    });

    projectsList.appendChild(card);
  });
}

function renderProjectDetails(project) {
  const learnings = Array.isArray(project.aprendizados) ? project.aprendizados : [];
  const images = Array.isArray(project.imagens) ? project.imagens : [];
  const actions = buildActionButtons(project);

  const content = `
    <div class="project-details__content">
      <button
        id="back-button"
        type="button"
        class="back-button"
        aria-label="Voltar para a apresentação inicial"
      >
        Voltar
      </button>
      <p class="project-details__kicker">Projeto selecionado</p>
      <h2 id="details-title">${escapeHtml(project.titulo)}</h2>
      <div class="project-details__intro">
        ${renderParagraphs(project.descricaoCompleta || project.descricaoCurta || "")}
      </div>

      ${learnings.length ? `
        <section aria-labelledby="learn-title">
          <h3 id="learn-title">Aprendizados e frentes de estudo</h3>
          <ul>
            ${learnings.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </section>
      ` : ""}

      ${actions ? `
        <section aria-labelledby="links-title">
          <h3 id="links-title">Links</h3>
          <div class="actions-list">${actions}</div>
        </section>
      ` : ""}

      ${images.length ? `
        <section aria-labelledby="gallery-title">
          <h3 id="gallery-title">Imagens do projeto</h3>
          <div class="gallery">
            ${images.map((image) => renderImageItem(image)).join("")}
          </div>
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
      <button
        id="back-button"
        type="button"
        class="back-button"
        aria-label="Voltar para a apresentação inicial"
        hidden
      >
        Voltar
      </button>
      <p class="project-details__kicker">${escapeHtml(introContent.kicker)}</p>
      <img
        class="profile-photo"
        src="${escapeAttribute(introContent.foto.src)}"
        alt="${escapeAttribute(introContent.foto.alt)}"
        loading="eager"
      >
      <h2 id="details-title">${escapeHtml(introContent.titulo)}</h2>
      ${introContent.paragrafos.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
      <div class="contact-block">
        <p>
          <strong>${escapeHtml(introContent.contato.label)}:</strong>
          <a href="mailto:${escapeHtml(introContent.contato.email)}">${escapeHtml(introContent.contato.email)}</a>
        </p>
      </div>
    </div>
  `;

  document.body.classList.remove("has-selected-project");
  updateDetailsContent(content, false);
}

function renderProjectsError(error) {
  projectsList.innerHTML = `
    <article class="project-card project-card--error" role="listitem">
      <h3>Os projetos ainda não foram configurados</h3>
      <p>${escapeHtml(error.message)}</p>
      <p>Enquanto isso, sua apresentação principal continua visível ao lado.</p>
      <p>Quando quiser ativar os cards, basta configurar o arquivo <code>data/projetos.json</code> e abrir o site em um servidor local.</p>
    </article>
  `;
}

function buildActionButtons(project) {
  const buttons = [];

  if (project.linkRepositorio) {
    buttons.push(`
      <a
        class="action-button action-button--ghost"
        href="${escapeAttribute(project.linkRepositorio)}"
        target="_blank"
        rel="noreferrer noopener"
        aria-label="Abrir repositório do projeto ${escapeHtml(project.titulo)} em nova aba"
      >
        Ver repositório
      </a>
    `);
  }

  if (project.linkDemo) {
    buttons.push(`
      <a
        class="action-button"
        href="${escapeAttribute(project.linkDemo)}"
        target="_blank"
        rel="noreferrer noopener"
        aria-label="Abrir demonstração do projeto ${escapeHtml(project.titulo)} em nova aba"
      >
        Ver demonstração
      </a>
    `);
  }

  return buttons.join("");
}

function renderImageItem(image) {
  if (!image || !image.src) {
    return "";
  }

  const alt = image.alt || "Imagem do projeto";
  const caption = image.legenda ? `<figcaption>${escapeHtml(image.legenda)}</figcaption>` : "";

  return `
    <figure class="gallery__item">
      <img src="${escapeAttribute(image.src)}" alt="${escapeAttribute(alt)}" loading="lazy">
      ${caption}
    </figure>
  `;
}

function renderParagraphs(value) {
  return String(value)
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean)
    .map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`)
    .join("");
}

function setActiveCard(projectId) {
  const cards = projectsList.querySelectorAll(".project-card");

  cards.forEach((card) => {
    const isActive = card.dataset.projectId === projectId;
    card.classList.toggle("project-card--active", isActive);
    card.setAttribute("aria-pressed", String(isActive));
  });
}

function clearActiveCards() {
  const cards = projectsList.querySelectorAll(".project-card");

  cards.forEach((card) => {
    card.classList.remove("project-card--active");
    card.setAttribute("aria-pressed", "false");
  });
}

function updateDetailsContent(content, animate = true) {
  if (!animate) {
    projectDetails.innerHTML = content;
    return;
  }

  // A troca de conteúdo usa uma transição curta para deixar o painel mais fluido.
  projectDetails.classList.add("is-transitioning");

  window.setTimeout(() => {
    projectDetails.innerHTML = content;
    projectDetails.classList.remove("is-transitioning");
    bindBackButton();
    projectDetails.focus();
  }, 170);
}

function bindBackButton() {
  const backButton = document.querySelector("#back-button");

  if (!backButton || backButton.hidden) {
    return;
  }

  backButton.addEventListener("click", () => {
    clearActiveCards();
    renderIntro();
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#96;");
}
