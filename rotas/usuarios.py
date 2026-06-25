from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_banco
from core.jwt import criar_token
from models.barbeiro import Barbeiro

roteador = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
)


@roteador.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_banco),
):
    barbeiro = (
        db.query(Barbeiro)
        .filter(Barbeiro.usuario == form_data.username)
        .first()
    )

    if not barbeiro or form_data.password != barbeiro.senha:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token(
        {
            "sub": str(barbeiro.id),
            "usuario": barbeiro.usuario,
            "nome": barbeiro.nome,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "barbeiro": {
            "id": barbeiro.id,
            "name": barbeiro.nome,
            "user": barbeiro.usuario,
        },
    }
