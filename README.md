# Lucas Regis — Portfólio

Portfólio estático em HTML, CSS e JavaScript, publicado no GitHub Pages. [Abrir o portfólio](https://lucaaregis4r-ops.github.io/Lucasportifolio/). Reúne os projetos, suas decisões de desenvolvimento e capturas das interfaces. O layout usa ameixa, grafite e fundo claro; Archivo, Newsreader e uma fonte monoespaçada diferenciam títulos, prosa e informações técnicas.

## Estrutura

- Abertura, três trabalhos selecionados, percurso do Scout, laboratório, trajetória e contato.
- Páginas próprias para os doze projetos, com endereço compartilhável, contexto, ferramentas e documentação visual.
- Scout Trainer, Registro do Atleta e o mapa de BH têm relatos sobre origem, escolhas, funcionamento atual, limites e aprendizados.
- O Scout de Vôlei é apresentado como experimento anterior, conectado ao Scout Trainer.
- Navegação e conteúdo independem de JavaScript. Os filtros do laboratório e controles das galerias são melhorias opcionais.
- Os GIFs existentes só carregam após clicar em **Reproduzir demonstração** e podem ser interrompidos. São capturas de interações reais, não simulações de recursos.

## Abrir localmente

```bash
python3 -m http.server 8791 --bind 127.0.0.1
```

Abra `http://127.0.0.1:8791/`. Os HTMLs gerados estão versionados; servir e publicar o site não exige instalação nem build.

## Editar

- `data/projetos.json`: cadastro dos projetos, descrições, tecnologias, situação, imagens e links.
- `data/editorial.json`: chamadas, relatos, fichas de implementação e referências dos três projetos selecionados.
- `docs/fontes-editoriais.md`: código e documentação que sustentam os detalhes técnicos publicados.
- `scripts/build.py`: estrutura das páginas e textos gerais.
- `style.css`: identidade e layout responsivo.
- `script.js`: filtros, troca de imagens e reprodução explícita dos GIFs.

Depois de alterar os textos ou a estrutura, gere novamente o HTML. O gerador usa Python 3 e Pillow para ler as dimensões reais das imagens:

```bash
python3 -m pip install Pillow
python3 scripts/build.py
python3 scripts/check.py
node --check script.js
```

O verificador confere arquivos, âncoras, títulos principais e atributos alternativos. Antes de publicar, revise também a aparência em telas grandes e pequenas e os controles por teclado.

## Mídia e cuidado com os dados

As imagens do Registro do Atleta e do Dashboard Olympico usam **apenas dados fictícios**. A captura do dashboard documenta uma demonstração anterior; o repositório evoluiu depois dela.

O Dashboard não aponta para as versões públicas das aplicações porque os repositórios correspondentes alertam para a presença de dados de atletas. Não inclua capturas dessas versões.

As imagens conceituais do simulador de RH permanecem identificadas como referências planejadas. A galeria abre com capturas do protótipo jogável. No Chatbot Configurável, as telas identificam o provedor local de teste.

A versão 0.7.0 do código do Scout Trainer está em desenvolvimento. O download público indicado corresponde à versão 0.3.0; o texto mantém essa diferença explícita.

A galeria inclui capturas reais das quatro modalidades do Scout Trainer, do Mosaico do Moradia BH, da versão atual de A Temporada e da interface local do gerador de vídeos. O vídeo produzido pelo gerador não está no portfólio. A imagem do Sorge é um diagrama, pois o projeto não tem interface própria. As capturas antigas de A Temporada e o GIF do mapa estão identificados como históricos.
