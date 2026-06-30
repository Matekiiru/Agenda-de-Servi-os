from fastapi import HTTPException

from core.jwt import criar_token
from repositories.barbeiro_repository import BarbeiroRepository


class AuthService:
    def __init__(self, db):
        self.barbeiro_repository = BarbeiroRepository(db)

    def login(self, username: str, password: str):
        barbeiro = self.barbeiro_repository.buscar_por_usuario(username)

        if not barbeiro or password != barbeiro.senha:
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
