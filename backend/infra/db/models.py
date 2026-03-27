"""
SQLAlchemy Models — mapeamento das entidades do domínio para tabelas PostgreSQL.
Definido conforme o schema em design.md (change sistema-viaje-bem).
"""

import uuid
from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(
        Enum("CUSTOMER", "ADMIN", name="user_role"),
        nullable=False,
        default="CUSTOMER",
    )
