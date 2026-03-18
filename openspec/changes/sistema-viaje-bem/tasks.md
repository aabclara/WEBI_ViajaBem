# Tasks: Sistema Viaje Bem (MVP) - Sequência TDD & SDD Inegociável

Estas tarefas refletem estritamente as decisões de design da Fricção Progressiva, Pagamento WhatsApp e Identidade Visual Clássica, agora envelopadas sob a doutrina de **Test-Driven Development (TDD)** e a infraestrutura obrigatória para impedir perdas contextuais na IA.

## Fase 1: Orquestração e Base Isolada (Docker & PostgreSQL)
- [ ] **1.1.** Criar o `docker-compose.yml` especificando o serviço `db` (PostgreSQL 16, porta `5432`). Adicionar volumes locais para resiliência.
- [ ] **1.2.** Esboçar os `Dockerfile`s abstratos das pastas `backend/` (Python 3.12) e `frontend/` (Node 20).
- [ ] **1.3.** *[Validação]*: Executar `docker-compose up -d db`. Conectar o cliente local PostgreSQL e atestar tabelas zeradas.

## Fase 2: Backend Core - Execução Strict TDD (FastAPI & Pytest)
- [ ] **2.1.** Na pasta `backend/`, instalar dependências obrigatórias (`fastapi`, `sqlmodel`, `pydantic`, `alembic`, `psycopg2-binary`) e a suíte de testes (`pytest`, `pytest-asyncio`, `httpx`).
- [ ] **2.2.** **[TDD do domínio]** Escrever testes Pytest unitários (falhos/red) para as regras lógicas centrais: transições do `status` (CREATED -> BLOCKED -> CONFIRMED) e limites de Overbooking validando `total_seats` vs `combo_size`.
- [ ] **2.3.** **[Implementar domínio]** Mapeamento Relacional: Configurar as quatro entidades essenciais mapeando a modelagem do arquivo Design (`User`, `Trip`, `Reservation`, `Passenger`) providenciando as Foreign Keys no `SQLModel` até os testes ficarem verdes.
- [ ] **2.4.** **[TDD dos casos de uso]** Projetar asserções contra injeções de payloads JSON futuros da área comercial, garantindo que CPFs vazios ou Compras sem vagas emitam falhas de formulário.
- [ ] **2.5.** **[Implementar casos de uso]** Schema Validation: Codificar os Schemas Pydantic v2 de Requests e Responses, em especial o Schema restrito para "Intenção de Compra". 
- [ ] **2.6.** **[TDD dos componentes da API]** Escrever suítes isoladas para as dependências cruciais (A conexão injetada do banco genérica e os validadores de autenticação JWT/Middlewares).
- [ ] **2.7.** **[Implementar os componentes]** Codificar as instâncias de Dependência do FastAPI (`Depends(get_session)`) e os formatadores de Payload DTO.
- [ ] **2.8.** **[TDD das rotas]** Programar scripts Client `httpx` de Pytest batendo massivamente no `/reservas` e `/admin/board`, exigindo interceptações `HTTP 201`, `HTTP 400` ou `HTTP 422`. 
- [ ] **2.9.** **[Implementar as rotas]** Roteamento FastAPI: Codificar definitivamente a Rota de Fricção Progressiva (`POST /reservas`) e as interações do Kanban até cimentar a API ao Swagger.
- [ ] **2.10.** **[Testes de integração com o banco]** Inicializar o Alembic, gerar a migração zero. Subir o container local, despachar queries orquestradas de Criação/Deleção de "Passageiros" atestando se a tabela filha exclui as chaves da transação Órfã (`ON DELETE CASCADE`).
- [ ] **2.11.** *[Validação Lógica]*: Acessar `/docs` Swagger e testar se o Pydantic retorna `HTTP 422 HTTPValidationError` com erro explícito de Domínio manual.

## Fase 3: Bootstrap Frontend Autêntico & Vitest Setup (Next.js)
- [ ] **3.1.** Inicializar app `frontend/` com Router, TypeScript Estrito e Tailwind (`npx create-next-app@latest`). Instalar framework de TDD visual (`vitest`, `jsdom`, `@testing-library/react`).
- [ ] **3.2.** Iniciar o CLI headless do Shadcn (`npx shadcn-ui@latest init`).
- [ ] **3.3.** Gerar o Pool de Componentes autorizados: `npx shadcn-ui@latest add button card dialog table input form toast progress`.
- [ ] **3.4.** Purgar CSS e forçar o Design System no `tailwind.config.ts`: Creme (`#F7F2E8`), Laranja da Escassez (`#FFA915`), e Ciano de Confiança (`#0DBDC2`) como variáveis centrais. Importar conjunto fixo `lucide-react`.

## Fase 4: Engenharia de Views Guiada por TDD Frontend
- [ ] **4.1.** **[TDD dos componentes da API (React)]** Forçar testes com `@testing-library/react` em cima de pedaços de UI (Mockar a passagem de *props* para a Barra Gamificada exibindo Laranja/80% e checar se Modais abrem sob clique ciano).
- [ ] **4.2.** **[Implementar os componentes]** Construir a "Home / Vitrine": Renderizar "Split-Hero" e o Grid das viagens. Implementar a Barra `<Progress />` dinâmica no botão inferior da entidade Viagem importada.
- [ ] **4.3.** **[Implementar os componentes]** Construir a Área de Checkout Oculto do Carrinho: Elemento Client Component interativo usando `<Sheet>`. Permitir formulário react-hook-form de Fricção Mínima limpa.
- [ ] **4.4.** **[Implementar os componentes]** Construir a Tela "Minhas Viagens": O Painel `<Table>` de burocracia civil embutindo botões Ciano para RGs ou chamadas Laranjas para WhatsApp/PIX.
- [ ] **4.5.** **[Implementar os componentes]** Construir o CRM Kanban do Administrador: Fazer grid React das colunas DND (Novos -> Sinal -> Confirmados) com Deep Linking pro WhatsApp.
- [ ] **4.6.** **[TDD das rotas]** Implementar Suíte Vitest asserindo em instâncias roteáveis com utilitários de servidor *Mockado* (ex: MSW) que o `app/page.tsx` levanta a listagem quando fetch bate e lida saudável com arrays vazias (fallback de sem dados).
- [ ] **4.7.** **[Implementar as rotas]** Executar acoplamento arquitetural nas páginas SSR do Next.js fechando o circuito via Redes Reais pra porta Python.
- [ ] **4.8.** **[Testes de integração com o banco]** Teste *Full End-to-End* (E2E) simulado ou real contra as APIs do FastAPI pra fechar se o payload do React preenche matematicamente as Foreign Keys do SQLModel em integridade total de sessão.
- [ ] **4.9.** *[Validação Integral]*: Simular drop sistêmico enviando Request ao backend fechado. O Front-End MUST disparar `<Toast variant="destructive">` via Hooks impedindo falha catastrófica silenciosa.
