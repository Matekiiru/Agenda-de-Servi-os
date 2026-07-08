from pydantic import BaseModel, Field


class ClienteBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)

    class Config:
        orm_mode = True


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
