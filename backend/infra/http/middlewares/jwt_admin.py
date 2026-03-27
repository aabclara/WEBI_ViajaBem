"""
JWTAdminMiddleware — FastAPI Dependency para proteção de rotas /admin/*.
Valida Bearer Token, expiração e role=ADMIN.
"""

import os
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from backend.domain.exceptions import AdminTokenInvalidError

_bearer_scheme = HTTPBearer(auto_error=False)

ALGORITHM = "HS256"


def verify_admin_token(token: Optional[str]) -> dict:
    """
    Decodifica e valida o JWT do administrador.
    Levanta AdminTokenInvalidError em qualquer falha.
    Função pura — testável sem contexto HTTP.
    """
    if not token:
        raise AdminTokenInvalidError("Token ausente")

    secret = os.getenv("ADMIN_JWT_SECRET", "")
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise AdminTokenInvalidError("Token expirado. Faça login novamente.")
    except JWTError:
        raise AdminTokenInvalidError("Token inválido")

    role = payload.get("role")
    if role != "ADMIN":
        raise AdminTokenInvalidError(f"Acesso negado: role '{role}' não tem permissão admin.")

    return payload


async def require_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> dict:
    """
    FastAPI Dependency — injeta payload do admin ou levanta HTTP 403.
    Uso: adicionar `admin=Depends(require_admin)` em qualquer rota /admin/*.
    """
    token = credentials.credentials if credentials else None
    try:
        return verify_admin_token(token)
    except AdminTokenInvalidError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )
