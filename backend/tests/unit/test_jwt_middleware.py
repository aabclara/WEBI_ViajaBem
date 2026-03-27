"""
Testes unitários (RED) para JWTAdminMiddleware.
Padrão AAA: Arrange → Act → Assert
Estes testes devem FALHAR antes da implementação do middleware existir.
"""

import pytest
import time
from unittest.mock import patch
from jose import jwt
from backend.infra.http.middlewares.jwt_admin import verify_admin_token
from backend.domain.exceptions import AdminTokenInvalidError

FAKE_SECRET = "secret-de-teste-com-pelo-menos-32-chars-ok"
ALGORITHM = "HS256"


def _make_token(payload: dict, secret: str = FAKE_SECRET) -> str:
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


class TestJWTAdminMiddleware:
    """Suite TDD para validação do JWT de administrador."""

    def test_token_valido_com_role_admin_passa_sem_erros(self):
        # Arrange
        payload = {
            "sub": "uuid-admin-001",
            "role": "ADMIN",
            "exp": int(time.time()) + 3600,
        }
        token = _make_token(payload)

        # Act + Assert — deve retornar o payload sem levantar exceção
        with patch("backend.infra.http.middlewares.jwt_admin.settings.ADMIN_JWT_SECRET", FAKE_SECRET):
            result = verify_admin_token(token)
            assert result["role"] == "ADMIN"
            assert result["sub"] == "uuid-admin-001"

    def test_token_expirado_levanta_admin_token_invalid(self):
        # Arrange
        payload = {
            "sub": "uuid-admin-001",
            "role": "ADMIN",
            "exp": int(time.time()) - 3600,  # expirado há 1 hora
        }
        token = _make_token(payload)

        # Act + Assert
        with patch("backend.infra.http.middlewares.jwt_admin.settings.ADMIN_JWT_SECRET", FAKE_SECRET):
            with pytest.raises(AdminTokenInvalidError, match="expirado"):
                verify_admin_token(token)

    def test_token_adulterado_levanta_admin_token_invalid(self):
        # Arrange
        payload = {
            "sub": "uuid-admin-001",
            "role": "ADMIN",
            "exp": int(time.time()) + 3600,
        }
        token = _make_token(payload)
        token_adulterado = token[:-5] + "XXXXX"  # corrompe a assinatura

        # Act + Assert
        with patch("backend.infra.http.middlewares.jwt_admin.settings.ADMIN_JWT_SECRET", FAKE_SECRET):
            with pytest.raises(AdminTokenInvalidError):
                verify_admin_token(token_adulterado)

    def test_token_com_role_customer_levanta_admin_token_invalid(self):
        # Arrange
        payload = {
            "sub": "uuid-customer-001",
            "role": "CUSTOMER",  # role incorreta
            "exp": int(time.time()) + 3600,
        }
        token = _make_token(payload)

        # Act + Assert
        with patch("backend.infra.http.middlewares.jwt_admin.settings.ADMIN_JWT_SECRET", FAKE_SECRET):
            with pytest.raises(AdminTokenInvalidError, match="role"):
                verify_admin_token(token)

    def test_ausencia_de_token_levanta_admin_token_invalid(self):
        # Arrange
        token = None

        # Act + Assert
        with patch("backend.infra.http.middlewares.jwt_admin.settings.ADMIN_JWT_SECRET", FAKE_SECRET):
            with pytest.raises(AdminTokenInvalidError):
                verify_admin_token(token)
