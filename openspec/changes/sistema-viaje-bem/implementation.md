# Implementation Plan — Sistema Viaje Bem (MVP)

> **Gerado em:** 2026-03-27  
> **Metodologia:** Spec-Driven Development + TDD + Clean Architecture  
> **Stack (config.yaml):** FastAPI + Pydantic v2 + SQLAlchemy 2.0 + PostgreSQL 16 | Next.js App Router + TypeScript estrito + shadcn/ui + Tailwind CSS | Docker + docker-compose

---

## 📋 DIAGNÓSTICO DE AUDITORIA

### 1. Estado do `archive/`

| Diretório | Estado |
|-----------|--------|
| `openspec/changes/archive/` | **VAZIO** |
| `openspec/changes/sistema-viaje-bem/` | **ATIVO** — nenhuma mudança foi consolidada |

> **Conclusão:** Todo o escopo de `sistema-viaje-bem` está pendente de implementação. Nenhum artefato foi arquivado.

---

### 2. Validação dos Artefatos Obrigatórios

| Artefato | Existe? | Diagnóstico |
|----------|---------|-------------|
| `proposal.md` | ✅ | Escopo claro: vitrine gamificada, painel líder, CRM Kanban. Sem gateway de pagamento. |
| `design.md` | ✅ | Docker topology, 4 entidades DB, contratos Pydantic v2, índices Alembic. |
| `tasks.md` | ✅ | 4 fases com padrão TDD explícito. Completo mas não sequenciado por camada arquitetural. |
| `specs/core-booking-flow.md` | ✅ | 6 cenários Gherkin cobrindo reserva, overbooking, OTP e voucher. |
| `specs/leader-panel-flow.md` | ✅ | 5 cenários Gherkin cobrindo painel do líder. |
| `specs/admin-management.md` | ✅ | 3 cenários Gherkin cobrindo Kanban e WhatsApp. |
| `specs/trip-management.md` | ✅ | 5 cenários Gherkin cobrindo CRUD de viagens. |
| `specs/frontend-ui-ux.md` | ⚠️ | Apenas 2 cenários. Cenários comportamentais testáveis ausentes (Toast, loading, disabled state). |
| `specs/admin-auth.md` | ❌ | **AUSENTE.** Mecanismo de autenticação do administrador não especificado. |
| `decision_log.md` | ✅ | 4 decisões aprovadas e 4 descartadas documentadas. |

### 3. Gaps de Consistência Detectados

| Gap | Tipo | Impacto |
|-----|------|---------|
| Autenticação admin não especificada (JWT vs sessão, credencial via env vs DB) | Spec faltante | **Bloqueante** — rotas `/admin/*` não podem ser implementadas sem essa decisão |
| `frontend-ui-ux.md` sem cenários comportamentais (Toast, pending, disabled) | Spec incompleta | Testes frontend sem contrato formal |
| `tasks.md` sequência não respeita hierarquia Infra → Domínio → TDD → Integração → Interface | Ordenação | Risco de implementar lógica antes de testes passando |
| Sem `.env.example` previsto em nenhum artefato | Infra omitida | Configuração de banco/secrets não documentada |
| Campos `price_per_person` e `image_url` usados nos cenários de `trip-management.md` mas ausentes do DB schema em `design.md` | Inconsistência | Modelagem incompleta — migrations falharão |

---

## 🗂️ PLANO DE IMPLEMENTAÇÃO REVISADO

> **Convenções injetadas do `config.yaml`:**
> - Todos os artefatos em **Português do Brasil**
> - Cláusulas RFC 2119 (MUST, SHALL, SHOULD, MUST NOT) nas regras
> - Specs em Gherkin (Dado/Quando/Então)
> - Ordem de execução: Docker → PostgreSQL → FastAPI → Next.js/UI
> - Proibido citar libs Python/JS nas specs
> - Proibido usar `any` no TypeScript

---

