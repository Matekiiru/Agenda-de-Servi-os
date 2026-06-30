from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql://postgres:1234@localhost:5432/barbearia"
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