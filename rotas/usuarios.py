from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_banco
from services.auth_service import AuthService

roteador = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
)


@roteador.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_banco),
):
    service = AuthService(db)
    return service.login(form_data.username, form_data.password)
