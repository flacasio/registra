# Como contribuir

Contribuições são bem-vindas, especialmente correções de scrapers, novos módulos, testes e melhorias de documentação.

## Antes de começar

Leia:

1. `README.md`;
2. `docs/CARD_STYLE_GUIDE.md`;
3. `docs/DEVELOPMENT.md`.

## Boas práticas

- mantenha cada alteração focada em um problema;
- não publique tokens, cookies, IDs privados ou conteúdo de `.env`;
- preserve a separação entre source, parser, cache e template;
- reutilize verbos e emojis oficiais;
- inclua exemplos ou fixtures sanitizados quando corrigir um parser;
- atualize a documentação quando alterar comportamento visível;
- não grave respostas vazias inesperadas sobre um cache válido.

## Novo módulo

Uma contribuição de módulo deve, sempre que aplicável, incluir:

- source;
- parser;
- template;
- estratégia de ID e antirrepetição;
- variáveis em `.env.example`;
- registro em `run.py`;
- agendamento no workflow;
- documentação do evento e dos emojis;
- teste ou fixture representativo.

## Pull requests

Na descrição do pull request, informe:

- o que mudou;
- por que a mudança é necessária;
- como foi testada;
- quais plataformas ou módulos são afetados;
- qualquer limitação conhecida.

Alterações que dependem de HTML externo devem mencionar a página ou estrutura usada como referência, sem incluir dados privados.
