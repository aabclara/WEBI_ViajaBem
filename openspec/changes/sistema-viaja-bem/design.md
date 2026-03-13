# Design Técnico Detalhado: Sistema Viaja Bem (MVP Agência Gamificada)

## 1. Objetivo do Sistema
O **Sistema Viaja Bem** tem como objetivo central automatizar a captação de clientes e a gestão de vendas de viagens curtas (micro-trips de finais de semana) através de uma **Vitrine Gamificada**. O sistema resolve o problema da alta fricção na organização de grupos de viagem, gerando "Senso de Urgência" (FOMO) ao exibir o preenchimento de vagas em tempo real e oferecendo benefícios coletivos (ex: upgrade de ônibus) conforme a excursão enche. Tudo isso é gerenciado por um **CRM Kanban Admin** onde a agência controla os recebimentos financeiros **manualmente e de forma externa** (via WhatsApp/Pix), minimizando os custos operacionais e jurídicos de um gateway Pagar.me/Stripe no MVP.

---

## 2. Visão Geral do Funcionamento (Operation)
O funcionamento da plataforma divide-se em três jornadas interligadas:

1.  **A Jornada de Captura (Vitrine e Líder de Viagem):**
    *   O usuário ("Líder") acessa a Vitrine e visualiza destinos filtrados por mês/estilo.
    *   A interface exibe urgência explícita (Ex: "Faltam apenas 4 vagas para garantir o Ônibus Semi-Leito").
    *   O Líder seleciona a quantidade de ingressos que deseja ("Combo") e trava a sua reserva fornecendo apenas dados de contato básicos (Email/Telefone).
    *   O sistema imediatamente retira temporariamente essas vagas do estoque (Status `CREATED`).
2.  **A Jornada de Venda (O Admin no Kanban):**
    *   A reserva "CREATED" aparece no painel do administrador.
    *   O Admin clica no Card do cliente, que abre um link direto para o WhatsApp com uma cobrança de 50% de sinal já pré formatada e as chaves Pix.
    *   Após o recebimento do comprovante no WhatsApp, o Admin move o Card para a coluna `BLOCKED`. A reserva do Líder é congelada matematicamente no sistema.
3.  **A Jornada Burocrática (Dashboard do Líder Pós-Venda):**
    *   Com a reserva `BLOCKED`, a vaga do Líder e seus convidados está garantida.
    *   O Líder loga em seu Dashboard restrito. Apenas agora o sistema obriga o Líder a cadastrar os RGs e Nomes completos dos seus Acompanhantes.
    *   Após quitação total, a reserva ganha status `CONFIRMED` e gera um link "Somente Leitura" para o líder enviar aos amigos no grupo do WhatsApp, contendo os horários e informações da viagem.

---

## 3. Arquitetura de Software e Componentes (Technical Stack)
A solução adota um modelo **Cliente-Servidor Distribuído**, projetado sob os preceitos do **Domain-Driven Design (DDD)** e da **Clean Architecture** aplicados no backend.

### 3.1. Front-End (Apresentação e Consumo)
*   **Framework:** **Next.js 14+ (React)**.
*   **Rendering Híbrido:** 
    *   **SSR (Server-Side Rendering):** Utilizado nas páginas de Catálogo (SEO amigável) para que as viagens indexem ativamente em motores de busca.
    *   **CSR (Client-Side Rendering):** Utilizado nos elementos dinâmicos (Barra de Progresso, Cronômetros de Urgência, Painel Privado do Líder).
*   **Design System:** CSS nativo ou TailwindCSS, operando estritamente sob a estética **"Minimalist Classic"** (alta resposta tátil, tipografia limpa, acessibilidade máxima).

### 3.2. Back-End (Lógica de Domínio e APIs)
*   **Framework:** **Python com FastAPI**. Execução Assíncrona via `Uvicorn/Gunicorn` garantindo performance não-bloqueante nos picos de acesso.
*   **Clean Architecture (Separação em Camadas):**
    *   *Domain/Core:* Entidades puras do negócio (User, Trip, Reservation) e Regras estritas (Ex: Regras de upgrade de Tier ou restrição matemática de exclusão de reservas). ZERO dependência de Python frameworks.
    *   *Use Cases/Application:* A orquestração (Ex: `CreateReservationUseCase`, `UpdateReservationStatusUseCase`).
    *   *Adapters:* Interfaces convertendo dados do HTTP (Rotas FastAPI) para requisições que o Core entenda.
    *   *Infrastructure:* Implementação real do Banco de Dados (PostgreSQL via SQLAlchemy/Alembic) e criptografia de senhas.
*   **Contrato de API:** Validação massiva de inputs executada nativamente pelo **Pydantic**. Especificações injetadas diretamente em **OpenAPI (Swagger)**.

