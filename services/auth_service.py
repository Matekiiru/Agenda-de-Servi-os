from fastapi import HTTPException

from core.jwt import MINUTOS_EXPIRACAO_TOKEN_ACESSO, criar_token
from core.seguranca import gerar_hash, verificar_senha
from repositories.barbeiro_repository import BarbeiroRepository


class AuthService:
    def __init__(self, db):
        self.barbeiro_repository = BarbeiroRepository(db)

    def login(self, username: str, password: str):
        barbeiro = self.barbeiro_repository.buscar_por_usuario(username)

        if not barbeiro:
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

        senha_legada = barbeiro.senha == password
        senha_valida = verificar_senha(password, barbeiro.senha)

        if not senha_valida and not senha_legada:
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

        if senha_legada:
            barbeiro.senha = gerar_hash(password)
            self.barbeiro_repository.db.add(barbeiro)
            self.barbeiro_repository.db.commit()

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
            "expires_in_minutes": MINUTOS_EXPIRACAO_TOKEN_ACESSO,
            "barbeiro": {
                "id": barbeiro.id,
                "name": barbeiro.nome,
                "user": barbeiro.usuario,
            },
        }
