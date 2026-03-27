"""
SQLUserRepository — implementação concreta de UserRepository usando SQLAlchemy 2.0.
"""

from sqlalchemy.orm import Session
from backend.infra.db.models import UserModel


class SQLUserRepository:
    """Implementa a interface UserRepository definida no domain/use_cases."""

    def __init__(self, db: Session):
        self._db = db

    def get_by_email(self, email: str):
        return (
            self._db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
