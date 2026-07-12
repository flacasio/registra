# Rezistro - estado atual

## Ideia

O Rezistro e um agregador pessoal de atualizacoes em redes sociais e servicos de midia.
Ele consulta fontes como Banco de Series, Letterboxd, Last.fm, Steam e Goodreads,
detecta novidades e envia cards para um chat privado no Telegram.

## Estrutura

- `sources/`: busca atividades nas plataformas.
- `parsers/`: transforma dados brutos em atividades padronizadas.
- `templates/`: transforma atividades em cards.
- `core/`: pecas comuns, como cache, Telegram, imagens e console.
- `cache/`: guarda o que ja foi visto para evitar repeticao.

## Modulos mais maduros

- Banco de Series
- Letterboxd
- Last.fm recente
- Last.fm favoritos
- Last.fm comentarios

## Modulos ainda em evolucao

- Steam comentarios
- Steam reviews
- Steam wishlist
- Steam achievements
- Steam perfect
- Steam new
- Steam awards
- Steam badges
- Steam screenshots
- Steam friends
- Goodreads
- Goodreads following
- Backloggd
- AOTY
- AOTY followers
- AOTY incoming
- Serializd

## Como rodar

Listar modulos:

```bash
python run.py --list
```

Rodar tudo:

```bash
python run.py
```

Rodar apenas um modulo:

```bash
python run.py lastfm_recent
```

## GitHub Actions

O workflow fica em `.github/workflows/rezistro.yml`.
Ele roda a cada 30 minutos, permite execucao manual e restaura o cache do
Rezistro entre execucoes para evitar notificacoes repetidas.

## Configuracao local

Copie `.env.example` para `.env` e preencha seus dados locais.
O arquivo `.env` nao deve ir para o GitHub.
Nos cards enviados ao Telegram, `REAL_NAME` e substituido por `DISPLAY_NAME`.
Textos dos cards devem ficar em portugues, preservando nomes e titulos.
Datas e horarios devem usar o fuso de Sao Paulo.
Os cards devem usar o nome da rede na primeira linha e a acao do `DISPLAY_NAME` como subtitulo.
Sempre que a fonte trouxer data de postagem/atividade, o card deve exibir essa data.
O Goodreads monitora os feeds de lendo, quero ler e lidos/avaliados.
O Goodreads Following monitora listas de pessoas e notifica apenas novos perfis depois da base inicial.
O Backloggd monitora atividades recentes de jogos, como jogando, concluiu e abandonou.
O AOTY monitora a avaliacao recente de albuns no perfil.
O AOTY Followers monitora seguidores novos depois da base inicial.
O AOTY Compare mantem uma base historica de notas e notifica quando uma nota existente sobe ou desce.
O AOTY Incoming monitora a lista publica de lancamentos futuros.
O Serializd monitora as atividades recentes do perfil, com suporte inicial para episodios registrados/avaliados.
Os modulos devem comparar listas recentes com o cache e enviar todos os itens ainda nao vistos, nao apenas o ultimo item.
O Steam Achievements monitora conquistas desbloqueadas por appid e monta card com imagem composta do jogo e do trofeu.
Os novos modulos de listas da Steam salvam base inicial e depois notificam apenas itens novos.

## Proximos cuidados

- Revogar e recriar tokens que ja foram salvos em arquivos antigos.
- Conferir os modulos que realmente funcionam antes de publicar no GitHub.
- Manter um modulo por vez: buscar, interpretar, montar card, testar, so entao passar ao proximo.
