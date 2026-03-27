# Design: Admin Authentication (admin-auth-spec)

## Background

O sistema Viaje Bem já possui a tabela `users` com campo `role: Enum(CUSTOMER, ADMIN)` definida no `design.md` do change `sistema-viaje-bem`. Esta spec complementa aquela modelagem, definindo a camada de autenticação que protege todas as rotas `/admin/*`.

## Goals / Non-Goals

**Goals:**
- Definir o mecanismo de login do administrador via `email` + `password`
- Especificar a geração e validação de JWT Bearer Token para o admin
- Especificar o middleware de proteção das rotas `/admin/*`
- Garantir que o mecanismo seja stateless (sem necessidade de Redis no MVP)

**Non-Goals:**
- Recuperação de senha do admin (escopo pós-MVP)
- Múltiplos administradores com permissões diferentes (RBAC) — MVP opera com role binário `ADMIN`
- Autenticação 2FA para o admin (pós-MVP)

## Architecture

### Mecanismo escolhido: JWT Bearer Token (stateless)

**Decisão:** JWT com expiração de 8h, assinado com secret injetado via variável de ambiente `ADMIN_JWT_SECRET`.

**Justificativa:** Stateless elimina necessidade de Redis ou banco de sessões no MVP, reduzindo infraestrutura. Para uso single-admin em baixo volume, o risco de token comprometido é mitigado pela expiração curta (8h).

### Fluxo de Autenticação

```
Cliente (browser admin)
    │
    ▼
POST /admin/auth/login  {email, password}
    │
    ▼
FastAPI Route → AdminAuthUseCase
    │  ├─ Busca user por email (role=ADMIN)
    │  ├─ Verifica hash bcrypt da password
    │  └─ Gera JWT {sub: user.id, role: "ADMIN", exp: now+8h}
    │
    ▼
Response: { access_token, token_type: "bearer", expires_in: 28800 }

─────────────── REQUISIÇÕES SUBSEQUENTES ───────────────

GET/POST/PATCH /admin/*
    │
    ▼
JWTAdminMiddleware
    │  ├─ Verifica presença do header Authorization: Bearer <token>
    │  ├─ Decodifica e valida assinatura com ADMIN_JWT_SECRET
    │  ├─ Verifica expiração (exp claim)
    │  └─ Verifica role == "ADMIN"
    │
    ├──[VÁLIDO]──▶ Injeta admin_user no request state → rota executada
    └──[INVÁLIDO]─▶ HTTP 403 Forbidden
```

### Estrutura de Pastas (Clean Architecture)

```
backend/
  domain/
    use_cases/
      admin_auth.py           ← AdminLoginUseCase (lógica pura, sem FastAPI)
  infra/
    http/
      middlewares/
        jwt_admin.py          ← JWTAdminMiddleware (FastAPI Dependency)
      routes/
        admin_auth_routes.py  ← POST /admin/auth/login
  schemas/
    admin_auth.py             ← AdminLoginRequest, TokenResponse (Pydantic v2)
```

### Contratos Pydantic v2

```python
# schemas/admin_auth.py

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str          # plaintext — bcrypt comparison happens in use case

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 28800    # 8 horas em segundos
```

### Variáveis de Ambiente Necessárias

```
ADMIN_JWT_SECRET=<string aleatória min. 32 chars>
ADMIN_JWT_EXPIRATION_HOURS=8
```

## Decisions

| Decisão | Alternativa considerada | Razão da escolha |
|---------|------------------------|-----------------|
| JWT stateless | Sessão server-side (Redis) | MVP sem Redis; complexidade desnecessária |
| bcrypt para hash de senha | argon2 | bcrypt maduro, passlib[bcrypt] já está nos requirements |
| Expiração de 8h | 24h ou sem expiração | Balanceamento entre usabilidade (jornada de trabalho) e segurança |
| Role verificada no JWT | Consulta ao banco a cada request | Performance: evita round-trip ao DB em toda requisição admin |

## Risks / Trade-offs

- **Token comprometido:** Sem blacklist no MVP, um token vazado permanece válido até expirar (8h). Mitigação: HTTPS obrigatório em produção.
- **Admin único:** Estrutura atual não suporta múltiplos admins com roles distintos. Aceitável para MVP de agência pequena.
