from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_banco
from schemas.barbeiro import BarbeiroResponse
from services.barbeiro_service import BarbeiroService

roteador = APIRouter(
    prefix="/barbeiros",
    tags=["Barbeiros"],
)


@roteador.get("", response_model=list[BarbeiroResponse])
def listar_barbeiros(db: Session = Depends(get_banco)):
    service = BarbeiroService(db)
    return service.listar_barbeiros()
