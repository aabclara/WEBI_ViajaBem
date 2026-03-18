# Tasks: Sistema Viaje Bem (MVP) - Sequência Atômica Inegociável

Estas tarefas refletem estritamente as decisões de design da Fricção Progressiva, Pagamento WhatsApp e Identidade Visual Clássica, envelopadas sob uma ordem de infraestrutura obrigatória para impedir perdas contextuais na IA.

## Fase 1: Orquestração e Base Isolada (Docker & PostgreSQL)
- [ ] **1.1.** Criar o `docker-compose.yml` especificando o serviço `db` (PostgreSQL 16, porta `5432`). Adicionar volumes locais para resiliência.
- [ ] **1.2.** Esboçar os `Dockerfile`s abstratos das pastas `backend/` (Python 3.12) e `frontend/` (Node 20).
- [ ] **1.3.** *[Validação]*: Executar `docker-compose up -d db`. Conectar o cliente local PostgreSQL e atestar tabelas zeradas.

## Fase 2: Backend Core - Domínio Viaje Bem e ORM (SQLModel)
- [ ] **2.1.** Na pasta `backend/`, instalar as dependências obrigatórias (`fastapi`, `sqlmodel`, `pydantic`, `alembic`, `psycopg2-binary`).
- [ ] **2.2.** Mapeamento Relacional: Configurar as quatro entidades essenciais mapeando a modelagem do arquivo Design (`User`, `Trip`, `Reservation`, `Passenger`) providenciando as Foreign Keys.
- [ ] **2.3.** Migrations: Inicializar o Alembic e gerar a migração zero para popular as tabelas reais no Docker DB.
- [ ] **2.4.** Schema Validation: Codificar os Schemas Pydantic. Criar Schema para "Intenção de Compra" validando restritamente o `combo_size`.
- [ ] **2.5.** Roteamento FastAPI de Fricção Progressiva: Codificar a Rota `POST /reservas` (Trancando a vaga e devolvendo Status `CREATED`).
- [ ] **2.6.** *[Validação]*: Ligar servidor uvicorn. Acessar `/docs` Swagger e popular via UI 1 Cliente, 1 Viagem e postar sucesso de 1 Reserva. Testar se o Pydantic retorna `HTTP 422 HTTPValidationError` para `combo_size` inválido.

## Fase 3: Bootstrap Frontend Estilo Clássico (Next.js & shadcn/ui)
- [ ] **3.1.** Inicializar app `frontend/` com Router, TypeScript Estrito e Tailwind (`npx create-next-app@latest`).
- [ ] **3.2.** Iniciar o CLI headless do Shadcn (`npx shadcn-ui@latest init`).
- [ ] **3.3.** Gerar o Pool de Componentes autorizados: `npx shadcn-ui@latest add button card dialog table input form toast progress`.
- [ ] **3.4.** Purgar CSS e forçar o Design System no `tailwind.config.ts`: Creme (`#F7F2E8`), Laranja da Escassez (`#FFA915`), e Ciano de Confiança (`#0DBDC2`) como variáveis CSS centrais. Adicionar pacote `lucide-react`.

## Fase 4: Engenharia de Telas (Views Específicas)
- [ ] **4.1.** Construir a "Home / Vitrine": Server Component. Estruturar "Split-Hero" no topo com chamada Laranja e Renderizar o Grid das viagens puxando API com `fetch()`. Usar `<Card>` e implementar a Barra de Gamificação dinâmica no botão Ciano inferior puxando componente `<Progress />` shadcn envelopado no valor matemático da lotação da base.
- [ ] **4.2.** Construir a Área de Checkout Oculto: Client Component acoplado e interativo usando o modal de base `<Sheet>`. Permitir a requisição em Fricção Mínima sem cobrar senhas robustas no input. 
- [ ] **4.3.** Construir a Tela Client "Minhas Viagens": O Painel de burocracia onde o líder visualizará na `<Table>` suas Reservas. Aqui fica embutido os avisos (Status Laranja "Falta Zap 50% Pix", ou Liberação Ciano "Cadastrar RGs" dos amigos da van).
- [ ] **4.4.** Construir o CRM Kanban do Administrador: Desenvolver a interface 4 colunas em React (Novos -> Sinal Pago -> Confirmados -> Cancelados) gerando os crachás arrastáveis e provendo o Botão do WhatsApp (com lucide-icon) que envia Link do banco pro zap. 
- [ ] **4.5.** *[Validação]*: Simular a falha completa de API enviando Request ao backend fechado. O Painel Front-End MUST disparar `<Toast variant="destructive">` via Hooks Shadcn impedindo falha catastrófica da Janela sem alterar arrays locais.
