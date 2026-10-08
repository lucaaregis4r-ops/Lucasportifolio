# Lucas Regis — Projetos e investigações

Portfólio estático em HTML, CSS e JavaScript, publicado no GitHub Pages. A apresentação parte dos problemas e das decisões de cada projeto, com identidade editorial em roxo, grafite e papel claro.

## Estrutura

- Abertura, três trabalhos selecionados, percurso do Scout, laboratório, trajetória e contato.
- Páginas próprias para os dez projetos, com endereço compartilhável, contexto, ferramentas e documentação visual.
- Scout Trainer, Registro do Atleta e o mapa de BH têm relatos sobre origem, escolhas, funcionamento atual, limites e aprendizados.
- O Scout de Vôlei é apresentado como experimento anterior, conectado ao Scout Trainer.
- Navegação e conteúdo independem de JavaScript. Os filtros do laboratório e controles das galerias são melhorias opcionais.
- Os dois GIFs só carregam após clicar em **Reproduzir demonstração** e podem ser interrompidos. São capturas de interações reais, não simulações de recursos.

## Abrir localmente

```bash
python3 -m http.server 8791 --bind 127.0.0.1
```

Abra `http://127.0.0.1:8791/`. Os HTMLs gerados estão versionados; servir e publicar o site não exige instalação nem build.

## Editar

- `data/projetos.json`: cadastro dos projetos, descrições, tecnologias, situação, imagens e links.
- `data/editorial.json`: chamadas e relatos dos três projetos selecionados.
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

As imagens do Registro do Atleta e do Dashboard Olympico usam **apenas dados fictícios**. O dashboard utiliza a captura atualizada, não a imagem antiga.

O Dashboard não aponta para as versões públicas das aplicações porque os repositórios correspondentes alertam para a presença de dados de atletas. Não inclua capturas dessas versões.

As imagens conceituais do simulador de RH permanecem identificadas como referências planejadas. A galeria abre com capturas do protótipo jogável. No Chatbot Configurável, as telas identificam o provedor local de teste.

A versão 0.5 do Scout Trainer está em desenvolvimento. O download público indicado corresponde à versão 0.3.0; o texto mantém essa diferença explícita.
