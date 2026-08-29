# Portfólio Lucas Regis

Este é o espaço onde reúno projetos que nasceram de dificuldades da rotina, ideias ligadas ao esporte ou simplesmente da vontade de aprender a construir alguma coisa com programação.

Sou psicólogo formado pela UFMG e trabalho no contexto esportivo. Aos poucos, fui usando a programação para criar ferramentas, organizar informações e experimentar outras formas de apresentar uma ideia. Alguns projetos já possuem versões utilizáveis; outros ainda fazem parte do meu processo de estudo.

No site, cada projeto aparece em um card. Ao selecionar um deles, conto um pouco sobre o motivo de ele existir, o que já consegui fazer e o que fui aprendendo no caminho.

## Categorias

1. **Projetos ligados ao esporte**
2. **Organização e leitura de dados**
3. **Aplicações para estudo e trabalho**

A ordem dos projetos dentro de cada categoria é definida pelo campo `prioridade` em `data/projetos.json`.

## Tecnologias do portfólio

- HTML semântico;
- CSS responsivo;
- JavaScript sem frameworks;
- JSON como fonte de dados dos projetos.

## Estrutura

```text
.
├── assets/imagens/       # Foto e capturas usadas nas galerias
├── data/projetos.json    # Conteúdo, categoria, prioridade e links
├── index.html            # Estrutura e navegação principal
├── script.js             # Carregamento, agrupamento e painel de detalhes
└── style.css             # Identidade visual e responsividade
```

## Executar localmente

O JSON é carregado por `fetch`, por isso o site deve ser aberto por um servidor HTTP local, e não diretamente pelo sistema de arquivos.

Com Python instalado:

```bash
python -m http.server 8000
```

Depois, acesse `http://localhost:8000`.

## Adicionar ou atualizar um projeto

Edite `data/projetos.json` e mantenha os campos principais:

```json
{
  "id": "identificador-unico",
  "titulo": "Nome do projeto",
  "categoria": "esporte",
  "prioridade": 1,
  "descricaoCurta": "Resumo para o card",
  "descricaoCompleta": "Texto do painel lateral",
  "tecnologias": [],
  "aprendizados": [],
  "status": "Em desenvolvimento",
  "imagens": [],
  "linkRepositorio": "",
  "linkDemo": ""
}
```

Categorias aceitas: `esporte`, `dados` e `trabalho`. O campo `linkDownload` pode ser usado quando houver um arquivo público confirmado.

Não adicione links estimados. Se um repositório ou demonstração não estiver confirmado, mantenha o campo vazio.

## Acessibilidade e experiência

- navegação por âncoras entre categorias;
- link para pular diretamente aos projetos;
- cards acionáveis por teclado, com estado selecionado comunicado por `aria-pressed`;
- foco visível e rótulos descritivos;
- painel de detalhes com atualização anunciada por `aria-live`;
- imagens com texto alternativo e carregamento tardio;
- respeito a `prefers-reduced-motion`;
- layout adaptado para telas menores.

## Conteúdo e privacidade

As descrições devem refletir apenas funcionalidades documentadas nos projetos. O portfólio não publica dados operacionais de atletas. No Registro do Atleta, a demonstração pública utiliza exclusivamente dados sintéticos e não representa uma ferramenta de decisão clínica.
