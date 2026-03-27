"""
AdminLoginUseCase — lógica pura de autenticação do administrador.
Não importa FastAPI, SQLAlchemy ou qualquer dependência de infraestrutura.
Depende apenas de interfaces abstratas (injeção de dependência).
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Protocol

from jose import jwt

from backend.domain.exceptions import InvalidCredentialsError
from backend.schemas.admin_auth import TokenResponse


class UserRepository(Protocol):
    """Interface abstrata — implementada pela camada de infra/SQLAlchemy."""

    def get_by_email(self, email: str):
        ...


class PasswordHasher(Protocol):
    """Interface abstrata — implementada pela camada de infra/passlib."""

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...


class AdminLoginUseCase:
    """
    Caso de uso: autenticação do administrador via email + password.

    Fluxo:
        1. Busca usuário por email no repositório.
        2. Verifica se o usuário existe e possui role=ADMIN.
        3. Verifica a senha via bcrypt.
        4. Gera e retorna JWT Bearer Token com expiração de 8h.

    Levanta InvalidCredentialsError em qualquer falha de autenticação
    sem expor qual etapa falhou (segurança por opacidade).
    """

    ALGORITHM = "HS256"

    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    def execute(self, email: str, password: str) -> TokenResponse:
        user = self._user_repo.get_by_email(email)

        # Falha genérica: não revela se é email ou senha o problema
        if user is None or getattr(user, "role", None) != "ADMIN":
            raise InvalidCredentialsError()

        if not self._password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError()

        return TokenResponse(access_token=self._generate_token(user))

    def _generate_token(self, user) -> str:
        secret = os.getenv("ADMIN_JWT_SECRET", "")
        expiration_hours = int(os.getenv("ADMIN_JWT_EXPIRATION_HOURS", "8"))

        expire = datetime.now(timezone.utc) + timedelta(hours=expiration_hours)
        payload = {
            "sub": str(user.id),
            "role": "ADMIN",
            "exp": expire,
        }
        return jwt.encode(payload, secret, algorithm=self.ALGORITHM)
