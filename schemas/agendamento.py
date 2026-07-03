from datetime import date, time

from pydantic import BaseModel, Field


class AgendamentoCreate(BaseModel):
    barbeiro_id: int
    cliente_nome: str = Field(min_length=2, max_length=150)
    servico_id: int
    data: date
    horario_inicio: time

    class Config:
        orm_mode = True


class AgendamentoResponse(BaseModel):
    id: int
    barbeiro_id: int
    barbeiro: str
    cliente: str
    servico: str
    duracao: int
    data: date
    horario_inicio: time
    status: str

    class Config:
        orm_mode = True
