# Portfólio Lucas Regis

Site pessoal de Lucas Regis, psicólogo formado pela UFMG, com projetos em esporte, dados e desenvolvimento de aplicações. Foi feito em HTML, CSS e JavaScript, sem dependências de build. O conteúdo dos dez projetos fica em `data/projetos.json`.

## O que há no site

- Grade visual com filtros por área e cartões com imagem, resumo, status e tecnologias.
- Galeria por projeto, com capturas reais e dois GIFs de interações reais. As imagens do Registro do Atleta e do Dashboard Olympico usam **somente dados fictícios**.
- Descrições completas sobre origem, funcionamento e aprendizados, além de links para código, demonstração ou versão publicada quando confirmados.
- Layout responsivo, navegação por teclado, diálogo nativo de detalhes, textos alternativos e redução de movimento quando solicitada pelo navegador.

Os GIFs de `registro-atleta-demo.gif` e `mapa-valores-bh-demo.gif` foram montados a partir de quadros capturados após interações reais nas respectivas aplicações. Eles não simulam recursos inexistentes.

## Executar localmente

O JSON é carregado por `fetch`, por isso abra o site por um servidor HTTP local:

```bash
python3 -m http.server 8000
```

Acesse `http://localhost:8000/`.

## Adicionar um projeto

Edite `data/projetos.json`. Cada item precisa de `id`, `titulo` e `categoria` (`esporte`, `dados` ou `trabalho`). Os campos `prioridade`, `subtitulo`, `descricaoCurta`, `descricaoCompleta`, `status`, `tecnologias`, `aprendizados`, `capa`, `imagens`, `linkRepositorio`, `linkDemo` e `linkDownload` controlam o cartão e o painel de detalhes. Imagens devem ter `src`, `alt` e `legenda` descritivos. `linkDownloadLabel` personaliza o texto de uma versão publicada.

Use apenas links verificados e imagens que possam ser divulgadas. O Dashboard de Controle de Carga não aponta para a versão publicada porque os repositórios correspondentes alertam que a edição estática pode conter dados de atletas. Não inclua capturas dessa edição no portfólio.
