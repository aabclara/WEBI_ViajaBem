"""
Rota FastAPI: POST /admin/auth/login
Chama AdminLoginUseCase e retorna TokenResponse.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.domain.exceptions import InvalidCredentialsError
from backend.domain.use_cases.admin_auth import AdminLoginUseCase
from backend.infra.db.session import get_session
from backend.infra.repositories.user_repo import SQLUserRepository
from backend.infra.security.password_hasher import BcryptPasswordHasher
from backend.schemas.admin_auth import AdminLoginRequest, TokenResponse

router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


def _get_login_use_case(db: Session = Depends(get_session)) -> AdminLoginUseCase:
    return AdminLoginUseCase(
        user_repo=SQLUserRepository(db),
        password_hasher=BcryptPasswordHasher(),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login do Administrador",
    description=(
        "Autentica o administrador com email e senha. "
        "Retorna JWT Bearer Token com expiração de 8 horas."
    ),
)
async def admin_login(
    body: AdminLoginRequest,
    use_case: AdminLoginUseCase = Depends(_get_login_use_case),
) -> TokenResponse:
    try:
        return use_case.execute(email=body.email, password=body.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
