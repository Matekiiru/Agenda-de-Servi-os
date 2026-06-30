from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_banco
from services.barbeiro_service import BarbeiroService

roteador = APIRouter(
    prefix="/barbeiros",
    tags=["Barbeiros"],
)


@roteador.get("")
def listar_barbeiros(db: Session = Depends(get_banco)):
    service = BarbeiroService(db)
    return service.listar_barbeiros()
