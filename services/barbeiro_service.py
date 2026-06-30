from repositories.barbeiro_repository import BarbeiroRepository


class BarbeiroService:
    def __init__(self, db):
        self.barbeiro_repository = BarbeiroRepository(db)

    def listar_barbeiros(self):
        barbeiros = self.barbeiro_repository.listar_todos()
        return [{"id": barbeiro.id, "nome": barbeiro.nome} for barbeiro in barbeiros]
