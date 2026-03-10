# Design: Sistema Viaja Bem (MVP Agência Gamificada)

## Architecture

O sistema será fundamentado em um modelo Cliente-Servidor distribuído, empregando princípios sólidos de Engenharia de Software Moderna (Clean Architecture e Domain-Driven Design) com suporte a picos de tráfego.

*   **Front-End:** Next.js (React) utilizando estratégias híbridas:
    *   *Server-Side Rendering (SSR):* Para indexação no Google das páginas de viagem (Catálogo).
    *   *Client-Side Rendering (CSR):* Para os cronômetros escassos e atualização reativa da Barra de Gamificação (Tiers de Assentos).
    *   *UI Philosophy:* "Minimalist Classic" (WCAG AA Compliance, Whitespace brutal, touch targets massivos, e tipografia estrutural robusta em tons cinza/Branco + 1 cor de acento profunda).
*   **Back-End:** Python com FastAPI para alta performance em rotas assíncronas, sustentando múltiplos paginadores e validadores Pydantic estritos para os formulários de reserva. O design do backend obedecerá à **Clean Architecture** para blindar a lógica sensível do negócio.
*   **Integração e Contratos:** Comunicação Front-End/Back-End inteiramente viabilizada e tipada através de contratos **OpenAPI (Swagger)** gerados a partir do FastAPI.
*   **Infraestrutura e Deploy:** Ambiente multi-container orquestrado via **Docker** (Banco de dados, FastAPI Microservice e Node.js Client). 

## Data Flow

1. **Catálogo & Intenção (Fricção Progressiva):** Usuário visualiza viagens pela Vitrine SSR e seleciona um Ticket "Combo".
2. **Reserva (CREATED):** O usuário "Líder" provê o Login (Híbrido Clássico ou OTP Magic Link) e reserva o Combo de `X` cadeiras. O banco de dados bloqueia `X` Vagas relativas à Ocupação Total da Excursão provisoriamente.
3. **Comunicação Externa e Pagamento:** A intenção cai no kanban do Administrador. A agência engaja o cliente manualmente (WhatsApp / wa.me link generation). O pagamento Pix de 50% é processado externamente em canais bancários diretos (Não há Gateway Stripe/Iugu nativo).
4. **Reserva (BLOCKED) & Fricção Tardia:** Uma vez computado o Pix, o Admin altera a intenção de `CREATED` para `BLOCKED`. Isso congela a reserva (O Líder perde a permissão de editar o seu quantitativo de acentos autonomamente). Nesse estágio, o Front-End exige que o Líder complete os formulários adicionais de IDs (RGs) de seus Passageiros convidados. Se houver falha na montagem/desistência de algum acompanhante do grupo, a moderação e readequação de valores deve ser solicitada em suporte ao Admin, transferindo a lógica dura sistêmica para a atuação via processo humano de suporte.
5. **Reserva (CONFIRMED):** Após finalizados os RGs e quitação total, gera-se o Link Master de compartilhamento "Read-Only" do itinerário.

## Data Model

O banco de dados (Relacional via ORM) modelará o domínio central focado em conversões:

- **User:** Perfil do sistema definindo papéis (`Admin` ou `Customer/Leader`).
- **Trip:** Agregador Principal (Aggregate Root em DDD). Contém `Destination`, `Data Inicial/Final`, `Total Seats`, `Base Cost`. Contará com regras embutidas virtuais de "Desbloqueios de Tiers" (Exemplo: Se 30 reservas confirmadas, upgrade Pousada) derivadas da soma das sub-reservas atreladas a ele.
- **Reservation (Intent):** Entidade atrelada à Trip e ao User Leader. Possui o Estado Cíclico rígido (`CREATED`, `BLOCKED`, `CONFIRMED`, `CANCELED`). Possui `combo_size` inteiro, guardando os "carrinhos" travados temporariamente.
- **Passenger:** Entidade sub-atrelada exclusiva de detalhamento da `Reservation`. Só exigível após a reserva passar para `BLOCKED`. Contém `Name`, `Phone` e `Documentation ID`.
