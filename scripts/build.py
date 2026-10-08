#!/usr/bin/env python3
"""Gera HTML estático; o site publicado não precisa de Python nem de build no servidor."""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'data/projetos.json').read_text())
EDITORIAL = json.loads((ROOT / 'data/editorial.json').read_text())
BY_ID = {p['id']: p for p in PROJECTS}
SELECTED = list(EDITORIAL)
LAB = ['dashboard-de-controle-de-carga', 'a-temporada', 'marca', 'analise-das-acoes-no-futebol', 'simulador-procedural-de-gestao-de-rh', 'modelo-de-chatbot-configuravel']
BASE = 'https://lucaaregis4r-ops.github.io/Lucasportifolio/'


def paragraphs(text):
    return ''.join(f'<p>{esc(p)}</p>' for p in text.replace('\\n', '\n').split('\n\n') if p.strip())


def image(src, alt, prefix='', eager=False, cls=''):
    from PIL import Image
    src = src.removeprefix('./')
    with Image.open(ROOT / src) as im:
        width, height = im.size
    return f'<img class="{cls}" src="{prefix}{src}" alt="{esc(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def head(title, description, prefix='', path=''):
    return f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#50267c"><meta name="description" content="{esc(description)}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/imagens/foto-lucas.jpg">
<link rel="canonical" href="{BASE}{path}"><title>{esc(title)}</title>
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&family=Newsreader:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}script.js" defer></script>
</head><body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>'''


def header(prefix=''):
    home = prefix + 'index.html' if prefix else ''
    return f'''<header class="site-header wrap"><a class="wordmark" href="{home}#inicio" aria-label="Lucas Regis, início">LR<span aria-hidden="true">.</span></a>
    <nav aria-label="Navegação principal"><a href="{home}#projetos">Projetos</a><a href="{home}#laboratorio">Laboratório</a><a href="{home}#sobre">Sobre</a><a href="{home}#contato">Contato</a></nav>
    <a class="header-github" href="https://github.com/lucaaregis4r-ops">GitHub <span aria-hidden="true">↗</span></a></header>'''


def footer(prefix=''):
    return f'''<footer class="site-footer wrap"><span>Lucas Regis · Portfólio</span><span>Em construção, como os projetos.</span><a href="#inicio">Voltar ao início ↑</a></footer></body></html>'''


def project_links(p):
    links = []
    for key, label in [('linkDemo', 'Abrir projeto'), ('linkRepositorio', 'Ver código'), ('linkDownload', p.get('linkDownloadLabel', 'Versão publicada'))]:
        if p.get(key):
            links.append(f'<a class="text-link" href="{esc(p[key])}">{esc(label)} <span aria-hidden="true">↗</span></a>')
    return '<div class="project-links">' + ''.join(links) + '</div>' if links else ''


def feature(pid):
    p, e = BY_ID[pid], EDITORIAL[pid]
    number = e['numero']
    title = 'Mapa de valores<br> em Belo Horizonte' if number == '03' else esc(p['titulo'])
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
    return head('Lucas Regis — Projetos e investigações', 'Gosto de entender como as coisas funcionam e construir ferramentas a partir das perguntas que encontro. Projetos, experimentos e notas de Lucas Regis.') + header() + '''
