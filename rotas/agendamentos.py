from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_banco
from schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from services.agendamento_service import AgendamentoService

roteador = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"],
)


@roteador.get("", response_model=list[AgendamentoResponse])
def listar_agendamentos(
    barbeiro_id: int | None = Query(default=None),
    data: date | None = Query(default=None),
    db: Session = Depends(get_banco),
):
    service = AgendamentoService(db)
    return service.listar_agendamentos(barbeiro_id=barbeiro_id, data=data)


@roteador.post("", response_model=AgendamentoResponse)
def criar_agendamento(payload: AgendamentoCreate, db: Session = Depends(get_banco)):
    service = AgendamentoService(db)
    return service.criar_agendamento(payload=payload)


@roteador.delete("/{agendamento_id}")
def cancelar_agendamento(agendamento_id: int, db: Session = Depends(get_banco)):
    service = AgendamentoService(db)
    return service.cancelar_agendamento(agendamento_id=agendamento_id)
