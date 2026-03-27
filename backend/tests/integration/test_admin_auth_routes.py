"""
Testes de integração (RED) para as rotas de autenticação admin.
Usa httpx.AsyncClient contra a app FastAPI real (sem banco externo — fixtures in-memory).
Padrão AAA: Arrange → Act → Assert
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient

from backend.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def valid_admin_token(client):
    """Fixture que realiza login e retorna um token JWT válido de ADMIN."""
    response = await client.post(
        "/admin/auth/login",
        json={"email": "admin@viajabem.com", "password": "admin-senha-correta"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


class TestAdminAuthLogin:
    """Suite de testes de integração para POST /admin/auth/login."""

    async def test_login_com_credenciais_validas_retorna_200_com_token(self, client):
        # Arrange
        payload = {"email": "admin@viajabem.com", "password": "admin-senha-correta"}

        # Act
        response = await client.post("/admin/auth/login", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 28800

    async def test_login_com_credenciais_invalidas_retorna_401(self, client):
        # Arrange
        payload = {"email": "admin@viajabem.com", "password": "senha-errada"}

        # Act
        response = await client.post("/admin/auth/login", json=payload)

        # Assert
        assert response.status_code == 401
        assert "access_token" not in response.json()

    async def test_login_com_payload_incompleto_retorna_422(self, client):
        # Arrange — sem campo password
        payload = {"email": "admin@viajabem.com"}

        # Act
        response = await client.post("/admin/auth/login", json=payload)

        # Assert
        assert response.status_code == 422


class TestAdminRoutesProtection:
    """Suite de testes de integração para proteção das rotas /admin/*."""

    async def test_acesso_sem_token_retorna_403(self, client):
        # Act
        response = await client.get("/admin/reservas")

        # Assert
        assert response.status_code == 403

    async def test_acesso_com_token_expirado_retorna_403(self, client):
        # Arrange — token gerado manualmente com exp no passado
        import time
        from jose import jwt

        expired_token = jwt.encode(
            {"sub": "admin-id", "role": "ADMIN", "exp": int(time.time()) - 3600},
            key="qualquer-secret",
            algorithm="HS256",
        )

        # Act
        response = await client.get(
            "/admin/reservas",
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        # Assert
        assert response.status_code == 403

    async def test_acesso_com_token_de_customer_retorna_403(self, client):
        # Arrange — token com role=CUSTOMER
        import time
        from jose import jwt

        customer_token = jwt.encode(
            {"sub": "customer-id", "role": "CUSTOMER", "exp": int(time.time()) + 3600},
            key="qualquer-secret",
            algorithm="HS256",
        )

        # Act
        response = await client.get(
            "/admin/reservas",
            headers={"Authorization": f"Bearer {customer_token}"},
        )

        # Assert
        assert response.status_code == 403

    async def test_acesso_com_token_valido_de_admin_retorna_200(
        self, client, valid_admin_token
    ):
        # Act
        response = await client.get(
            "/admin/reservas",
            headers={"Authorization": f"Bearer {valid_admin_token}"},
        )

        # Assert
        assert response.status_code == 200
