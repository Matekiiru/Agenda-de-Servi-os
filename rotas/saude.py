from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session


from core.auth import obter_usuario_logado
from core.database import get_banco

roteador = APIRouter(
    prefix="/saude",
    tags=["Saude Check"]
)

@roteador.get("")
def saude():
    return {
        "status": "UP",
        "servico": "estudantes-api"
    }

@roteador.get("/db")
def saude_db(db: Session = Depends(get_banco)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "UP",
            "banco de dados": "conectado"
        }
    except Exception as erro:
        return {
            "status": "DOWN",
            "banco de dados": "desconectado",
            "ERRO": str(erro)
        }