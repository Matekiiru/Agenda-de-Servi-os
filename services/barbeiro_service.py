from repositories.barbeiro_repository import BarbeiroRepository
from schemas.barbeiro import BarbeiroResponse


class BarbeiroService:
    def __init__(self, db):
        self.barbeiro_repository = BarbeiroRepository(db)

    def listar_barbeiros(self):
        barbeiros = self.barbeiro_repository.listar_todos()
        return [
            BarbeiroResponse(id=barbeiro.id, nome=barbeiro.nome, usuario=barbeiro.usuario)
            for barbeiro in barbeiros
        ]
