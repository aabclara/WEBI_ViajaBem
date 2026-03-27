from pydantic import BaseModel, EmailStr


class AdminLoginRequest(BaseModel):
    """Payload recebido na rota POST /admin/auth/login."""

    email: EmailStr
    password: str  # texto plano — comparação bcrypt ocorre no use case


class TokenResponse(BaseModel):
    """Resposta retornada após autenticação bem-sucedida do admin."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 28800  # 8 horas em segundos
