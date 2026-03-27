"""Value object de autenticação — representa o token emitido após login bem-sucedido."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AuthToken:
    """
    Value object imutável retornado pelo AdminLoginUseCase.
    Não depende de FastAPI, Pydantic ou qualquer lib de infra.
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int = field(default=28800)  # 8 horas em segundos
