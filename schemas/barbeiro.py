from pydantic import BaseModel, Field


class BarbeiroBase(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    usuario: str = Field(min_length=3, max_length=150)

    class Config:
        orm_mode = True


class BarbeiroCreate(BarbeiroBase):
    senha: str = Field(min_length=3, max_length=255)


class BarbeiroResponse(BarbeiroBase):
    id: int
