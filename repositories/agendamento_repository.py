from datetime import date

from sqlalchemy.orm import Session

from models.agendamento import Agendamento
from models.barbeiro import Barbeiro
from models.cliente import Cliente
from models.servico import Servico


class AgendamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, barbeiro_id: int | None = None, data: date | None = None):
        query = self.db.query(Agendamento).join(Cliente).join(Servico).join(Barbeiro)

        if barbeiro_id is not None:
            query = query.filter(Agendamento.barbeiro_id == barbeiro_id)

        if data is not None:
            query = query.filter(Agendamento.data == data)

        return query.order_by(Agendamento.data.asc(), Agendamento.horario_inicio.asc()).all()

    def buscar_por_id(self, agendamento_id: int):
        return self.db.query(Agendamento).filter(Agendamento.id == agendamento_id).first()

    def buscar_conflitos(self, barbeiro_id: int, data_agendamento: date):
        return (
            self.db.query(Agendamento)
            .filter(
                Agendamento.barbeiro_id == barbeiro_id,
                Agendamento.data == data_agendamento,
                Agendamento.status != "cancelado",
            )
            .all()
        )

    def criar(self, agendamento: Agendamento):
        self.db.add(agendamento)
        self.db.commit()
        self.db.refresh(agendamento)
        return agendamento

    def cancelar(self, agendamento: Agendamento):
        self.db.delete(agendamento)
        self.db.commit()
