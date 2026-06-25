from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Barbeiro(Base):
    __tablename__ = "barbeiros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    usuario = Column(String(150), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    agendamentos = relationship("Agendamento", back_populates="barbeiro")