### 3.3. Infraestrutura e DevOps
*   **Containerização:** O projeto será unificado via **Docker / Docker Compose**, garantindo isolamento total entre o Banco, a API FastAPI e o servidor Next.js. Prontificado para Deploy na Nuvem (AWS/Render/Vercel).
*   **CI/CD Pipeline:** Uso de **GitHub Actions** configurado para barrar códigos que não passem nos **Testes Unitários (Pytest)**.

---

## 4. Arquitetura do Banco de Dados (Data Model Detail)
Uma modelagem relacional rígida **(PostgreSQL)** contendo as quatro pedras angulares do domínio (Aggregates).

### Entidade: `User` (Usuários / Líderes e Admins)
Os indivíduos que acessam o sistema. Acompanhantes de viagem *não possuem* esta entidade (eles não fazem login).
*   `id` (UUID - PK)
*   `name` (Varchar 150)
*   `email` (Varchar 255 - Unique / Index Indexado)
*   `password_hash` (Varchar)
*   `role` (Enum: `CUSTOMER`, `ADMIN`) - Restringe o acesso ao CRM Kanban.
*   `created_at` / `updated_at` (Timestamps)

### Entidade: `Trip` (As Viagens Oferecidas)
O pacote base de venda ofertado na Vitrine. Atua como o "Root Aggregate" para a contagem de lotação.
*   `id` (UUID - PK)
*   `title` (Varchar 100) - Ex: "Fim de Semana em Capitólio"
*   `destination` (Varchar 100)
*   `base_price` (Decimal)
*   `start_date` / `end_date` (DateTime)
*   `total_seats` (Integer) - O estoque absoluto de lugares no ônibus/hotel.
*   `status` (Enum: `DRAFT`, `PUBLISHED`, `SOLD_OUT`, `COMPLETED`)

### Entidade: `Reservation` (O Combo/Intenção de Compra)
A relação transacional entre um usuário líder e a viagem. Aqui moram as lógicas de bloqueio gamificado.
*   `id` (UUID - PK)
*   `trip_id` (UUID - FK para Trip)
*   `leader_user_id` (UUID - FK para User)
*   `combo_size` (Integer) - Número de cadeiras que o líder puxou para sua reserva (ex: 4 lugares).
*   `status` (Enum: `CREATED` = Novo; `BLOCKED` = Sinal Pago [congela edição de combo]; `CONFIRMED` = 100% Pago; `CANCELED` = Excluída).
*   `expires_at` (DateTime) - Prazos gerados para Urgência de sinal (ex: cai em 24h se o sinal não for pago).

### Entidade: `Passenger` (Os Acompanhantes e Burocracia)
Só é preenchida pelo Líder após a `Reservation` pular para o status de permissão correta.
*   `id` (UUID - PK)
*   `reservation_id` (UUID - FK vinculando ao Combo do Líder)
*   `full_name` (Varchar 200)
*   `rg_document` (Varchar 50) - Documento de identidade exigido para lista de embarque.
*   `is_leader` (Boolean) - Diferencia a linha do passageiro que efetuou a compra dos convidados.

---

## 5. Funções Core do Sistema (Domínio)

A lógica central processará as funções críticas do Back-End sem necessitar intervenção humana ou scripts engessados de banco de dados:

1.  **`CalculateTripOccupancy()`**: Função estrita de domínio. Soma constantemente todas as instâncias de `Reservations` que estejam em fase `CREATED/BLOCKED/CONFIRMED` para uma `Trip` específica. Retorna em `%` (Porcentagem) e números fixos (Ex: "38 de 40") para alimentar as Barras Gamificadas sem causar "Overbooking".
2.  **`LockReservationCombo(reservation_id)`**: Uma vez que o Front-End Admin despache um *Patch* migrando a Reserva de `CREATED` para `BLOCKED`, a camada Service congela o `combo_size`. Qualquer tentativa do Front-End cliente de enviar um "Excluir um passageiro" no combo é negada por erro de domínio (HTTP 403 Forbidden Business Rule).
3.  **`AutoCancelExpiredReservations()`**: Uma rotina nativa/background process do FastAPI garantindo que Vagas de impulso não se tornem Vagas Zumbis. Se um `expires_at` expira sem que o Admin mova o fluxo da Intent para Bloqueado, o pacote retorna para a Vitrine (Esgotando urgência).
4.  **`GenerateReadOnlyItinerary(...)`**: Cria chaves temporárias criptografadas para formar a Rota Publica "Link a ser enviado no WhatsApp pros acompanhantes". Isso permite bater no servidor Next.js renderizando apenas layout informativo passivo para convidados.
