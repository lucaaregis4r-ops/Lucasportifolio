#!/usr/bin/env python3
"""Gera HTML estático; o site publicado não precisa de Python nem de build no servidor."""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'data/projetos.json').read_text())
EDITORIAL = json.loads((ROOT / 'data/editorial.json').read_text())
BY_ID = {p['id']: p for p in PROJECTS}
SELECTED = ['mapa-de-valores-imobiliarios-em-belo-horizonte', 'modelo-de-chatbot-configuravel', 'sorge', 'estudio-de-videos-curtos']
LAB = ['marca', 'registro-do-atleta', 'simulador-procedural-de-gestao-de-rh', 'dashboard-de-controle-de-carga', 'scout-trainer', 'analise-das-acoes-no-futebol', 'a-temporada', 'scout-de-volei']
BASE = 'https://lucaaregis4r-ops.github.io/Lucasportifolio/'


def paragraphs(text):
    return ''.join(f'<p>{esc(p)}</p>' for p in text.replace('\\n', '\n').split('\n\n') if p.strip())


def image(src, alt, prefix='', eager=False, cls=''):
    from PIL import Image
    from xml.etree import ElementTree
    src = src.removeprefix('./')
    if src.endswith('.svg'):
        svg = ElementTree.parse(ROOT / src).getroot()
        width, height = int(svg.attrib['width']), int(svg.attrib['height'])
    else:
        with Image.open(ROOT / src) as im:
            width, height = im.size
    return f'<img class="{cls}" src="{prefix}{src}" alt="{esc(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def head(title, description, prefix='', path=''):
    return f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#4d3048"><meta name="description" content="{esc(description)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/imagens/foto-lucas.jpg">
<link rel="canonical" href="{BASE}{path}"><title>{esc(title)}</title>
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=Newsreader:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}script.js" defer></script>
</head><body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>'''


def header(prefix=''):
    home = prefix + 'index.html' if prefix else ''
    return f'''<header class="site-header wrap"><a class="wordmark" href="{home}#inicio" aria-label="Lucas Regis, início">LR<span aria-hidden="true">.</span></a>
    <nav aria-label="Navegação principal"><a href="{home}#projetos">Projetos</a><a href="{home}#laboratorio">Laboratório</a><a href="{home}#sobre">Sobre</a><a href="{home}#contato">Contato</a></nav>
    <a class="header-github" href="https://github.com/lucaaregis4r-ops">GitHub <span aria-hidden="true">↗</span></a></header>'''


def footer(prefix=''):
    return f'''<footer class="site-footer wrap"><span>Lucas Regis · Portfólio</span><span>Arquivo de projetos · 2026</span><a href="#inicio">Voltar ao início ↑</a></footer></body></html>'''


def project_links(p):
    links = []
    for key, label in [('linkDemo', 'Abrir projeto'), ('linkRepositorio', 'Ver código'), ('linkDownload', p.get('linkDownloadLabel', 'Versão publicada'))]:
        if p.get(key):
            links.append(f'<a class="text-link" href="{esc(p[key])}">{esc(label)} <span aria-hidden="true">↗</span></a>')
    return '<div class="project-links">' + ''.join(links) + '</div>' if links else ''


def feature(pid):
    p, e = BY_ID[pid], EDITORIAL[pid]
    number = e['numero']
    title = 'Moradia BH' if pid == 'mapa-de-valores-imobiliarios-em-belo-horizonte' else esc(p['titulo'])
    src = 'assets/imagens/' + e['capa']
    return f'''<article class="feature feature--{number}" id="{pid}">
    <div class="feature-heading"><span class="project-number">{number}</span><div><p class="meta">{e['area']}</p><h3><a href="projetos/{pid}.html">{title}</a></h3></div><span class="status">{esc(p['status'])}</span></div>
    <div class="feature-body"><div class="feature-copy"><h4>{esc(e['chamada'])}</h4><p>{esc(e['resumo'])}</p><a class="text-link" href="projetos/{pid}.html">Ler sobre o projeto <span aria-hidden="true">↗</span></a><p class="tool-note">{esc(' · '.join(p['tecnologias'][:3]))}</p></div>
    <figure><a class="image-link" href="projetos/{pid}.html" aria-label="Ver o projeto {esc(p['titulo'])}">{image(src, e['legenda'])}<span class="image-hint" aria-hidden="true">Abrir projeto ↗</span></a><figcaption><span>Fig. {number}</span>{esc(e['legenda'])}</figcaption></figure></div></article>'''


def lab_row(pid, i):
    p = BY_ID[pid]
    cover = p.get('capa') or p['imagens'][0]
    return f'''<article class="lab-row" data-category="{p['categoria']}"><span class="lab-number">{i:02}</span><a class="lab-image" href="projetos/{pid}.html" tabindex="-1" aria-hidden="true">{image(cover['src'], '')}</a><div class="lab-copy"><p class="meta">{esc(p['status'])}</p><h3><a href="projetos/{pid}.html">{esc(p['titulo'])}<span aria-hidden="true"> ↗</span></a></h3><p>{esc(p['descricaoCurta'])}</p></div><span class="lab-category">{ {'esporte':'Esporte', 'dados':'Dados', 'trabalho':'Aplicações'}[p['categoria']]}</span></article>'''


def home():
    return head('Lucas Regis — Dados, IA e automação', 'Projetos de análise de dados, IA aplicada, automação e desenvolvimento de ferramentas por Lucas Regis.') + header() + '''
