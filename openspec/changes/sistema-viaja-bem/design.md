# Design Técnico Detalhado: Sistema Viaja Bem MVP

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
- `rg`: Varchar.