## NÍVEL 0 — PRÉ-CONDIÇÃO: Corrigir Gaps Bloqueantes

> Estes itens MUST ser resolvidos antes de qualquer implementação.

### [GAP-01] Criar `specs/admin-auth.md`
Definir cenários Gherkin para:
- Login do admin com credenciais válidas (usuário/senha via variável de ambiente ou tabela `users` com `role=ADMIN`)
- Tentativa de acesso a rota `/admin/*` sem autenticação → HTTP 403
- Expiração de sessão/token → redirecionamento para login

**Decisão arquitetural necessária:** JWT Bearer Token (stateless, adequado para MVP Docker) ou sessão server-side (exige Redis, complexidade extra).
> **Recomendação:** JWT com expiração de 8h, secret via variável de ambiente `ADMIN_JWT_SECRET`.

### [GAP-02] Atualizar `design.md` — Tabela `trips`
Adicionar campos ausentes identificados nos cenários de `trip-management.md`:
```
trips:
  + price_per_person: Numeric(10,2) NOT NULL
  + cover_image_url:  Varchar (nullable → upload externo ou URL)
  + end_date:         DateTime NOT NULL
  + is_active:        Boolean DEFAULT True (controla visibilidade na vitrine)
```

### [GAP-03] Criar `.env.example` na raiz do projeto
```
DATABASE_URL=postgresql://user:password@db:5432/viajabem
ADMIN_JWT_SECRET=changeme
OTP_EXPIRATION_MINUTES=10
```

---

## NÍVEL 1 — INFRAESTRUTURA

> Objetivo: ambiente de execução e testes 100% containerizado e reproduzível.

### INFRA-01 — `docker-compose.yml` (raiz do projeto)
Três serviços obrigatórios segundo `design.md`:

```
Serviço: db
  image: postgres:16-alpine
  portas: 5432:5432
  volume: ./volumes/postgres:/var/lib/postgresql/data
  env: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

Serviço: api
  build: ./backend (Python 3.12)
  command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
  portas: 8000:8000
  depends_on: db

Serviço: web
  build: ./frontend (Node 20 standalone)
  command: npm run dev
  portas: 3000:3000
  depends_on: api

Serviço: test (modo CI)
  build: ./backend
  command: pytest --tb=short -v --asyncio-mode=auto
  depends_on: db
```

### INFRA-02 — `backend/Dockerfile`
```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### INFRA-03 — `frontend/Dockerfile`
```
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
```

### INFRA-04 — `backend/requirements.txt`
```
fastapi==0.111.*
uvicorn[standard]
sqlalchemy==2.0.*
alembic
psycopg2-binary
pydantic[email]==2.*
python-jose[cryptography]    # JWT admin
passlib[bcrypt]              # hash de senha
pytest
pytest-asyncio
httpx
```

### INFRA-05 — Migração Alembic: `alembic init`
Configurar `alembic.ini` com `DATABASE_URL` via env. Gerar migration zero com as 4 tabelas + campos adicionados no GAP-02.

**Validação INFRA:**  
Executar `docker-compose up -d db` → conectar cliente PostgreSQL → confirmar tabelas criadas sem erros.

---

## NÍVEL 2 — DOMÍNIO (Core — sem dependências de framework)

> Objetivo: lógica de negócio em Python puro. Nenhum import de SQLAlchemy ou FastAPI aqui.

### DOMAIN-01 — Value Object: `ReservationStatus`
```
Localização: backend/domain/value_objects/reservation_status.py
Valores: CREATED | BLOCKED | CONFIRMED | CANCELED
```

### DOMAIN-02 — Entidade: `Reservation`
```
Localização: backend/domain/entities/reservation.py
Comportamentos a implementar (métodos puros):
  - can_add_passengers() → bool  [BLOCKED only]
  - is_combo_editable()  → bool  [CREATED only]
  - transition_to(new_status)    [valida transições legais]