<main id="conteudo">
<section class="opening wrap" id="inicio" aria-labelledby="nome"><div class="opening-meta meta"><span>Dados, IA aplicada e automação</span><span>Portfólio / 2026</span></div><h1 id="nome"><span class="greeting">Olá, meu nome é</span> Lucas<span>.</span></h1>
<div class="opening-bottom"><div class="opening-statement"><p class="lead">Sou psicólogo formado pela UFMG e desenvolvo ferramentas para organizar dados, automatizar tarefas e apoiar decisões.</p><p class="opening-context">Minha experiência profissional me aproximou de planilhas, relatórios e processos que dependem de várias pessoas. Neste portfólio, mostro como levo esse olhar a projetos de dados, IA aplicada e desenvolvimento — com o estágio e os limites de cada projeto identificados.</p></div>
<nav class="opening-index" aria-label="Projetos selecionados"><p class="meta">Índice / Destaques</p><a href="#mapa-de-valores-imobiliarios-em-belo-horizonte"><span>01</span> Moradia BH <span aria-hidden="true">↘</span></a><a href="#modelo-de-chatbot-configuravel"><span>02</span> Chatbot Configurável <span aria-hidden="true">↘</span></a><a href="#sorge"><span>03</span> Sorge <span aria-hidden="true">↘</span></a><a href="#estudio-de-videos-curtos"><span>04</span> Estúdio de Vídeos Curtos <span aria-hidden="true">↘</span></a></nav></div></section>
<section class="selected wrap" id="projetos" aria-labelledby="selected-title"><div class="section-heading"><p class="meta">01 — Trabalhos selecionados</p><h2 id="selected-title">Dados, IA<br> e automação.</h2><p>Separei os projetos que mostram como identifico um problema, preparo a informação e construo uma ferramenta que pode ser usada e revisada.</p></div>
''' + ''.join(feature(pid) for pid in SELECTED) + '''</section>
<section class="evolution" aria-labelledby="evolution-title"><div class="wrap evolution-inner"><div class="evolution-intro"><p class="meta">Da tarefa à ferramenta</p><h2 id="evolution-title">Como trabalho<br> com problemas.</h2><p>Os projetos partem de uma tarefa concreta e avançam por etapas que deixam os dados e as decisões mais fáceis de acompanhar.</p></div><ol class="timeline"><li><span class="meta">Entender o fluxo</span><h3>Começar pela tarefa</h3><p>Identifico quem precisa da informação, como ela chega e onde o processo trava.</p></li><li><span class="meta">Preparar a informação</span><h3>Conferir a base</h3><p>Reviso fontes, formatos, duplicidades e lacunas antes de automatizar.</p></li><li><span class="meta">Construir a ferramenta</span><h3>Reduzir etapas manuais</h3><p>Uso interfaces, regras e integrações para tornar o fluxo mais claro e repetível.</p></li><li><span class="meta">Validar o resultado</span><h3>Mostrar limites</h3><p>Registro o que já funciona, o que ainda depende de revisão e o que precisa ser testado no uso real.</p></li></ol></div></section>
<section class="laboratory wrap" id="laboratorio" aria-labelledby="lab-title"><div class="section-heading"><p class="meta">02 — Outros projetos</p><h2 id="lab-title">Mais projetos.</h2><p>Outras aplicações e experimentos, organizados por área. Os projetos ligados ao esporte ficam reunidos aqui, depois dos trabalhos de dados, IA e automação.</p></div>
<div class="lab-toolbar" hidden><div class="lab-filters" role="group" aria-label="Filtrar projetos"><button type="button" data-filter="todos" aria-pressed="true">Tudo</button><button type="button" data-filter="dados" aria-pressed="false">Dados</button><button type="button" data-filter="trabalho" aria-pressed="false">Produtos e automação</button><button type="button" data-filter="esporte" aria-pressed="false">Esporte</button></div><span class="meta" id="lab-count" aria-live="polite">''' + str(len(LAB)) + ''' projetos</span></div>
<div class="lab-list">''' + ''.join(lab_row(pid, i) for i, pid in enumerate(LAB, len(SELECTED) + 1)) + '''</div></section>
<section class="about wrap" id="sobre" aria-labelledby="about-title"><div class="about-aside"><p class="meta">03 — Sobre</p>''' + image('assets/imagens/foto-lucas.jpg', 'Lucas Regis', cls='portrait') + '''<p class="portrait-caption">Lucas Regis<br> Psicólogo formado pela UFMG.</p></div><div class="about-body"><h2 id="about-title">Formação<br> e percurso.</h2><p class="lead">Sou psicólogo formado pela UFMG. Minha experiência profissional se desenvolveu no esporte, em um trabalho que envolve acompanhamento, planejamento e articulação entre pessoas e áreas.</p><p>Nessa rotina, lidei com registros, planilhas e relatórios que pedem atenção ao contexto e aos limites da informação. Esse foi o ponto de partida de algumas ferramentas; depois, continuei explorando problemas de outros campos, como ofertas de moradia, leitura de documentos e assistentes configuráveis.</p><p>Hoje quero levar essa experiência a oportunidades em análise de dados, operações, IA aplicada e automação. Os projetos abaixo são experiências de trabalho e projetos autorais em diferentes estágios, descritos com transparência sobre o que já funciona e o que ainda falta validar.</p><div class="practice"><h3>Competências aplicadas nos projetos</h3><dl><div><dt>Dados</dt><dd>Coleta e validação, planilhas, SQL, Python, visualização e interpretação cuidadosa das fontes.</dd></div><div><dt>Automação</dt><dd>Fluxos com regras claras, integrações e IA quando ela ajuda a resolver a tarefa.</dd></div><div><dt>Aplicações</dt><dd>Interfaces, APIs e programas locais, com documentação e revisão do funcionamento.</dd></div></dl></div></div></section>
<section class="contact" id="contato" aria-labelledby="contact-title"><div class="wrap contact-inner"><p class="meta">04 — Contato</p><h2 id="contact-title">Podemos conversar.</h2><div class="contact-bottom"><p>Aberto a oportunidades em<br> dados, operações e automação.</p><div><a class="contact-email" href="mailto:lucaaregis4r@gmail.com">lucaaregis4r@gmail.com <span aria-hidden="true">↗</span></a><a class="text-link" href="https://github.com/lucaaregis4r-ops">Meus repositórios no GitHub ↗</a></div></div></div></section>
</main>''' + footer()

def gallery(p):
    # Preserve the original file as evidence; show current screenshots first.
    media = list(p['imagens'])
    first = media[0]
    serialized = esc(json.dumps(media, ensure_ascii=False))
    thumbs = ''.join(f'<button type="button" data-slide="{i}" aria-pressed="{str(i == 0).lower()}" aria-label="{i + 1}. {esc(m["alt"])}">{image(m.get("poster", m["src"]), "", "../")}<span>{i + 1:02}{" / GIF" if m["src"].endswith(".gif") else ""}</span></button>' for i, m in enumerate(media))
    fallback = ''.join(f'<li><a href="../{m["src"].removeprefix("./")}">{esc(m["legenda"])}</a></li>' for m in media)
    return f'''<section class="case-gallery" id="imagens" aria-labelledby="gallery-title"><div class="subsection-heading"><p class="meta">Documentação visual</p><h2 id="gallery-title">Por dentro do projeto</h2></div><div class="gallery" data-gallery="{serialized}"><figure><div class="gallery-stage">{image(first['src'], first['alt'], '../', cls='gallery-image')}</div><figcaption aria-live="polite"><span class="gallery-counter">01 / {len(media):02}</span><span class="gallery-caption">{esc(first['legenda'])}</span></figcaption></figure><div class="gallery-actions"><a class="text-link gallery-original" href="../{first['src'].removeprefix('./')}" target="_blank" rel="noopener">Abrir imagem em tamanho original ↗</a><button class="motion-toggle" type="button" aria-pressed="false" hidden>Reproduzir demonstração</button></div><div class="gallery-controls" hidden><div class="gallery-thumbs" role="group" aria-label="Selecionar imagem">{thumbs}</div><div class="gallery-arrows"><button type="button" data-direction="-1" aria-label="Imagem anterior">←</button><button type="button" data-direction="1" aria-label="Próxima imagem">→</button></div></div><noscript><ul>{fallback}</ul></noscript></div></section>'''


def implementation(editorial):
    if not editorial:
        return ''
    rows = ''.join(f'<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>' for label, value in editorial['implementacao'])
    return f'<section class="implementation" id="implementacao" aria-labelledby="implementation-title"><h2 class="meta" id="implementation-title">Implementação / {editorial["numero"]}</h2><dl>{rows}</dl></section>'


def detail(p):
    pid = p['id']
    e = EDITORIAL.get(pid)
    number = e['numero'] if e else (f'{len(SELECTED) + LAB.index(pid) + 1:02}' if pid in LAB else 'Arquivo')
    prefix = '../'
    cover = {'src':'assets/imagens/' + e['capa'], 'alt':e['legenda']} if e else (p.get('capa') or p['imagens'][0])
    sections = e['secoes'] if e else None
    intro = e['resumo'] if e else p['descricaoCurta']
    context = e['area'] if e else ('Experimento anterior / Scout' if pid == 'scout-de-volei' else 'Laboratório / ' + {'esporte':'Esporte', 'dados':'Dados', 'trabalho':'Aplicações'}[p['categoria']])
    narrative = ''.join(f'<section class="story-section" id="nota-{i}"><p class="meta">Nota {i:02}</p><h2>{esc(title)}</h2>{paragraphs(text)}</section>' for i, (title, text) in enumerate(sections, 1)) if sections else f'<section class="story-section" id="sobre-projeto"><p class="meta">Descrição</p><h2>Sobre o projeto</h2>{paragraphs(p["descricaoCompleta"])}</section><section class="story-section" id="aprendizados"><p class="meta">Notas de trabalho</p><h2>Notas de desenvolvimento</h2><ul class="learning-list">' + ''.join(f'<li>{esc(item)}.</li>' for item in p['aprendizados']) + '</ul></section>'
    nav = ''.join(f'<a href="#nota-{i}"><span>{i:02}</span>{esc(title)}</a>' for i, (title, _) in enumerate(sections, 1)) if sections else '<a href="#sobre-projeto">Sobre o projeto</a><a href="#aprendizados">Aprendizados</a>'
    if e:
        nav = '<a href="#implementacao">Ficha de implementação</a>' + nav
    references = '<div class="source-links"><p class="meta">No repositório</p>' + ''.join(f'<a class="text-link" href="{esc(url)}">{esc(label)} ↗</a>' for label, url in e.get('referencias', [])) + '</div>' if e else ''
    evolution = '<aside class="related-note"><p class="meta">Uma versão anterior</p><p>Antes do Scout Trainer, experimentei registrar partidas no navegador com o Scout de Vôlei.</p><a class="text-link" href="scout-de-volei.html">Ver a versão anterior ↗</a></aside>' if pid == 'scout-trainer' else ('<aside class="related-note"><p class="meta">Continuação do projeto</p><p>As experiências de registro continuaram no Scout Trainer.</p><a class="text-link" href="scout-trainer.html">Conhecer o Scout Trainer ↗</a></aside>' if pid == 'scout-de-volei' else '')
    ordered = SELECTED + LAB
    nextp = BY_ID[ordered[(ordered.index(pid) + 1) % len(ordered)]]
    return head(p['titulo'] + ' — Lucas Regis', intro, prefix, f'projetos/{pid}.html') + header(prefix) + f'''
