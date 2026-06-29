from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_banco
from services.agendamento_service import AgendamentoService

roteador = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"],
)


class AgendamentoCreate(BaseModel):
    barbeiro_id: int
    cliente_nome: str
    servico_id: int
    data: str
    horario_inicio: str


@roteador.get("")
def listar_agendamentos(
    barbeiro_id: int | None = Query(default=None),
    data: str | None = Query(default=None),
    db: Session = Depends(get_banco),
):
    service = AgendamentoService(db)
    return service.listar_agendamentos(barbeiro_id=barbeiro_id, data=data)


@roteador.post("")
def criar_agendamento(payload: AgendamentoCreate, db: Session = Depends(get_banco)):
    service = AgendamentoService(db)
    return service.criar_agendamento(
        barbeiro_id=payload.barbeiro_id,
        cliente_nome=payload.cliente_nome,
        servico_id=payload.servico_id,
        data=payload.data,
        horario_inicio=payload.horario_inicio,
    )


@roteador.delete("/{agendamento_id}")
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(get_banco)):
    service = AgendamentoService(db)
    return service.cancelar_agendamento(agendamento_id=agendamento_id)