```

**Transições legais (Spec core-booking-flow):**
```
CREATED  → BLOCKED    (admin confirma sinal)
CREATED  → CANCELED   (admin cancela)
BLOCKED  → CONFIRMED  (admin confirma total)
BLOCKED  → CANCELED   (admin cancela)
CONFIRMED → (imutável)
CANCELED  → (imutável)
```

### DOMAIN-03 — Entidade: `Trip`
```
Localização: backend/domain/entities/trip.py
Comportamentos:
  - available_seats(reserved: int) → int
  - is_sold_out(reserved: int)     → bool
  - can_reduce_seats(new_total, reserved) → bool  [Spec trip-management]
```

### DOMAIN-04 — Regra de Negócio: Overbooking
```
Localização: backend/domain/rules/overbooking.py
Função: validate_booking(trip_total_seats, already_reserved, requested) → raises DomainError se inválido
```

### DOMAIN-05 — Interface (Abstract): `ReservationRepository`
```
Localização: backend/domain/repositories/reservation_repo.py
Métodos abstratos: save(), get_by_id(), list_by_user(), update_status()
```

### DOMAIN-06 — Interface (Abstract): `TripRepository`
```
Localização: backend/domain/repositories/trip_repo.py
Métodos abstratos: save(), get_by_id(), list_active(), get_seat_count()
```

---

## NÍVEL 3 — TDD: TESTES PRIMEIRO (Padrão AAA)

> Regra absoluta: **nenhum código de produção de domínio ou use case é escrito antes do teste correspondente estar RED.**

### Bloco A — Testes Unitários de Domínio

#### TEST-DOM-01 — Transições de status da reserva
```
Arquivo: backend/tests/unit/test_reservation_entity.py

AAA — Teste 1: CREATED não pode adicionar passageiros
  Arrange: reservation = Reservation(status=CREATED)
  Act:     result = reservation.can_add_passengers()
  Assert:  result is False

AAA — Teste 2: BLOCKED pode adicionar passageiros
  Arrange: reservation = Reservation(status=BLOCKED)
  Act:     result = reservation.can_add_passengers()
  Assert:  result is True

AAA — Teste 3: CONFIRMED não permite mais transições
  Arrange: reservation = Reservation(status=CONFIRMED)
  Act:     reservation.transition_to(CANCELED)
  Assert:  raises DomainError

AAA — Teste 4: Transição válida CREATED → BLOCKED
  Arrange: reservation = Reservation(status=CREATED)
  Act:     reservation.transition_to(BLOCKED)
  Assert:  reservation.status == BLOCKED
```

#### TEST-DOM-02 — Regra de Overbooking
```
Arquivo: backend/tests/unit/test_overbooking_rule.py

AAA — Teste 1: Reserva aceita com vagas suficientes
  Arrange: total=10, reserved=7, requested=2
  Act:     validate_booking(10, 7, 2)
  Assert:  sem exceção

AAA — Teste 2: Reserva recusada por overbooking
  Arrange: total=10, reserved=9, requested=2
  Act:     validate_booking(10, 9, 2)
  Assert:  raises OverbookingError

AAA — Teste 3: Reserva de exatamente o último assento
  Arrange: total=10, reserved=9, requested=1
  Act:     validate_booking(10, 9, 1)
  Assert:  sem exceção
```

#### TEST-DOM-03 — Trip: proteção de vagas com reservas ativas
```
Arquivo: backend/tests/unit/test_trip_entity.py

AAA — Teste 1: Redução de vagas bloqueada
  Arrange: trip = Trip(total_seats=10), reserved=8
  Act:     trip.can_reduce_seats(new_total=7, reserved=8)
  Assert:  False

AAA — Teste 2: Redução de vagas permitida
  Arrange: trip = Trip(total_seats=10), reserved=5
  Act:     trip.can_reduce_seats(new_total=6, reserved=5)
  Assert:  True
```

### Bloco B — Testes de Use Cases

#### TEST-UC-01 — CreateReservation
```
Arquivo: backend/tests/unit/test_use_case_create_reservation.py

