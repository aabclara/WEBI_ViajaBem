"""
Ponto de entrada da aplicação FastAPI — Viaje Bem API.
Registra todos os routers e aplica middlewares globais.
"""

from fastapi import FastAPI

from backend.infra.http.routes.admin_auth_routes import router as admin_auth_router

app = FastAPI(
    title="Viaje Bem API",
    description="Sistema de Gestão de Viagens — MVP",
    version="0.1.0",
)

# ─── Rotas Públicas ──────────────────────────────────────────────────
app.include_router(admin_auth_router)

# ─── Rotas Admin (protegidas por JWTAdminMiddleware via Depends) ─────
# Os routers abaixo serão adicionados conforme as demais features forem implementadas.
# Exemplo de como proteger uma rota futura:
#   from backend.infra.http.middlewares.jwt_admin import require_admin
#   @router.get("/reservas", dependencies=[Depends(require_admin)])
