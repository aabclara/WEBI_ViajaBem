# Spec: Admin CRM Gestão Kanban e Operação de Venda

## Requirement: Gestão Visual de Reservas e Pagamento via WhatsApp
O painel administrativo atuará como a fonte principal e centralizada para o controle manual de cobranças e vagas. O fluxo de pagamento MUST ser direcionado ao WhatsApp, e a efetivação refletida via Kanban através de transições de coluna.

### Cenário: Geração de Link de Cobrança para WhatsApp
- **Dado** que um administrador autenticado acessa o Kanban de reservas,
- **Quando** ele analisar uma reserva na coluna inicial e clicar na ação de envio de cobrança,
- **Então** a interface MUST gerar um link formatado para o WhatsApp contendo uma mensagem informativa padrão associada aos dados de PIX da agência.
- **E** tal ação NÃO altera o status persistente da reserva no Kanban ou banco de dados.

### Cenário: Transição Manual de Status (Drag and Drop Otimista)
- **Dado** que o Kanban exibe as colunas de status sequenciais,
- **Quando** o administrador arrastar um card de reserva para uma coluna sinalizando avanço financeiro (exílio: de `CREATED` para `BLOCKED` ou `CONFIRMED`),
- **Então** a interface MUST refletir a mudança visualmente de forma instantânea na UI e disparar um `PATCH` REST request contendo o novo status.
- **E** o modelo lógico do servidor MUST atualizar e blindar essas instâncias permanentemente, travando o total de vagas e negando edições destrutivas por parte do visitante.

### Cenário de Erro: Falha de conexão com o banco durante arrasto no Kanban
- **Dado** que o agente arrastou um card para uma nova coluna,
- **Quando** o banco de dados estiver indisponível e o `PATCH` request falhar,
- **Então** a interface MUST reverter o card para a posição anterior e MUST exibir mensagem de erro informando falha na conexão sem perder o estado anterior da reserva.
