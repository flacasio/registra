# Registra!

**Registra!** é um agregador modular de atividades públicas em plataformas de entretenimento e mídia.

O projeto consulta serviços como Banco de Séries, Goodreads, Steam, Backloggd, Letterboxd, Last.fm, Album of the Year, Serializd e Futez, detecta novas atividades e as transforma em cards padronizados enviados ao Telegram.

A configuração permite personalizar o nome exibido, os perfis monitorados e os módulos ativos, tornando o projeto reutilizável em diferentes instalações.

## Como funciona

```text
sources -> parsers -> templates -> core.telegram
```

- `sources/`: consulta as plataformas.
- `parsers/`: interpreta os dados encontrados.
- `templates/`: monta os cards.
- `core/`: contém peças comuns, como cache, imagens, texto e Telegram.
- `cache/`: guarda o que já foi visto para evitar repetição.

## Documentação

- [`docs/CARD_STYLE_GUIDE.md`](docs/CARD_STYLE_GUIDE.md): identidade, eventos, emojis e layout dos cards.
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md): arquitetura, convenções, testes e tratamento de erros.
- [`docs/SOURCES.md`](docs/SOURCES.md): informações sobre as fontes monitoradas.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): orientações para contribuições.

## Configuração

Copie `.env.example` para `.env` e preencha os valores locais.
O arquivo `.env` não deve ser publicado.

Use `DISPLAY_NAME` para o nome que deve aparecer nos cards.
Use `REAL_NAME` para o nome real que deve ser substituído automaticamente.
Use `DISPLAY_EMOJI` para o emoji que aparece antes do nome nos cards.

Os textos dos cards são exibidos em português. Nomes de pessoas, jogos, filmes, livros, discos e músicas são preservados. Datas com horário usam o fuso de São Paulo e o formato `27/07/2026, às 06:36`.

## Uso

Listar módulos:

```bash
python run.py --list
```

Rodar todos os módulos:

```bash
python run.py
```

Rodar apenas um módulo:

```bash
python run.py lastfm_recent
```

## GitHub Actions

O projeto inclui o workflow:

```text
.github/workflows/rezistro.yml
```

Ele roda automaticamente em ritmos diferentes e também pode ser executado manualmente pela aba Actions do GitHub.

O workflow usa três ritmos:

- `lastfm_recent`: a cada 5 minutos.
- módulos normais: a cada 30 minutos.
- `aoty_compare` e `steam_wishlist`: a cada 6 horas.

Os horários foram deslocados alguns minutos para reduzir atrasos em momentos de maior uso do GitHub Actions.

Para funcionar, cadastre no GitHub Actions os mesmos Secrets listados em `.env.example`.

Para conquistas da Steam, use `STEAM_ACHIEVEMENTS_APPIDS` com um ou mais appids separados por vírgula. Exemplo: `613100`.
Na primeira execução, o módulo de conquistas salva a base atual sem enviar troféus antigos. Depois disso, envia apenas conquistas novas.

Os módulos de listas da Steam seguem a mesma regra de base inicial: biblioteca, jogos platinados, wishlist, prêmios, insígnias, capturas e amigos só notificam itens que aparecerem depois da primeira leitura.
A wishlist da Steam roda em ritmo mais lento porque a página costuma bloquear consultas frequentes com erro 429.

O módulo de seguindo do Goodreads também salva a base inicial e depois notifica apenas novos perfis.
O módulo de seguidores do AOTY segue a mesma regra: base inicial primeiro, novos seguidores depois.

O módulo `aoty_compare` salva uma base de todas as notas na primeira execução. Depois verifica blocos de páginas para detectar notas alteradas. Ajuste `AOTY_COMPARE_MAX_PAGES` e `AOTY_COMPARE_PAGES_PER_RUN` no `.env` para controlar volume e velocidade da varredura.

Para evitar bloqueio do AOTY, a base inicial também é montada em blocos pequenos e `AOTY_REQUEST_DELAY_SECONDS` define uma pausa entre requisições.

O módulo `futez` usa `FUTEZ_PROFILE_URL` quando a URL pública do perfil estiver disponível. Se o padrão da rede permitir, também pode usar `FUTEZ_USER_ID`.

O módulo `aoty_incoming` monitora a lista pública configurada em `AOTY_INCOMING_LIST_PATH`, salvando uma base inicial e notificando novos lançamentos.
