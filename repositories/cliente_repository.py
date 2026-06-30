from sqlalchemy.orm import Session

from models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_nome(self, nome: str):
        return self.db.query(Cliente).filter(Cliente.nome.ilike(nome)).first()

    def criar(self, nome: str):
        cliente = Cliente(nome=nome)
        self.db.add(cliente)
        self.db.flush()
        return cliente
