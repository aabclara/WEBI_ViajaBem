"""
Sessão do banco de dados (SQLAlchemy 2.0).
Provê a dependency get_session para injeção nas rotas FastAPI.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://viajabem:viajabem@db:5432/viajabem")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """FastAPI dependency — abre e fecha a sessão de banco por requisição."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
