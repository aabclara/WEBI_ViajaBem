# Design Técnico Detalhado: Sistema Viaje Bem MVP

Este documento define as diretrizes arquiteturais estritas e infraestrutura do projeto, assegurando conformidade visual exata com os layouts estabelecidos (`docs/`) e prevenindo invenções no frontend/backend.

## 1. Topologia de Infraestrutura (Docker Orquestration)
O ecossistema inteiro MUST ser distribuído e executado mandatoriamente via `docker-compose`. Execuções avulsas nos hosts nativos são desencorajadas.
- **db:** Container oficial rodando `PostgreSQL 16+`.
- **api:** Container Python `3.12+` hospedando Uvicorn/FastAPI.
- **web:** Container Node `20+` rodando o Next.js App Router (Modo Standalone).

## 2. Governança Front-End (Next.js & shadcn/ui)
O projeto utilizará **TypeScript Estrito** (sem exceções linter).

### Separação de Rendering (RSC vs Client)
O Next.js exige clareza sobre onde o JavaScript interativo carrega.
- **Server Components (Default):** As rotas matriciais (ex: `app/page.tsx`, `app/admin/page.tsx`) e layouts globais MUST operar Server-Side para assegurar o ciclo natural de Data-Fetching da base de viagens e o SEO absoluto do catálogo.
- **Client Components (`"use client"`):** Extensões isoladas de árvore MUST ser marcadas explicitamente como Client-side apenas quando necessitarem de Hooks (`useState`, `useEffect`) ou Listeners. Exemplos arquiteturais:
  - Paineis de Formulários (`Dialog`/`Sheet` de Checkout).
  - Motores Drag and Drop da tela do Kanban (`SortableContext`).
  - Barras Dinâmicas de Progresso e Menus Sanduíche.

### Mapeamento Estrito de UI Component (shadcn/ui e Lucide)
A criação de componentes crus usando classes de TailwindCSS para tentar montar caixas e modais está PROIBIDA. A UI MUST mapear-se inteiramente sobre `shadcn/ui` gerados localmente reproduzindo a imagem guia:
- `Button:` (Implementação de todas CTA laranjas de 56px e secundários ciano).
- `Card`, `CardHeader`, `CardContent`: (Envelopamento para cada Viagem na Vitrine da Home).
- `Sheet` ou `Dialog`: (Intervenção progressiva do Checkout do Cliente na Tela sem routing externo).
- `Table` / `DataTable`: (Dashboard do Líder para manipulação dos passageiros e exibição de faturas).
- `Progress`: (Barra indicativa física do overbooking gamificando estoques).
- `Input`, `Form`, `Toast`: (Gerenciadores visuais para submissões Zod em formulários).
- **Iconografia:** Todos os SVGs MUST provir da lib `lucide-react`. O uso de emojis na tipografia corporativa é uma infração grave.

## 3. Back-End Core e Banco de Dados (FastAPI + SQLAlchemy)
Integração física em TypeScript-Like Types acoplada sobre o ecossistema `Pydantic v2` para parsing.

### Estruturas Relacionais Aprovadas (PostgreSQL)

**Tabela: `users`**
- `id`: UUID (Primary Key).
- `email`: Varchar (Constraint Unique, BTREE Indexado para auth).
- `role`: Enum Estrito (`CUSTOMER`, `ADMIN`).

**Tabela: `trips`**
- `id`: UUID (Primary Key).
- `destination`: Varchar.
- `total_seats`: Integer. (Fonte inegociável da verdade para ocupação).
- `start_date`: DateTime (Indexed).

**Tabela: `reservations` (Corpo Transacional)**
- `id`: UUID (Primary Key).
- `trip_id`: UUID (Foreign Key, `ON DELETE CASCADE`), Indexado para COUNTS do Frontend gamificado.
- `user_id`: UUID (Foreign Key).
- `combo_size`: Integer.
- `status`: Enum (`CREATED`, `BLOCKED`, `CONFIRMED`, `CANCELED`).

**Tabela: `passengers`**
- `id`: UUID (Primary Key).
- `reservation_id`: UUID (Foreign Key).
- `name`: Varchar (NOT NULL) — nome completo do acompanhante.
- `rg`: Varchar (NOT NULL).

---

## 4. Contratos Pydantic (TypeSafe)

Todos os schemas abaixo MUST ser definidos com `Pydantic v2` na camada `backend/schemas/`. A rota FastAPI não aceita inputs não tipados por estes modelos.

**`ReservationCreate`** — payload enviado pelo frontend ao criar uma reserva
```python
class ReservationCreate(BaseModel):
    email: EmailStr       # e-mail do líder
    trip_id: UUID
    combo_size: int       # mínimo 1, máximo total_seats disponíveis
```

**`ReservationResponse`** — resposta retornada pela API após criação bem-sucedida
```python
class ReservationResponse(BaseModel):
    id: UUID
    status: ReservationStatus  # Enum: CREATED | BLOCKED | CONFIRMED | CANCELED
    trip_id: UUID
    combo_size: int
```

**`PassengerCreate`** — payload para cadastrar um acompanhante no painel do líder
```python
class PassengerCreate(BaseModel):
    name: str             # nome completo
    rg: str               # documento RG
    reservation_id: UUID
```

**`UserAuth`** — payload inicial de autenticação (dispara envio do OTP)
```python
class UserAuth(BaseModel):
    email: EmailStr
```

**`OTPVerify`** — payload para validar o código OTP recebido por email
```python
class OTPVerify(BaseModel):
    email: EmailStr
    code: str             # código numérico de 6 dígitos
```

---

## 5. Índices do Banco (PostgreSQL)

Os índices abaixo MUST ser declarados explicitamente nas migrations do Alembic para garantir desempenho nas queries críticas.

| Tabela | Coluna | Tipo | Constraint | Finalidade |
|---|---|---|---|---|
| `users` | `email` | BTREE | UNIQUE | Autenticação e busca do líder |
| `reservations` | `trip_id` | BTREE | — | Contagem de vagas ocupadas (gamificação) |
| `reservations` | `user_id` | BTREE | — | Listagem de reservas no painel do líder |
| `trips` | `start_date` | BTREE | — | Ordenação do catálogo de viagens |
