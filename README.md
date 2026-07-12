# Rezistro

Rezistro e um agregador pessoal de atualizacoes em redes sociais e servicos de midia.

Ele consulta plataformas como Banco de Series, Goodreads, Steam, Backloggd,
Letterboxd, Last.fm, Album of the Year, Serializd e Futez, detecta novidades e envia
cards para um chat privado no Telegram.

## Como funciona

```text
sources -> parsers -> templates -> core.telegram
```

- `sources/`: consulta as plataformas.
- `parsers/`: interpreta os dados encontrados.
- `templates/`: monta os cards.
- `core/`: contem pecas comuns, como cache, imagens e Telegram.
- `cache/`: guarda o que ja foi visto para evitar repeticao.

## Configuracao

Copie `.env.example` para `.env` e preencha os valores locais.
O arquivo `.env` nao deve ser publicado.

Use `DISPLAY_NAME` para o nome que deve aparecer nos cards.
Use `REAL_NAME` para o nome real que deve ser substituido automaticamente.
Use `DISPLAY_EMOJI` para o emoji que aparece antes do nome nos cards.

Textos dos cards devem sair em portugues. Nomes de pessoas, jogos, filmes,
livros, discos e musicas devem ser preservados. Datas com horario usam o fuso
de Sao Paulo e o formato `11 de julho de 2026 às 22:30`.

## Uso

Listar modulos:

```bash
python run.py --list
```

Rodar todos os modulos:

```bash
python run.py
```

Rodar apenas um modulo:

```bash
python run.py lastfm_recent
```

## GitHub Actions

O projeto inclui o workflow:

```text
.github/workflows/rezistro.yml
```

Ele roda automaticamente em ritmos diferentes e tambem pode ser executado manualmente
pela aba Actions do GitHub.

O workflow usa tres ritmos:

- `lastfm_recent`: a cada 5 minutos.
- modulos normais: a cada 30 minutos.
- `aoty_compare` e `steam_wishlist`: a cada 6 horas.

Os horarios foram deslocados alguns minutos para reduzir atrasos em momentos de
maior uso do GitHub Actions.

Para funcionar, cadastre no GitHub Actions os mesmos Secrets listados em
`.env.example`.

Para conquistas da Steam, use `STEAM_ACHIEVEMENTS_APPIDS` com um ou mais appids
separados por virgula. Exemplo: `613100`.
Na primeira execucao, o modulo de conquistas salva a base atual sem enviar
trofeus antigos. Depois disso, envia apenas conquistas novas.

Os modulos de listas da Steam seguem a mesma regra de base inicial: biblioteca,
jogos platinados, wishlist, premios, insignias, capturas e amigos so notificam
itens que aparecerem depois da primeira leitura.
A wishlist da Steam roda em ritmo mais lento porque a pagina costuma bloquear
consultas frequentes com erro 429.
O modulo de seguindo do Goodreads tambem salva a base inicial e depois notifica
apenas novos perfis.
O modulo de seguidores do AOTY segue a mesma regra: base inicial primeiro,
novos seguidores depois.
O modulo `aoty_compare` salva uma base de todas as notas na primeira execucao.
O modulo `futez` usa `FUTEZ_PROFILE_URL` quando a URL publica do perfil estiver
disponivel. Se o padrao da rede permitir, tambem pode usar `FUTEZ_USER_ID`.
Depois verifica blocos de paginas para detectar notas alteradas. Ajuste
`AOTY_COMPARE_MAX_PAGES` e `AOTY_COMPARE_PAGES_PER_RUN` no `.env` se precisar
controlar volume e velocidade da varredura.
Para evitar bloqueio do AOTY, a base inicial tambem e montada em blocos pequenos
e `AOTY_REQUEST_DELAY_SECONDS` define uma pausa entre requisicoes.
O modulo `aoty_incoming` monitora a lista publica configurada em
`AOTY_INCOMING_LIST_PATH`, salvando base inicial e notificando novos lancamentos.
