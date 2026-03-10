# Spec: Admin CRM Kanban & Pós-Sinal

## Contexto
O processo de gestão da agência Viaja Bem é 100% externo à gateway de pagamentos. Logo, o painel foca na aprovação manual do progresso do funil. O sistema suporta um Dashboard do Líder para reter a retenção da Venda e Link Mágico de Compartilhamento.

### Requirement: CRM Kanban Boards
Visualização direta e centralizada das reservas pendentes aos Administradores.

#### Scenario: Visualizando Intenções de Compra Pendentes
- **WHEN** Admin acessa o painel de Reservas do destino X.
- **THEN** O Quadro lista intenções na coluna "Novos (CREATED)".
- **AND** cards apresentam o `combo_size`, Contato (Zap) e Telefone do Líder de Compra.

#### Scenario: Gestão Ativa em Whatsapp (External Gateaway)
- **WHEN** Admin clica em Contatar no Quadro Kanban de Intent "CREATED".
- **THEN** Sistema abre "API web.whatsapp.me" com link pré-formatado do PIX de cobrança.

#### Scenario: Congelamento Parcial (Sinal de 50%)
- **WHEN** Admin comprova recebimento de Pix por fora e avança o Card no Kanban para `BLOCKED`.
- **THEN** a Viagem reconhece aquelas vagas como Efetivamente Traçadas.
- **AND** a UI/API trancam as edições do Tamanho Total de Combos para aquele grupo (Se o líder quer mudar, deve acionar Suporte da agência manualmente).

### Requirement: O Dashboard do Líder
Área onde a Burocracia foi delegada ao líder pra retenção pós-ímpeto de compra.

#### Scenario: Submissão de Docs (Identidades)
- **WHEN** Intenção está nos estados `CREATED` ou `BLOCKED`.
- **THEN** o Líder pode inserir RGs/Nomes dos Acompanhantes em seu Dashboard da viagem até preencher o tamanho exato de N Cadeiras de seu `combo_size`.

#### Scenario: Emissão Public Link (Acompanhantes)
- **WHEN** toda a equipe preencheu seus RGs e o Admin mudou a Intent para `CONFIRMED`.
- **THEN** Dashboard do líder gera um botão "Compartilhar Viagem" que emite um URL read-only (não exige criação de contas adicionais) para que todo o seu time possa abrir a viagem, ver o horário do embarque e acessar uma cópia das regras, aumentando o engajamento orgânico do funil.
