# Casos de Uso — Sistema Viaje Bem

## Diagrama Geral de Atores

```mermaid
flowchart LR
    V(["👤 Visitante"])
    L(["👤 Líder"])
    A(["👤 Administrador"])
    S(["⚙️ Sistema"])

    V -->|acessa| UC1["Visualizar catálogo de viagens"]
    V -->|interage| UC2["Realizar reserva (Fricção Mínima)"]

    L -->|autentica via| UC3["Solicitar OTP por email"]
    L -->|valida| UC4["Verificar código OTP"]
    L -->|consulta| UC5["Visualizar painel de reservas"]
    L -->|cadastra| UC6["Cadastrar dados dos acompanhantes"]
    L -->|compartilha| UC7["Visualizar e copiar voucher viral"]
    L -->|altera| UC8["Alterar combo (bloqueado se BLOCKED)"]

    A -->|gerencia| UC9["Visualizar Kanban de reservas"]
    A -->|arrasta| UC10["Atualizar status da reserva (Drag & Drop)"]
    A -->|envia| UC11["Gerar link de cobrança WhatsApp / PIX"]

    S -->|dispara| UC12["Enviar OTP por email"]
    S -->|gera| UC13["Gerar voucher viral após BLOCKED"]
    S -->|valida| UC14["Bloquear overbooking (validação de vagas)"]
    S -->|retorna| UC15["Notificar erros e timeouts via Toast"]
```

---

## UC-01: Fluxo do Visitante (Vitrine & Reserva)

```mermaid
flowchart TD
    V(["👤 Visitante"])

    V --> A["Acessar vitrine Home"]
    A --> B["Ver lista de viagens com barra de ocupação"]
    B --> C{"Viagem disponível?"}
    C -- Não --> D["Exibir viagem esgotada (sem CTA)"]
    C -- Sim --> E["Clicar em Reservar"]
    E --> F["Preencher e-mail e quantidade de vagas"]
    F --> G["Submeter formulário"]
    G --> H{"Vagas suficientes?"}
    H -- Não --> I["Retornar HTTP 422 + Toast de erro"]
    H -- Sim --> J["Criar reserva com status CREATED"]
    J --> K["Redirecionar para painel do líder"]
```

---

## UC-02: Fluxo do Líder (Painel Autenticado)

```mermaid
flowchart TD
    L(["👤 Líder"])

    L --> A["Acessar painel 'Minhas Viagens'"]
    A --> B["Solicitar OTP via email"]
    B --> C["Receber e digitar código OTP"]
    C --> D{"OTP válido?"}
    D -- Não --> E["Exibir erro + opção de reenvio"]
    E --> B
    D -- Sim --> F["Acessar painel com reservas ativas"]

    F --> G{"Status da reserva?"}
    G -- CREATED --> H["Visualizar status pendente\nFormulário de acompanhantes BLOQUEADO"]
    G -- BLOCKED --> I["Cadastrar dados dos acompanhantes\nNome + RG"]
    G -- BLOCKED --> J["Visualizar e copiar voucher viral"]
    G -- CONFIRMED --> K["Visualizar confirmação final"]

    I --> L1{"Dados válidos?"}
    L1 -- Não --> M["Destacar campos inválidos sem limpar form"]
    L1 -- Sim --> N["Salvar e exibir mensagem de sucesso"]
```

---

## UC-03: Fluxo do Administrador (CRM Kanban)

```mermaid
flowchart TD
    A(["👤 Administrador"])

    A --> B["Acessar painel Kanban"]
    B --> C["Visualizar colunas de status:\nCREATED → BLOCKED → CONFIRMED → CANCELED"]
    C --> D["Analisar card de reserva"]
    D --> E{"Ação desejada?"}

    E -- Cobrança --> F["Clicar em 'Enviar cobrança'"]
    F --> G["Gerar deep-link WhatsApp com dados de PIX"]
    G --> H["Abrir WhatsApp sem alterar status no Kanban"]

    E -- Confirmação --> I["Arrastar card para nova coluna"]
    I --> J{"PATCH request bem-sucedido?"}
    J -- Sim --> K["Persistir novo status no banco de dados"]
    J -- Não --> L["Reverter card para posição anterior\n+ exibir Toast de erro de conexão"]
```

---

## UC-04: Casos de Erro (Resiliência do Sistema)

```mermaid
flowchart TD
    S(["⚙️ Sistema"])

    S --> A{"Operação que exige banco de dados"}
    A -- DB indisponível --> B["Retornar HTTP 503"]
    B --> C["Exibir mensagem de indisponibilidade temporária\nSem expor detalhes técnicos"]
    C --> D["Preservar dados do formulário na sessão"]

    A -- Timeout da API --> E["Manter loader ativo"]
    E --> F["Desabilitar botão de envio"]
    F --> G["Após timeout, exibir Toast de erro\nSem recarregar a página"]

    A -- Banco OK --> H["Processar operação normalmente"]
```
