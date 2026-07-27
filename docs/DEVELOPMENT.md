# Guia de desenvolvimento

## Arquitetura

```text
plataforma pública
      ↓
   source
      ↓
   parser
      ↓
   cache
      ↓
  template
      ↓
 Telegram
```

### Responsabilidades

- `sources/`: obter respostas HTTP e conteúdo bruto.
- `parsers/`: converter conteúdo externo em dicionários previsíveis.
- `templates/`: transformar atividades em cards.
- `core/`: serviços compartilhados, texto, imagem, cache e envio.
- `cache/`: estado persistente usado para evitar duplicidade.

Um template não deve raspar HTML. Um parser não deve enviar mensagens. Separar essas responsabilidades mantém os módulos testáveis e reduz o estrago quando uma plataforma muda o próprio layout.

## Convenções de código

### Arquivos e funções

- nomes de módulos e arquivos em `snake_case`;
- função pública principal do parser: `parse` ou `parse_all`;
- função pública principal do template: `make_card`;
- auxiliares privados iniciados por `_`;
- constantes em `UPPER_SNAKE_CASE`;
- chaves de atividade curtas, estáveis e descritivas.

### Identificadores de atividade

Todo evento deve possuir um `id` determinístico. Ele deve representar a atividade, não apenas o usuário ou a plataforma.

Boas fontes de ID:

- GUID de RSS;
- URL permanente;
- identificador nativo da plataforma;
- composição estável de usuário, item, evento e timestamp.

Evite usar apenas horário de execução, pois isso recria o mesmo evento em cada rodada.

## Configuração

- credenciais e perfis ficam em variáveis de ambiente;
- `.env` nunca deve ser versionado;
- toda variável nova deve entrar em `.env.example`;
- valores específicos de uma instalação não devem ser embutidos no código;
- textos visíveis devem respeitar `DISPLAY_NAME`, `REAL_NAME` e `DISPLAY_EMOJI`.

## Tratamento de erros

### Requisições

- definir timeout;
- tratar respostas não bem-sucedidas;
- respeitar limites e erro 429;
- evitar repetição agressiva de requisições;
- registrar plataforma e etapa quando ocorrer uma falha.

### Mudanças de HTML

Quando um seletor deixar de funcionar:

1. não gravar cache vazio como se fosse uma coleta válida;
2. falhar com mensagem clara;
3. preservar a base anterior;
4. revisar source e parser separadamente;
5. incluir um fixture ou exemplo que reproduza a mudança.

### Dados opcionais

Campos opcionais devem usar `activity.get(...)`. O card deve continuar válido quando capa, comentário, álbum, avaliação ou link estiverem ausentes.

## Cache e antirrepetição

- a primeira execução de módulos históricos pode apenas formar a base;
- uma coleta vazia inesperada não deve apagar o cache;
- IDs antigos não devem reaparecer por reordenação da página;
- alterações legítimas, como mudança de nota, precisam gerar um novo evento ou comparar estado anterior e atual;
- caches devem ser pequenos, legíveis e específicos por módulo.

## Plano de testes

### Parser

Validar:

- extração com todos os campos;
- ausência de campo opcional;
- item inválido;
- lista vazia;
- caracteres especiais;
- separação entre título e avaliação quando a plataforma mistura ambos.

### Template

Validar:

- ação correta;
- ordem das linhas;
- emojis oficiais;
- formato de data;
- ausência de linhas vazias desnecessárias;
- HTML aceito pelo Telegram.

### Cache

Validar:

- primeira execução;
- evento novo;
- evento repetido;
- alteração de estado;
- resposta vazia ou falha de rede.

### Verificação manual

Antes de ativar um módulo em produção:

- [ ] Executar o parser com uma resposta real ou fixture.
- [ ] Gerar ao menos um card de exemplo.
- [ ] Confirmar o link externo.
- [ ] Rodar duas vezes e confirmar que não duplica.
- [ ] Simular ausência de imagem e campo opcional.
- [ ] Confirmar que nenhum segredo aparece nos logs.

## Fluxo para um novo módulo

1. Definir o evento e sua ação curta.
2. Escolher emojis já existentes sempre que possível.
3. Criar source e parser.
4. Definir um ID determinístico.
5. Implementar cache ou comparação de estado.
6. Criar template conforme o manual visual.
7. Adicionar configuração ao `.env.example`.
8. Registrar o módulo em `run.py` e no workflow, quando necessário.
9. Testar coleta, card e antirrepetição.
10. Atualizar README, documentação e changelog.

## Instruções para assistentes de IA

Antes de modificar o Rezistro:

1. ler `README.md`;
2. ler `docs/CARD_STYLE_GUIDE.md`;
3. identificar a camada correta para a mudança;
4. reutilizar funções compartilhadas;
5. não inventar verbos ou emojis sem documentá-los;
6. preservar compatibilidade com variáveis de ambiente existentes;
7. não inserir dados pessoais, tokens, cookies ou URLs privadas;
8. explicar qualquer suposição sobre HTML externo;
9. preferir alterações pequenas e verificáveis;
10. atualizar a documentação quando a convenção mudar.

## Evolução recomendada

- fixtures sanitizados para cada plataforma;
- testes automatizados de parser e template;
- configuração declarativa dos módulos;
- validação central dos dicionários de atividade;
- relatório de saúde dos scrapers;
- geração de cards de demonstração sem envio ao Telegram;
- métricas de falhas, duplicatas evitadas e tempo de execução.
