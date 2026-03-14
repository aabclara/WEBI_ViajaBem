# Tasks: Sistema Viaja Bem (MVP) - Micro-Passos

Este cronograma foi refatorado em micro-tarefas ("Small Chained Steps") para garantir que o desenvolvimento (seja por humanos ou IA) ocorra sem perda de contexto arquitetural. Nenhuma tarefa contém mais de um domínio lógico.

## Fase 1: Fundação & Infraestrutura (DevOps Inicial)
- [ ] **1.1.** Criar a pasta do Back-End `backend/` e inicializar o ambiente virtual Python (`venv`).
- [ ] **1.2.** Instalar as dependências base do Back-End: `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`, e `alembic`.
- [ ] **1.3.** Criar o arquivo `backend/main.py` com uma rota "Hello World" do FastAPI rodando.
- [ ] **1.4.** Criar a pasta do Front-End `frontend/` rodando `npx create-next-app@latest` (usando App Router e Tailwind).
- [ ] **1.5.** Redigir o arquivo `docker-compose.yml` na raiz do projeto contendo um container para o "PostgreSQL" local.

## Fase 2: Modelagem de Dados e ORM (DDD)
- [ ] **2.1.** Mapear Entidade/Tabela `User` no SQLAlchemy (Campos: id, name, email, role).
- [ ] **2.2.** Mapear Entidade/Tabela `Trip` no SQLAlchemy (Campos: id, destination, seats, price).
- [ ] **2.3.** Mapear Entidade/Tabela `Reservation` (FKs para User/Trip, comb_size e status enum).
- [ ] **2.4.** Mapear Entidade/Tabela `Passenger` (FK para Reservation, nome e RG).
- [ ] **2.5.** Gerar a primeira migration (`alembic revision --autogenerate`) contendo todas as 4 tabelas e rodar o `alembic upgrade head`.

## Fase 3: Regras Core de Negócio (Back-End)
- [ ] **3.1.** Codificar o *Controller/Router* de criação de Reserva (`POST /reservas`), recebendo um input Pydantic de `combo_size` e `email`.
- [ ] **3.2.** Codificar o Serviço (Use Case) que checa se o "Combo" requisitado não excede os Lugares Disponíveis da `Trip`.
- [ ] **3.3.** Codificar o Serviço de mudança de estado (`PATCH /reservas/{id}/status`) mudando de CREATED para BLOCKED.
- [ ] **3.4.** Escrever um teste unitário rústico (`pytest`) verificando que é impossível alterar o `combo_size` de uma reserva já `BLOCKED`.

## Fase 4: O Design System e Globals (Front-End)
- [ ] **4.1.** Injetar as cores oficiais (`#F7F2E8` Creme, `#0DBDC2` Ciano, `#FFA915` Laranja) no arquivo `tailwind.config.ts`.
- [ ] **4.2.** Importar e definir a família de fontes ('Inter' ou 'Roboto') como padrão global no `layout.tsx` e `globals.css`.
- [ ] **4.3.** Criar o componente base de "Botão Principal Primário" reutilizável (Tamanho 48px, Cor Laranja).

## Fase 5: Integração Telas Públicas (App UI)
- [ ] **5.1.** Construir o Layout Principal Vitrine (`page.tsx` home): Fundo Creme e o Header com as 4 âncoras ("Quem Somos", "Contato").
- [ ] **5.2.** Construir e importar os *Card Components* de Destino no grid da Home.
- [ ] **5.3.** Integrar a lógica da "Barra de Gamificação" nesses Cards, simulando a matemática de `(Ocupados / Vagas Totais) * 100` em Laranja.
- [ ] **5.4.** Construir o Modal Lateral/PopUp de Checkout que surge ao clicar no Card de Viagem.

## Fase 6: Integração Telas de Painéis (Burocracia & CRM)
- [ ] **6.1.** Construir a Tela de Login unificada (Tabulada entre "Usuário / Código" e "Senha").
- [ ] **6.2.** Desenvolver o "Dashboard Meu Painel" (Cliente): Renderizar a lista de viagens ativas com botões Laranja de Pagamento Pendente ou Ciano de Confirmado.
- [ ] **6.3.** Construir o fluxo dentro do Painel Cliente para Adicionar as strings de RG dependendo do tamanho do combo.
- [ ] **6.4.** Clicar e renderizar a Tela Isolada B2B: "Admin Login".
- [ ] **6.5.** Puxar o "CRM Kanban Admin" construindo as 4 colunas verticais CSS.
- [ ] **6.6.** Codificar os "Draggables Cards" (Intenções) e o botão com link SVG contendo o `href="https://wa.me/"` para cobrar o Pix.
- [ ] **6.7.** Finalizar com a UI Leve do Itinerário Público (Vírus Compartilhável) sem botões de edição de usuário.
