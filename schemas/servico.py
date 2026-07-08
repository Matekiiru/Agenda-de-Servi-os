from pydantic import BaseModel, Field


class ServicoBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    duracao_minutos: int = Field(gt=0)

    class Config:
        orm_mode = True


class ServicoCreate(ServicoBase):
    pass


class ServicoResponse(ServicoBase):
    id: int
