from sqlalchemy.orm import Session

from models.barbeiro import Barbeiro


class BarbeiroRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_todos(self):
        return self.db.query(Barbeiro).order_by(Barbeiro.nome.asc()).all()

    def buscar_por_id(self, barbeiro_id: int):
        return self.db.query(Barbeiro).filter(Barbeiro.id == barbeiro_id).first()

    def buscar_por_usuario(self, usuario: str):
        return self.db.query(Barbeiro).filter(Barbeiro.usuario == usuario).first()
