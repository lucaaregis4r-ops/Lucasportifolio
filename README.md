# Portfólio Lucas Regis

Site de portfólio pessoal estático criado com HTML, CSS e JavaScript puro, pronto para publicação no GitHub Pages. O projeto apresenta Lucas Regis e reúne iniciativas relacionadas a dados, tecnologia, automações, dashboards, jogos e soluções digitais, sem restringir a leitura apenas ao contexto da psicologia ou do esporte.

## Estrutura do projeto

```text
.
|-- assets/
|   `-- imagens/
|-- data/
|   `-- projetos.json
|-- index.html
|-- script.js
|-- style.css
`-- README.md
```

## Como editar os projetos

Todos os cards e detalhes dos projetos são carregados a partir do arquivo [`data/projetos.json`](./data/projetos.json). Cada item da lista representa um projeto e segue esta estrutura:

```json
{
  "id": "nome-unico-do-projeto",
  "titulo": "Título do projeto",
  "subtitulo": "Subtítulo curto",
  "descricaoCurta": "Texto breve usado no card",
  "descricaoCompleta": "Texto exibido na área de detalhes",
  "tecnologias": ["HTML", "CSS", "JavaScript"],
  "aprendizados": ["Aprendizado 1", "Aprendizado 2"],
  "status": "Em desenvolvimento",
  "imagens": [
    {
      "src": "./assets/imagens/exemplo.png",
      "alt": "Descrição da imagem",
      "legenda": "Legenda opcional"
    }
  ],
  "linkRepositorio": "https://github.com/usuario/repositorio",
  "linkDemo": "https://seudominio.com/demo"
}
```

Notas importantes:

- `id`: deve ser único para cada projeto.
- `tecnologias` e `aprendizados`: são listas e podem receber quantos itens você quiser.
- `imagens`: pode ficar vazia (`[]`) se o projeto ainda não tiver imagens.
- `linkRepositorio` e `linkDemo`: deixe como string vazia (`""`) quando não houver link. Os botões só aparecem se o campo estiver preenchido.

## Como adicionar imagens

Coloque as imagens do projeto dentro da pasta `assets/imagens/`.

Depois, adicione a referência correspondente no campo `imagens` do projeto dentro do JSON:

```json
"imagens": [
  {
    "src": "./assets/imagens/dashboard-carga-01.png",
    "alt": "Tela principal do dashboard de controle de carga",
    "legenda": "Visão geral do painel com indicadores principais."
  }
]
```

Se um projeto tiver várias imagens, basta adicionar vários objetos na lista.

## Como rodar localmente

Como o site usa `fetch` para carregar o arquivo JSON, abrir o `index.html` diretamente no navegador pode bloquear a leitura do arquivo em alguns ambientes.

O jeito mais simples é usar um servidor local, por exemplo:

1. Instale a extensão Live Server no VS Code.
2. Abra a pasta do projeto no VS Code.
3. Clique com o botão direito em `index.html`.
4. Escolha `Open with Live Server`.

Se você quiser algo ainda mais simples, também pode usar o arquivo [`iniciar-servidor-local.bat`](./iniciar-servidor-local.bat):

1. Dê dois cliques em `iniciar-servidor-local.bat`.
2. O navegador vai abrir em `http://localhost:8000/`.
3. Deixe a janela do terminal aberta enquanto estiver usando o site.

Se preferir PowerShell, use [`iniciar-servidor-local.ps1`](./iniciar-servidor-local.ps1).

Também funciona com outros servidores locais simples, como `python -m http.server`, se preferir.

## Como publicar no GitHub Pages

1. Crie um repositório no GitHub.
2. Envie os arquivos deste projeto para a branch principal (`main` ou `master`).
3. No GitHub, abra `Settings`.
4. Vá até `Pages`.
5. Em `Build and deployment`, selecione:
   - `Source`: `Deploy from a branch`
   - `Branch`: sua branch principal
   - `Folder`: `/ (root)`
6. Salve.

Depois disso, o GitHub Pages vai gerar a URL pública do site.

## Personalização rápida

- Textos gerais da apresentação inicial: edite o objeto `introContent` em [`script.js`](./script.js).
- Cores e espaçamentos: ajuste as variáveis em `:root` no arquivo [`style.css`](./style.css).
- Estrutura visual principal: está concentrada em [`index.html`](./index.html), com o conteúdo dinâmico vindo do JSON.
