from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    duracao_minutos = Column(Integer, nullable=False)

    agendamentos = relationship("Agendamento", back_populates="servico")