<main id="conteudo">
<section class="opening wrap" id="inicio" aria-labelledby="nome"><div class="opening-meta meta"><span>Projetos, experimentos e algumas perguntas</span><span>Portfólio / 2026</span></div><h1 id="nome">Lucas Regis<span>.</span></h1>
<div class="opening-bottom"><div class="opening-statement"><p class="lead">Gosto de entender como as coisas funcionam. E de construir ferramentas quando encontro um problema que vale investigar.</p><p class="opening-context">Comecei na psicologia e no esporte. A programação veio depois, entre dificuldades do trabalho, ideias para testar e vontade de aprender.</p></div>
<nav class="opening-index" aria-label="Projetos selecionados"><p class="meta">Três pontos de partida</p><a href="#scout-trainer"><span>01</span> Observar um jogo <span aria-hidden="true">↘</span></a><a href="#registro-do-atleta"><span>02</span> Aproximar registros <span aria-hidden="true">↘</span></a><a href="#mapa-de-valores-imobiliarios-em-belo-horizonte"><span>03</span> Explorar uma cidade <span aria-hidden="true">↘</span></a><p>O que tentei, o que mudou<br> e o que ainda está em aberto.</p></nav></div></section>
<section class="selected wrap" id="projetos" aria-labelledby="selected-title"><div class="section-heading"><p class="meta">01 — Trabalhos selecionados</p><h2 id="selected-title">Algumas perguntas<br> viraram projetos.</h2><p>Três trabalhos para conhecer de perto: o problema, as escolhas e os limites do que consegui construir.</p></div>
''' + ''.join(feature(pid) for pid in SELECTED) + '''</section>
<section class="evolution" aria-labelledby="evolution-title"><div class="wrap evolution-inner"><div class="evolution-intro"><p class="meta">Nota de percurso / Scout</p><h2 id="evolution-title">Uma versão<br> leva a outra.</h2><p>O Scout de Vôlei foi uma primeira tentativa. Algumas ideias seguiram adiante; outras precisaram mudar quando comecei a construir o Scout Trainer.</p><a class="text-link" href="projetos/scout-de-volei.html">Ver o primeiro experimento ↗</a></div><ol class="timeline"><li><span class="meta">Primeiros registros</span><h3>Scout de Vôlei</h3><p>Cliques, placar e ações salvas no navegador.</p></li><li><span class="meta">Treinar a observação</span><h3>Scout Trainer</h3><p>Praticar códigos e ganhar familiaridade com o registro.</p></li><li><span class="meta">Mudar a forma de coletar</span><h3>Registro visual</h3><p>Quadra, trajetórias e análises espaciais.</p></li><li><span class="meta">Abrir outra pergunta</span><h3>Futebol e sequências</h3><p>Posse, pressão e cadeias de Markov, com os limites da coleta manual.</p></li></ol></div></section>
<section class="laboratory wrap" id="laboratorio" aria-labelledby="lab-title"><div class="section-heading"><p class="meta">02 — Laboratório</p><h2 id="lab-title">Outras coisas<br> que fui investigar.</h2><p>Jogos, ferramentas de trabalho e ideias que ainda estão tomando forma. Nem tudo começou com a intenção de virar um produto.</p></div>
<div class="lab-toolbar" hidden><div class="lab-filters" role="group" aria-label="Filtrar laboratório"><button type="button" data-filter="todos" aria-pressed="true">Tudo</button><button type="button" data-filter="esporte" aria-pressed="false">Esporte</button><button type="button" data-filter="dados" aria-pressed="false">Dados</button><button type="button" data-filter="trabalho" aria-pressed="false">Aplicações</button></div><span class="meta" id="lab-count" aria-live="polite">6 projetos</span></div>
<div class="lab-list">''' + ''.join(lab_row(pid, i) for i, pid in enumerate(LAB, 4)) + '''</div></section>
<section class="about wrap" id="sobre" aria-labelledby="about-title"><div class="about-aside"><p class="meta">03 — Sobre</p>''' + image('assets/imagens/foto-lucas.jpg', 'Lucas Regis', cls='portrait') + '''<p class="portrait-caption">Lucas Regis<br> Psicólogo formado pela UFMG.</p></div><div class="about-body"><h2 id="about-title">A programação<br> entrou pelo caminho.</h2><p class="lead">Eu não comecei com um plano de trabalhar com software. Comecei querendo resolver algumas coisas que encontrava no trabalho.</p><p>Na psicologia do esporte, sentia falta de maneiras mais simples de registrar partidas, acompanhar informações e conversar sobre decisões em equipe. Fui criando protótipos e aprendendo enquanto tentava fazê-los funcionar.</p><p>Depois vieram perguntas fora do esporte: como organizar dados de imóveis, fazer um leitor de PDFs ou experimentar uma simulação de trabalho. Alguns projetos resolvem uma dificuldade concreta. Outros me ajudam a estudar um assunto que me chamou a atenção.</p><p>A psicologia continua presente na maneira como penso sobre pessoas, dados e sistemas. Hoje tenho interesse em trabalhar com desenvolvimento, análise de dados e automação, em um contexto no qual eu possa aprender com outras pessoas e construir ferramentas úteis.</p><div class="practice"><h3>O que venho praticando</h3><dl><div><dt>Construir aplicações</dt><dd>Interfaces web, APIs e aplicativos locais, com JavaScript, TypeScript, React e Python.</dd></div><div><dt>Trabalhar com dados</dt><dd>Coleta, limpeza, SQLite, visualização e análise — incluindo o cuidado com fontes e informações incompletas.</dd></div><div><dt>Revisar o que construí</dt><dd>Testes, documentação, controle de versões e ajustes a partir do uso.</dd></div></dl></div></div></section>
<section class="contact" id="contato" aria-labelledby="contact-title"><div class="wrap contact-inner"><p class="meta">04 — Contato</p><h2 id="contact-title">Podemos conversar.</h2><div class="contact-bottom"><p>Sobre um projeto, uma pergunta em comum<br> ou uma oportunidade de trabalho.</p><div><a class="contact-email" href="mailto:lucaaregis4r@gmail.com">lucaaregis4r@gmail.com <span aria-hidden="true">↗</span></a><a class="text-link" href="https://github.com/lucaaregis4r-ops">Meus repositórios no GitHub ↗</a></div></div></div></section>
</main>''' + footer()


def gallery(p):
    # Preserve the original file as evidence; show current screenshots first.
    media = list(p['imagens'])
    if p['id'] == 'scout-trainer':
        media = media[1:] + media[:1]
    first = media[0]
    serialized = esc(json.dumps(media, ensure_ascii=False))
    thumbs = ''.join(f'<button type="button" data-slide="{i}" aria-pressed="{str(i == 0).lower()}" aria-label="{i + 1}. {esc(m["alt"])}">{image(m.get("poster", m["src"]), "", "../")}<span>{i + 1:02}{" / GIF" if m["src"].endswith(".gif") else ""}</span></button>' for i, m in enumerate(media))
    fallback = ''.join(f'<li><a href="../{m["src"].removeprefix("./")}">{esc(m["legenda"])}</a></li>' for m in media)
    return f'''<section class="case-gallery" id="imagens" aria-labelledby="gallery-title"><div class="subsection-heading"><p class="meta">Documentação visual</p><h2 id="gallery-title">Por dentro do projeto</h2></div><div class="gallery" data-gallery="{serialized}"><figure><div class="gallery-stage">{image(first['src'], first['alt'], '../', cls='gallery-image')}</div><figcaption aria-live="polite"><span class="gallery-counter">01 / {len(media):02}</span><span class="gallery-caption">{esc(first['legenda'])}</span></figcaption></figure><div class="gallery-actions"><a class="text-link gallery-original" href="../{first['src'].removeprefix('./')}" target="_blank" rel="noopener">Abrir imagem em tamanho original ↗</a><button class="motion-toggle" type="button" aria-pressed="false" hidden>Reproduzir demonstração</button></div><div class="gallery-controls" hidden><div class="gallery-thumbs" role="group" aria-label="Selecionar imagem">{thumbs}</div><div class="gallery-arrows"><button type="button" data-direction="-1" aria-label="Imagem anterior">←</button><button type="button" data-direction="1" aria-label="Próxima imagem">→</button></div></div><noscript><ul>{fallback}</ul></noscript></div></section>'''


def detail(p):
    pid = p['id']
    e = EDITORIAL.get(pid)
    number = e['numero'] if e else (f'{LAB.index(pid) + 4:02}' if pid in LAB else 'Arquivo')
    prefix = '../'
    cover = {'src':'assets/imagens/' + e['capa'], 'alt':e['legenda']} if e else (p.get('capa') or p['imagens'][0])
    sections = e['secoes'] if e else None
    intro = e['resumo'] if e else p['descricaoCurta']
    context = e['area'] if e else ('Experimento anterior / Scout' if pid == 'scout-de-volei' else 'Laboratório / ' + {'esporte':'Esporte', 'dados':'Dados', 'trabalho':'Aplicações'}[p['categoria']])
    narrative = ''.join(f'<section class="story-section" id="nota-{i}"><p class="meta">Nota {i:02}</p><h2>{esc(title)}</h2>{paragraphs(text)}</section>' for i, (title, text) in enumerate(sections, 1)) if sections else f'<section class="story-section" id="sobre-projeto"><p class="meta">Origem e desenvolvimento</p><h2>Sobre o projeto</h2>{paragraphs(p["descricaoCompleta"])}</section><section class="story-section" id="aprendizados"><p class="meta">Notas de trabalho</p><h2>O que venho aprendendo</h2><ul class="learning-list">' + ''.join(f'<li>{esc(item)}.</li>' for item in p['aprendizados']) + '</ul></section>'
    nav = ''.join(f'<a href="#nota-{i}"><span>{i:02}</span>{esc(title)}</a>' for i, (title, _) in enumerate(sections, 1)) if sections else '<a href="#sobre-projeto">Sobre o projeto</a><a href="#aprendizados">Aprendizados</a>'
    evolution = '<aside class="related-note"><p class="meta">Uma versão anterior</p><p>Antes do Scout Trainer, experimentei registrar partidas no navegador com o Scout de Vôlei.</p><a class="text-link" href="scout-de-volei.html">Ver esse começo ↗</a></aside>' if pid == 'scout-trainer' else ('<aside class="related-note"><p class="meta">Este projeto faz parte de um percurso</p><p>As experiências de registro continuaram no Scout Trainer.</p><a class="text-link" href="scout-trainer.html">Conhecer o Scout Trainer ↗</a></aside>' if pid == 'scout-de-volei' else '')
    ordered = SELECTED + LAB + ['scout-de-volei']
    nextp = BY_ID[ordered[(ordered.index(pid) + 1) % len(ordered)]]
    return head(p['titulo'] + ' — Lucas Regis', intro, prefix, f'projetos/{pid}.html') + header(prefix) + f'''