AAA — Teste 1: Criação bem-sucedida
  Arrange: mock TripRepository retorna trip com 5 vagas livres
           mock ReservationRepository.save() aceita
  Act:     CreateReservation(trip_repo, res_repo).execute(trip_id, email, combo_size=2)
  Assert:  ReservationRepository.save() chamado 1x com status=CREATED

AAA — Teste 2: Falha por overbooking
  Arrange: mock TripRepository retorna trip com 0 vagas livres
  Act:     CreateReservation(...).execute(trip_id, email, combo_size=1)
  Assert:  raises OverbookingError

AAA — Teste 3: Falha por trip_id inexistente
  Arrange: mock TripRepository.get_by_id() retorna None
  Act:     CreateReservation(...).execute(trip_id_invalido, ...)
  Assert:  raises TripNotFoundError
```

#### TEST-UC-02 — UpdateReservationStatus (Admin Kanban)
```
Arquivo: backend/tests/unit/test_use_case_update_status.py

AAA — Teste 1: Transição válida persiste
  Arrange: mock repo retorna reservation CREATED
  Act:     UpdateStatus(repo).execute(res_id, new_status=BLOCKED)
  Assert:  repo.update_status() chamado com BLOCKED

AAA — Teste 2: Transição inválida não persiste
  Arrange: mock repo retorna reservation CONFIRMED
  Act:     UpdateStatus(repo).execute(res_id, new_status=CANCELED)
  Assert:  raises DomainError; repo.update_status() NÃO chamado
```

#### TEST-UC-03 — AddPassengers
```
Arquivo: backend/tests/unit/test_use_case_add_passengers.py

AAA — Teste 1: Passageiros adicionados em reserva BLOCKED
  Arrange: mock repo retorna reservation BLOCKED, combo_size=3
  Act:     AddPassengers(repo).execute(res_id, passengers=[p1, p2, p3])
  Assert:  passenger_repo.save_all() chamado com lista de 3

AAA — Teste 2: Bloqueado em reserva CREATED
  Arrange: mock repo retorna reservation CREATED
  Act:     AddPassengers(repo).execute(res_id, passengers=[p1])
  Assert:  raises PassengerFormLockedError
```

### Bloco C — Testes de Integração (Rotas FastAPI via httpx)

> Estes testes usam banco de dados real em container `test-db`. Executados via `docker-compose run test`.

#### TEST-ROUTE-01 — POST /reservas
```
Arquivo: backend/tests/integration/test_reservation_routes.py

Cenário (Spec core-booking-flow): Criação com fricção mínima
  Request:  POST /reservas  {email, trip_id, combo_size: 2}
  Assert:   HTTP 201, body.status == "CREATED"

Cenário: Overbooking
  Request:  POST /reservas  {combo_size: vagas + 1}
  Assert:   HTTP 422, body.detail contém mensagem de disponibilidade

Cenário: Payload inválido (email faltante)
  Request:  POST /reservas  {trip_id, combo_size}
  Assert:   HTTP 422 (Pydantic ValidationError)
```

#### TEST-ROUTE-02 — PATCH /reservas/{id}/status
```
Arquivo: backend/tests/integration/test_admin_routes.py

Cenário (Spec admin-management): Drag & Drop Kanban
  Request:  PATCH /admin/reservas/{id}/status  {status: "BLOCKED"}  [com header Authorization JWT]
  Assert:   HTTP 200, body.status == "BLOCKED"

Cenário: Transição inválida
  Request:  PATCH /admin/reservas/{id}/status  {status: "CANCELED"}  [reserva CONFIRMED]
  Assert:   HTTP 409 Conflict

Cenário: Sem token JWT
  Request:  PATCH /admin/reservas/{id}/status  [sem Authorization header]
  Assert:   HTTP 403 Forbidden

