# Manual de identidade dos cards

## Princípios

Os cards do Registra! devem ser rápidos de ler, consistentes entre plataformas e livres de texto redundante.

- O título da rede identifica a origem do evento.
- A linha seguinte usa o padrão `nome exibido + verbo`.
- Cada linha apresenta uma informação principal.
- Emojis representam categorias ou funções, não decoração.
- O mesmo conceito deve usar o mesmo emoji sempre que possível.
- Nomes próprios e títulos originais não devem ser traduzidos.

## Nome e linguagem

O nome mostrado nos cards vem de `DISPLAY_NAME`. Nos exemplos desta documentação, ele aparece como **Zi**.

Prefira ações curtas:

| Módulo | Evento | Texto do card |
|---|---|---|
| Last.fm Recent | música escutada | Zi escutou |
| Last.fm Loved | música amada | Zi amou |
| Last.fm Comments | comentário recebido | Zi foi comentada |
| Steam Recent | jogo recente | Zi jogou |
| Steam Achievements | conquista desbloqueada | Zi conquistou |
| Steam Awards | prêmio recebido | Zi foi premiada |
| Banco de Séries | episódio assistido | Zi assistiu |
| Banco de Séries | episódio avaliado | Zi avaliou |
| Serializd | episódio registrado | Zi assistiu |
| Letterboxd | filme assistido | Zi assistiu |
| Backloggd | jogo iniciado | Zi começou |
| Backloggd | jogo abandonado | Zi abandonou |
| Backloggd | jogo concluído | Zi concluiu |
| AOTY Feed | álbum avaliado | Zi avaliou |
| AOTY Compare | nota alterada | Zi reavaliou |

## Datas

O formato oficial para data e hora é:

```text
27/07/2026, às 06:36
```

Regras:

- usar o fuso `America/Sao_Paulo`;
- usar zero à esquerda em dia e mês;
- usar relógio de 24 horas;
- não misturar datas por extenso com datas numéricas nos cards.

## Emojis oficiais

| Emoji | Significado principal |
|---|---|
| 🎵 | música |
| 🎤 | artista |
| 💿 | álbum |
| 🎬 | cinema ou Letterboxd |
| 🎞️ | filme ou série |
| 📺 | episódio |
| 🎮 | jogo |
| 🥇 | conquistas da Steam |
| 📋 | descrição ou detalhe de conquista |
| 🎖 | premiação da Steam |
| 🏅 | prêmio recebido |
| ⭐ / ⭐️ | avaliação |
| 💘 | atividade de música amada |
| ✍ | comentário |
| 📅 | data de lançamento |
| ↗️ | nota aumentada |
| ↘️ | nota reduzida |
| 🔁 | reavaliação sem direção identificável |
| 🕒 | horário ou momento da atividade |
| 🔗 | link externo |

## Repetições conhecidas

Alguns emojis aparecem em mais de um módulo por representarem o mesmo conceito:

- `🎞️`: títulos de filmes, séries e episódios conforme o contexto.
- `⭐` ou `⭐️`: avaliações no BDS, Serializd, Letterboxd e AOTY.
- `💿`: álbuns no Last.fm e no AOTY.
- `🎮`: jogos nos módulos da Steam e do Backloggd.
- `📺`: episódios no BDS e no Serializd.
- `🕒`: datas, horários e tempos relativos.
- `🔗`: links para a atividade original.

Essas repetições são intencionais. Um emoji novo só deve ser criado quando o conceito realmente for novo.

## Estrutura recomendada

```text
[emoji da rede] Rede
Nome ação

[imagem, quando disponível]

[emoji] informação principal
[emoji] informação secundária
[emoji] avaliação ou estado

🕒 27/07/2026, às 06:36
🔗 Link
```

Nem todos os cards precisam ter todas as linhas. Linhas vazias devem separar blocos, não inflar o card.

## Regras por módulo

### Last.fm Recent

- ação: `escutou`;
- música: `🎵`;
- artista: `🎤`;
- álbum: `💿`;
- quando não houver timestamp, usar `🕒 Tocando agora`.

### Last.fm Loved

- ação: `amou`;
- manter música, artista e álbum nas mesmas posições do Recent.

### Last.fm Comments

- ação: `foi comentada`;
- autor: `👤`;
- comentário: `✍`.

### Steam Recent

- tempo das duas últimas semanas: sufixo `recente`;
- tempo acumulado: sufixo `total`.

### Steam Achievements

- ícone da rede: `🥇`;
- ação: `conquistou`;
- descrição da conquista: `📋`.

### Steam Awards

- ícone da rede: `🎖`;
- ação: `foi premiada`;
- prêmio: `🏅`.

### Banco de Séries

- ações: `assistiu` e `avaliou`;
- série: `🎞️`;
- episódio: `📺` nos cards assistidos;
- nota: `⭐`.

### Serializd

- evento `LOGGED`: `assistiu`;
- episódio: `📺`.

### Letterboxd

- ação de filme assistido: `assistiu`;
- título em linha própria;
- avaliação em linha própria, iniciada por `⭐️`.

### Backloggd

- ações: `começou`, `abandonou` e `concluiu`;
- não acrescentar `um jogo` à ação.

### AOTY

- Feed: `avaliou`;
- Compare: `reavaliou`;
- Incoming: usar `📅` nas informações de lançamento;
- aumento de nota: `↗️`;
- redução de nota: `↘️`.

## Checklist visual

Antes de publicar um módulo ou alteração:

- [ ] A ação está na lista oficial?
- [ ] O emoji já tem significado documentado?
- [ ] A data usa o formato oficial?
- [ ] O título não contém avaliação ou metadado grudado?
- [ ] Há no máximo uma informação principal por linha?
- [ ] O card evita frases como “um filme”, “um álbum” ou “um jogo” quando o item já aparece abaixo?
- [ ] O link aponta para a atividade original?