<main id="conteudo" class="case-main wrap"><section class="case-opening" id="inicio"><a class="back-link" href="../index.html#{'projetos' if e else 'laboratorio'}">← Voltar ao portfólio</a><div class="case-meta meta"><span>{number} / {esc(context)}</span><span>{esc(p['status'])}</span></div><h1>{esc(p['titulo'])}</h1><p class="case-deck">{esc(intro)}</p>{project_links(p)}</section>
<figure class="case-cover">{image(cover['src'], cover['alt'], prefix, eager=True)}<figcaption><span>Em tela</span>{esc(cover.get('legenda') or cover['alt'])}</figcaption></figure>
<div class="case-layout"><aside class="case-sidebar"><nav aria-label="Nesta página"><p class="meta">Nesta página</p>{nav}<a href="#ferramentas">Ferramentas</a><a href="#imagens">Imagens e demonstrações</a></nav></aside><div class="case-story">{narrative}{evolution}<section class="story-section tools-section" id="ferramentas"><p class="meta">Ferramentas utilizadas</p><h2>Com o que construí</h2><ul class="tools-list">{''.join(f'<li>{esc(t)}</li>' for t in p['tecnologias'])}</ul></section></div></div>
{gallery(p)}<nav class="case-end" aria-label="Continuar explorando"><a class="text-link" href="../index.html#laboratorio">Voltar ao índice</a><a href="{nextp['id']}.html"><span class="meta">Próximo projeto</span><span>{esc(nextp['titulo'])} ↗</span></a></nav></main>''' + footer(prefix)


(ROOT / 'index.html').write_text(home())
for project in PROJECTS:
    (ROOT / 'projetos' / (project['id'] + '.html')).write_text(detail(project))
print(f'Gerados: página inicial + {len(PROJECTS)} páginas de projetos.')
