# Tasks: Admin Authentication (admin-auth-spec)

Implementação sequenciada sob TDD e Clean Architecture. Ordem obrigatória: Infra → Domínio → TDD (red) → Implementação (green) → Integração.

## 1. Infraestrutura e Dependências

- [x] 1.1 Adicionar ao `backend/requirements.txt`: `python-jose[cryptography]` e `passlib[bcrypt]`
- [x] 1.2 Adicionar ao `.env.example` as variáveis `ADMIN_JWT_SECRET` e `ADMIN_JWT_EXPIRATION_HOURS=8`
- [x] 1.3 Criar `backend/schemas/admin_auth.py` com os schemas Pydantic v2: `AdminLoginRequest` (email, password) e `TokenResponse` (access_token, token_type, expires_in)

## 2. Domínio — Use Case (TDD: RED primeiro)

- [x] 2.1 **[RED]** Criar `backend/tests/unit/test_admin_login_use_case.py` com testes falhos:
  - Login com credenciais válidas retorna token com `role=ADMIN`
  - Login com senha incorreta levanta `InvalidCredentialsError`
  - Login com email não cadastrado levanta `InvalidCredentialsError`
- [x] 2.2 **[GREEN]** Criar `backend/domain/use_cases/admin_auth.py` — `AdminLoginUseCase`: busca user por email + verifica bcrypt hash + gera JWT assinado com `ADMIN_JWT_SECRET` até todos os testes ficarem verdes
- [x] 2.3 **[RED]** Criar `backend/tests/unit/test_jwt_middleware.py` com testes falhos:
  - Token válido com `role=ADMIN` passa pelo middleware
  - Token expirado retorna HTTP 403
  - Token adulterado/assinatura inválida retorna HTTP 403
  - Token com `role=CUSTOMER` retorna HTTP 403
  - Ausência de header `Authorization` retorna HTTP 403
- [x] 2.4 **[GREEN]** Criar `backend/infra/http/middlewares/jwt_admin.py` — `JWTAdminMiddleware` como FastAPI `Depends()`: decodifica JWT, valida `exp` e `role=ADMIN` até todos os testes passarem

## 3. Integração — Testes de Rota (TDD: RED primeiro)

- [x] 3.1 **[RED]** Criar `backend/tests/integration/test_admin_auth_routes.py` com suíte `httpx`:
  - `POST /admin/auth/login` com credenciais válidas → HTTP 200 + `access_token`
  - `POST /admin/auth/login` com credenciais inválidas → HTTP 401
  - `POST /admin/auth/login` com payload incompleto → HTTP 422
  - `GET /admin/reservas` sem token → HTTP 403
  - `GET /admin/reservas` com token expirado → HTTP 403
  - `GET /admin/reservas` com token de CUSTOMER → HTTP 403
  - `GET /admin/reservas` com token válido de ADMIN → HTTP 200
- [x] 3.2 **[GREEN]** Criar `backend/infra/http/routes/admin_auth_routes.py` — rota `POST /admin/auth/login` que chama `AdminLoginUseCase` e retorna `TokenResponse` até todos os testes de integração passarem
- [x] 3.3 Registrar o router de autenticação admin no `main.py` com prefixo `/admin/auth`
- [x] 3.4 Aplicar `JWTAdminMiddleware` como dependência em todos os routers sob `/admin/*` (exceto `/admin/auth/login`)

## 4. Validação Final

- [ ] 4.1 Executar `docker-compose run test pytest tests/unit/test_admin_login_use_case.py tests/unit/test_jwt_middleware.py -v` → todos GREEN
- [ ] 4.2 Executar `docker-compose run test pytest tests/integration/test_admin_auth_routes.py -v` → todos GREEN
- [ ] 4.3 Acessar `localhost:8000/docs` e verificar que `POST /admin/auth/login` aparece sem o cadeado e rotas `/admin/*` aparecem com cadeado de autenticação Bearer
- [ ] 4.4 Testar manualmente via Swagger: login com credenciais válidas → copiar token → usar "Authorize" → confirmar acesso às rotas protegidas
