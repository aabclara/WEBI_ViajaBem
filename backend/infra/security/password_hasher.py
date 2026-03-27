"""
BcryptPasswordHasher — implementação concreta da interface PasswordHasher.
Usa passlib + bcrypt para verificação segura de senhas.
"""

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher:
    """Implementa a interface PasswordHasher definida no use case."""

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)

    def hash(self, plain_password: str) -> str:
        """Utilitário para gerar hashes — usado em seeds/migrations."""
        return _pwd_context.hash(plain_password)
