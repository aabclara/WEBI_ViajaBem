# Tasks: Sistema Viaja Bem (MVP)

Abaixo estão as tarefas sequenciais derivadas da especificações do OpenSpec e do document de Design de Software, prontas para o início da fase de execução.

## 1. Fundação e Infraestrutura (DevOps & Docker)
- [ ] Criar template local base (FastAPI + Pydantic) para o Backend Python.
- [ ] Inicializar projeto escalável (Next.js 14+) para o Frontend.
- [ ] Escrever arquivo `docker-compose.yml` contendo os 3 principais serviços: PostgreSQL, Backend da API e App Frontend.
- [ ] Configurar integrações e schemas do GitHub Actions local para CI/CD inicial.

## 2. Modelagem do Domínio (DDD) e Banco de Dados
- [ ] Declarar as entidades do Python relativas à Camada de Negócios: `User`, `Trip`, `Reservation`, `Passenger`.
- [ ] Criar scripts de Migrations via ORM (ex: Alembic ou Prisma) refletindo as entidades criadas para os Tiers e Gamificação.
- [ ] Testes Unitários Base: Criar suite rodando `pytest` sobre a lógica que proíbe alterações no Tamanho de Combo se o Status for superior a "CREATED".

## 3. APIs REST e Lógica Administrativa
- [ ] Rota Básico de Login/Sessão (OTP e Password tradicional).
- [ ] Rota de Criação de Intenção (`POST /reservas` - Trancando Carrinho e Subtraindo Assentos das Entidades).
- [ ] Serviço de Workflow Admin: `PATCH /reservas/{id}/status` mudando estado do CRM (ex: Confirmando o Pagamento do Sinal para bloquear IDs de preenchimento).
- [ ] Gerar arquivo de contrato Swagger (openapi.json) a partir das rotas FastApi para ingestão no Frontend.

## 4. Frontend Funcional: UX/UI (Classic Minimalist)
- [ ] Estabelecer o Design System global via Tailwind CSS/Vanilla CSS, implementando tipografia suíça sólida, branco de alto contraste, cor de acento e áreas grandes para clique (Touch-Targets de 48px).
- [ ] Implementar Página de Catálogo (Home SSR) conectada à base, consumindo a porcentagem das "Vagas Gamificadas".
- [ ] Construir o Modal Lateral/PopUp do Cadastro inicial rápido do "Combo/Líder".
- [ ] Modelar "Dashboard do Usuário", criando painel responsivo onde são fornecidos RGs extras e exibido botão "Copiar Link para Acompanhantes".
- [ ] Tela do CRM Admin (Quadro Vertical Trello) permitindo mover Cards entre status via drag-n-drop/modais e botão de Zap (gerar redirect href whatsapp contendo string PIX pré montada).
