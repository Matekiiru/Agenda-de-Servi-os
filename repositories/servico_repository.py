from sqlalchemy.orm import Session

from models.servico import Servico


class ServicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, servico_id: int):
        return self.db.query(Servico).filter(Servico.id == servico_id).first()
