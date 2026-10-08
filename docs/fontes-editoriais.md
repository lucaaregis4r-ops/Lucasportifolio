# Referências da revisão editorial — 8 de outubro de 2026

Os relatos descrevem implementações observadas no código e na documentação. A menção a testes significa que esses cenários estão no repositório; esta edição do portfólio não executou as suítes dos aplicativos nem certifica seu estado global.

## Scout Trainer

Repositório: `lucaaregis4r-ops/Treino-de-estatistica`, revisão `6c8f2fbccb0f569874858745a030df6d27beb06f`.

- `README.md`: modalidades, versão em desenvolvimento, diferenças para tracking, PDF, pendências de validação e piloto.
- `src/infrastructure/persistence/indexeddb/ScoutTrainerDatabase.ts`: IndexedDB, stores e evolução do esquema.
- `docs/arquitetura/decisoes/ADR-004-local-first.md`: baixa dependência operacional e persistência local.
- `docs/arquitetura/decisoes/ADR-012-visual-input-shared-canonical-pipeline.md` e `src/domain/scout/mapper/VisualScoutMapper.ts`: entrada visual e evento compartilhado.
- `src/domain/football/FootballAssistedRecording.ts`: pressão ausente/desconhecida e precisão da observação.
- `src/domain/football/FootballMarkovAnalyzer.ts`: transições por posse, interrupção em coleta suspensa e probabilidade calculada por contagens.
- `src/tests/integration/football-recording-cycle.test.ts`: correção, desfazer, placar, recarga, exportação e restauração.

A versão 0.5 é a referência da documentação; o download público continua apontando para a versão 0.3.0. Não apresentar a versão de desenvolvimento como lançamento validado.

## Registro do Atleta

Repositório: `lucaaregis4r-ops/registro-do-atleta`, revisão `0cded5c8ae76acf81aa2ee2532c9177194879b3c`.

- `README.md` e `docs/ARCHITECTURE.md`: fontes, normalização por domínio, identidade, filas de revisão, SQLite, API local, demo estática e limites do LLM opcional.
- `tests/unit/test_pipeline.py`: reprocessar a mesma planilha sem criar novos registros.
- `tests/unit/test_records.py`: leitura de CSV e referência à linha original.
- `tests/unit/test_api_review.py`: confirmar, rejeitar e criar identidades, associação de nomes e registro da revisão.
- `src/registro_atleta/operations/backup.py`: backup via SQLite e verificação de integridade.

Não atribuir à demo sintética validação clínica ou cobertura de todos os formatos reais. Não usar dados reais nas imagens.

## Mapa de valores / Moradia BH

Repositório: `lucaaregis4r-ops/Valor-de-Casas-em-bh`, revisão `73bf5edf47b18edb92fbb3b736653c103dbda985`.

- `README.md` e `index.html` (Metodologia): Atlas histórico, Mercado Agora, fontes/períodos diferentes, base de 2021 tratada como apartamentos, JSON público, PostgreSQL em Docker e operação local.
- `pipeline/normalize.py`: valores, área e aluguel por m².
- `pipeline/deduplicate.py`: identidade do anúncio limitada à fonte e à coleta; não inferir deduplicação universal de imóveis.
- `pipeline/geocoding_cache.py`: normalização de cidade/bairro e coordenadas aproximadas com precisão de bairro.
- `pipeline/validation.py` e `tests/test_validation.py`: rejeição de coleta truncada ou inválida antes da persistência.
- `assets/js/filters.js`, `statistics.js` e `app.js`: medianas, agrupamento e mínimo de amostra por bairro.

Capturas atuais feitas no navegador a partir da revisão `cd9df582ab0ac355dfdb6ee665217f5bc18e37b5`, sem alterações na interface: Atlas, Mercado Agora e perfil de Santa Tereza. A coleta mais recente estava interrompida; a imagem e a legenda preservam esse estado. O GIF anterior permanece identificado como histórico.

## Demais projetos

Nesta rodada, os resumos foram condensados a partir dos relatos existentes em `data/projetos.json`, sem acrescentar arquitetura, testes executados, métricas ou resultados.

## Voz e capturas — 8 de outubro de 2026

A abertura e as motivações dos três projetos foram organizadas a partir das explicações fornecidas por Lucas, preservando a ordem do raciocínio e os projetos em evolução. Detalhes técnicos continuam baseados nas referências acima.

- Registro do Atleta: `src/registro_atleta/llm/provider.py` confirma integração opcional com Ollama, desabilitada por padrão. Novas capturas de Revisões e Macrociclo usam exclusivamente a demo sintética do repositório, cuja data dos dados continua visível (julho de 2026).
- Scout Trainer: captura atual de registro visual, feita após criar uma partida com o elenco demonstrativo pela interface. Nenhuma ação esportiva real foi utilizada; a partida está vazia.
- Imagens PNG são screenshots reais. Não houve geração de mockups, retoque da interface ou fabricação de dados para as capturas.
