import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1,
    )

motor = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessaoLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor
)

Base = declarative_base()

from models.barbeiro import Barbeiro  # noqa: E402,F401
from models.cliente import Cliente  # noqa: E402,F401
from models.servico import Servico  # noqa: E402,F401
from models.agendamento import Agendamento  # noqa: E402,F401


def get_banco():
    banco = SessaoLocal()
    try:
        yield banco
    finally:
        banco.close()