Cenário: DB indisponível durante PATCH (Spec admin-management — falha de conexão)
  Request:  PATCH com banco derrubado
  Assert:   HTTP 503 Service Unavailable
```

#### TEST-ROUTE-03 — POST /auth/otp e POST /auth/otp/verify
```
Arquivo: backend/tests/integration/test_auth_routes.py

Cenário (Spec core-booking-flow): OTP enviado por e-mail
  Request:  POST /auth/otp  {email: "lider@email.com"}
  Assert:   HTTP 200, (mock SMTP verificado chamado 1x)

Cenário: OTP inválido
  Request:  POST /auth/otp/verify  {email, code: "000000"}
  Assert:   HTTP 401 Unauthorized

Cenário: OTP expirado
  Request:  POST /auth/otp/verify com OTP > OTP_EXPIRATION_MINUTES
  Assert:   HTTP 401 com mensagem de expiração
```

---

## NÍVEL 4 — INTERFACE: Camada FastAPI

> Use cases prontos e testados MUST existir antes de criar a rota correspondente.

### ROUTE-01 — `/reservas` (Public)
```
POST   /reservas                → CreateReservation use case
GET    /reservas/{id}           → GetReservation use case (acesso via OTP token)
```

### ROUTE-02 — `/auth` (Public)
```
POST   /auth/otp                → dispara envio OTP ao e-mail do líder
POST   /auth/otp/verify         → valida código + retorna JWT do líder
POST   /admin/auth/login        → credenciais admin → JWT admin (GAP-01 resolvido)
```

### ROUTE-03 — `/painel` (Líder — JWT protegido)
```
GET    /painel/reservas                        → lista reservas do líder autenticado
POST   /painel/reservas/{id}/passageiros       → AddPassengers use case
GET    /painel/reservas/{id}/voucher           → retorna link viral
```

### ROUTE-04 — `/admin` (Admin — JWT protegido)
```
GET    /admin/reservas                         → lista todas as reservas (Kanban data)
PATCH  /admin/reservas/{id}/status             → UpdateStatus use case
POST   /admin/viagens                          → CreateTrip use case
PUT    /admin/viagens/{id}                     → UpdateTrip use case
GET    /admin/viagens/{id}/whatsapp-link        → gera deep-link WhatsApp/PIX
```

### ROUTE-05 — `/viagens` (Public — SSR Next.js consome)
```
GET    /viagens                                → lista viagens ativas com contagem de vagas
GET    /viagens/{id}                           → detalhe da viagem
```

---

## NÍVEL 5 — FRONTEND (Next.js)

> Seguir hierarquia idêntica: Bootstrap → Design System → TDD componentes → Views SSR → Client Islands.

### FRONT-INFRA-01 — Bootstrap Next.js App Router
```
Comando: npx create-next-app@latest ./frontend --typescript --tailwind --app --no-src-dir --no-import-alias
Instalar shadcn: npx shadcn-ui@latest init
Gerar componentes: npx shadcn-ui@latest add button card dialog table input form toast progress sheet
Instalar testes: npm install -D vitest jsdom @testing-library/react @testing-library/user-event @vitejs/plugin-react
Instalar validação: npm install zod react-hook-form @hookform/resolvers
Instalar DnD: npm install @dnd-kit/core @dnd-kit/sortable
```

### FRONT-INFRA-02 — Design System no `tailwind.config.ts`
```
Cores obrigatórias (config.yaml + MASTER.md):
  primary:          #FFA914  (laranja urgência/gamificação)
  accent-teal:      #0DBDC2  (ciano ação/confiança)
  background-light: #F7F2E8  (creme global)
  background-dark:  #231C0F  (header/footer)
  card-white:       #FFFFFF
  text-main:        #1F1F1F
Fonte: Inter (400/500/700/900) via Google Fonts
```

### FRONT-TDD-01 — Testes de componentes (Vitest + testing-library)
```
Arquivo: frontend/__tests__/components/TripCard.test.tsx

