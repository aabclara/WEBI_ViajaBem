"""
Testes unitários (RED) para AdminLoginUseCase.
Padrão AAA: Arrange → Act → Assert
Estes testes devem FALHAR antes da implementação do use case.
"""

import pytest
from unittest.mock import MagicMock
from backend.domain.use_cases.admin_auth import AdminLoginUseCase
from backend.domain.exceptions import InvalidCredentialsError


class TestAdminLoginUseCase:
    """Suite TDD para o fluxo de autenticação do administrador."""

    def test_login_com_credenciais_validas_retorna_token_com_role_admin(self):
        # Arrange
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_email.return_value = MagicMock(
            id="uuid-admin-001",
            email="admin@viajabem.com",
            role="ADMIN",
            password_hash="$2b$12$hash_valido_aqui",
        )
        mock_password_hasher = MagicMock()
        mock_password_hasher.verify.return_value = True

        use_case = AdminLoginUseCase(
            user_repo=mock_user_repo,
            password_hasher=mock_password_hasher,
        )

        # Act
        token_response = use_case.execute(
            email="admin@viajabem.com",
            password="senha-correta",
        )

        # Assert
        assert token_response.access_token is not None
        assert token_response.token_type == "bearer"
        assert token_response.expires_in == 28800

    def test_login_com_senha_incorreta_levanta_invalid_credentials(self):
        # Arrange
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_email.return_value = MagicMock(
            id="uuid-admin-001",
            role="ADMIN",
            password_hash="$2b$12$hash_qualquer",
        )
        mock_password_hasher = MagicMock()
        mock_password_hasher.verify.return_value = False  # senha errada

        use_case = AdminLoginUseCase(
            user_repo=mock_user_repo,
            password_hasher=mock_password_hasher,
        )

        # Act + Assert
        with pytest.raises(InvalidCredentialsError):
            use_case.execute(email="admin@viajabem.com", password="senha-errada")

    def test_login_com_email_nao_cadastrado_levanta_invalid_credentials(self):
        # Arrange
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_email.return_value = None  # user não existe

        use_case = AdminLoginUseCase(
            user_repo=mock_user_repo,
            password_hasher=MagicMock(),
        )

        # Act + Assert
        with pytest.raises(InvalidCredentialsError):
            use_case.execute(
                email="nao-existe@viajabem.com",
                password="qualquer-senha",
            )

    def test_login_com_usuario_role_customer_levanta_invalid_credentials(self):
        # Arrange — role CUSTOMER não deve ter acesso admin
        mock_user_repo = MagicMock()
        mock_user_repo.get_by_email.return_value = MagicMock(
            id="uuid-customer-001",
            role="CUSTOMER",  # não é ADMIN
            password_hash="$2b$12$hash_qualquer",
        )
        mock_password_hasher = MagicMock()
        mock_password_hasher.verify.return_value = True  # senha certa, mas role errada

        use_case = AdminLoginUseCase(
            user_repo=mock_user_repo,
            password_hasher=mock_password_hasher,
        )

        # Act + Assert
        with pytest.raises(InvalidCredentialsError):
            use_case.execute(email="cliente@viajabem.com", password="senha-certa")
