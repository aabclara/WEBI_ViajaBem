# Proposal: Admin Authentication (admin-auth-spec)

## Motivation

O painel administrativo do Viaje Bem possui rotas críticas de gestão (`/admin/reservas`, `/admin/viagens`) que atualmente não possuem especificação de autenticação. Sem esta spec, qualquer usuário poderia acessar e manipular o Kanban de reservas, alterar status de pagamento e criar pacotes de viagem, expondo o negócio a manipulações fraudulentas. Esta lacuna foi identificada como **bloqueante** no `implementation.md` (GAP-01).

## What Changes

Formalizar o mecanismo de autenticação exclusivo do administrador da agência:

- **Login do Admin:** Rota `POST /admin/auth/login` recebendo `email` + `password`. Admin é identificado por `role=ADMIN` na tabela `users` ou por variável de ambiente (`ADMIN_EMAIL` / `ADMIN_PASSWORD_HASH`). Retorna JWT Bearer Token com expiração de 8 horas.
- **Proteção de Rotas:** Todas as rotas sob `/admin/*` exigem header `Authorization: Bearer <token>`. Requisições sem token ou com token expirado retornam HTTP 403.
- **Logout / Expiração:** O token expira em 8h. Não há blacklist de tokens no MVP (stateless por design).

## Changed Requirements

- `specs/admin-management.md`: Os cenários de Kanban assumem admin autenticado mas não especificam como. Esta spec complementa aquela ao definir o fluxo de autenticação.
- `design.md` (sistema-viaje-bem): A tabela `users` com `role=ADMIN` já existe no schema. Esta spec formaliza o uso desse campo para autenticação.

## Impact

- Impacta a camada de infra (`backend/infra/http/middlewares/`) com um middleware JWT de verificação de role.
- Exige variável de ambiente `ADMIN_JWT_SECRET` no `.env` (já previsto no GAP-03 do `implementation.md`).
- Não altera o fluxo do líder (OTP) nem da vitrine pública — escopo restrito ao contexto admin.