<main id="conteudo" class="case-main wrap"><section class="case-opening" id="inicio"><a class="back-link" href="../index.html#{'projetos' if e else 'laboratorio'}">← Voltar ao portfólio</a><div class="case-meta meta"><span>{number} / {esc(context)}</span><span>{esc(p['status'])}</span></div><h1>{esc(p['titulo'])}</h1><p class="case-deck">{esc(intro)}</p>{project_links(p)}</section>
{implementation(e)}
<figure class="case-cover">{image(cover['src'], cover['alt'], prefix, eager=True)}<figcaption><span>Em tela</span>{esc(cover.get('legenda') or cover['alt'])}</figcaption></figure>
<div class="case-layout"><aside class="case-sidebar"><nav aria-label="Nesta página"><p class="meta">Nesta página</p>{nav}<a href="#ferramentas">Ferramentas</a><a href="#imagens">Imagens e demonstrações</a></nav></aside><div class="case-story">{narrative}{evolution}<section class="story-section tools-section" id="ferramentas"><p class="meta">Ferramentas utilizadas</p><h2>Ferramentas</h2><ul class="tools-list">{''.join(f'<li>{esc(t)}</li>' for t in p['tecnologias'])}</ul>{references}</section></div></div>
{gallery(p)}<nav class="case-end" aria-label="Continuar explorando"><a class="text-link" href="../index.html#laboratorio">Voltar ao índice</a><a href="{nextp['id']}.html"><span class="meta">Próximo projeto</span><span>{esc(nextp['titulo'])} ↗</span></a></nav></main>''' + footer(prefix)


(ROOT / 'index.html').write_text(home())
for project in PROJECTS:
    (ROOT / 'projetos' / (project['id'] + '.html')).write_text(detail(project))
print(f'Gerados: página inicial + {len(PROJECTS)} páginas de projetos.')