AAA — Barra de progresso reflete ocupação correta
  Arrange: render(<TripCard totalSeats={10} reservedSeats={8} />)
  Act:     —
  Assert:  getByRole("progressbar") tem value="80"

AAA — Botão Reservar desabilitado quando esgotado
  Arrange: render(<TripCard totalSeats={10} reservedSeats={10} />)
  Act:     —
  Assert:  getByRole("button", {name: /reservar/i}) está disabled

```

```
Arquivo: frontend/__tests__/components/CheckoutSheet.test.tsx

AAA — Botão desabilitado durante pending (Spec frontend-ui-ux)
  Arrange: render(<CheckoutSheet />), mock fetch pendente
  Act:     userEvent.click(getByRole("button", {name: /reservar/i}))
  Assert:  botão fica disabled durante a requisição

AAA — Toast de erro exibido em falha de rede
  Arrange: mock fetch rejeita com network error
  Act:     userEvent.click(botão de envio)
  Assert:  getByRole("alert") contém texto de erro
```

```
Arquivo: frontend/__tests__/components/KanbanBoard.test.tsx

AAA — Card reverte posição em erro de PATCH (Spec admin-management)
  Arrange: render(<KanbanBoard reservations={[...]} />), mock PATCH retorna 503
  Act:     simular drag do card para nova coluna
  Assert:  card retorna à coluna original; Toast de erro visível
```

### FRONT-VIEWS-01 — Server Components (SSR)
```
app/page.tsx            → busca /viagens (fetch server-side), renderiza TripGrid
app/admin/page.tsx      → Server Component → passa dados para KanbanBoard (Client)
app/painel/page.tsx     → OTP-guard → lista reservas do líder
```

### FRONT-VIEWS-02 — Client Islands
```
components/features/vitrine/TripCard.tsx       → "use client" — Progress + Sheet de checkout
components/features/checkout/CheckoutSheet.tsx → "use client" — react-hook-form + Zod + Toast
components/features/kanban/KanbanBoard.tsx     → "use client" — dnd-kit + Optimistic UI
components/features/leader/PassengerForm.tsx   → "use client" — react-hook-form, bloqueado se CREATED
```

---

## ✅ CHECKLIST DE VALIDAÇÃO FINAL (por nível)

| Nível | Evidência de conclusão |
|-------|----------------------|
| INFRA | `docker-compose up -d db api` sobe sem erros; `/docs` Swagger acessível em `localhost:8000` |
| DOMÍNIO | `docker-compose run test pytest tests/unit/ -v` → todos GREEN |
| TDD Rotas | `docker-compose run test pytest tests/integration/ -v` → todos GREEN |
| INTERFACE Backend | Swagger `/docs` reflete todas as rotas; Pydantic retorna HTTP 422 em payload inválido manualmente |
| INFRA Frontend | `npm run dev` sobe; Tailwind aplica cores corretas; shadcn componentes importáveis |
| TDD Frontend | `npm run test` → todos os testes Vitest GREEN |
| INTERFACE Frontend | Vitrine exibe viagens com barra de progresso laranja; checkout via Sheet sem routing externo; Kanban com drag-and-drop funcional |

---

## 🚫 RESTRIÇÕES INEGOCIÁVEIS (RFC 2119 — config.yaml)

- `domain/` MUST NOT importar de `infra/`, `schemas/` ou FastAPI
- Nenhuma rota FastAPI SHALL ser adicionada sem teste de integração correspondente GREEN
- TypeScript MUST ser estrito — proibido `any` em qualquer arquivo `.ts` / `.tsx`
- Componentes UI MUST usar exclusivamente shadcn/ui — proibido `<button>` ou `<div>` crus para CTAs
- Ícones MUST provir de `lucide-react` — emojis e SVGs inline são infração
- Nenhuma migration Alembic SHALL ser commitada sem passar no step INFRA-05 de validação
- Ordem de execução MUST ser: Docker → PostgreSQL → FastAPI → Next.js/UI
