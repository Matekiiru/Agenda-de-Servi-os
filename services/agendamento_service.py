from datetime import date, datetime, time, timedelta

from fastapi import HTTPException

from models.agendamento import Agendamento
from repositories.agendamento_repository import AgendamentoRepository
from repositories.barbeiro_repository import BarbeiroRepository
from repositories.cliente_repository import ClienteRepository
from repositories.servico_repository import ServicoRepository
from schemas.agendamento import AgendamentoCreate, AgendamentoResponse


class AgendamentoService:
    def __init__(self, db):
        self.agendamento_repository = AgendamentoRepository(db)
        self.barbeiro_repository = BarbeiroRepository(db)
        self.cliente_repository = ClienteRepository(db)
        self.servico_repository = ServicoRepository(db)

    def listar_agendamentos(self, barbeiro_id: int | None, data: date | None):
        agendamentos = self.agendamento_repository.listar(barbeiro_id=barbeiro_id, data=data)

        return [
            AgendamentoResponse(
                id=agendamento.id,
                barbeiro_id=agendamento.barbeiro_id,
                barbeiro=agendamento.barbeiro.nome,
                cliente=agendamento.cliente.nome,
                servico=agendamento.servico.nome,
                duracao=agendamento.servico.duracao_minutos,
                data=agendamento.data,
                horario_inicio=agendamento.horario_inicio,
                status=agendamento.status,
            )
            for agendamento in agendamentos
        ]

    def criar_agendamento(self, payload: AgendamentoCreate):
        barbeiro = self.barbeiro_repository.buscar_por_id(payload.barbeiro_id)
        servico = self.servico_repository.buscar_por_id(payload.servico_id)

        if not barbeiro:
            raise HTTPException(status_code=404, detail="Barbeiro não encontrado")

        if not servico:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

        data_agendamento = payload.data
        horario_inicio_obj = payload.horario_inicio

        cliente = self.cliente_repository.buscar_por_nome(payload.cliente_nome.strip())
        if not cliente:
            cliente = self.cliente_repository.criar(payload.cliente_nome.strip())

        inicio = datetime.combine(data_agendamento, horario_inicio_obj)
        fim = inicio + timedelta(minutes=servico.duracao_minutos)

        conflitos = self.agendamento_repository.buscar_conflitos(payload.barbeiro_id, data_agendamento)

        for agendamento in conflitos:
            inicio_existente = datetime.combine(agendamento.data, agendamento.horario_inicio)
            fim_existente = inicio_existente + timedelta(minutes=agendamento.servico.duracao_minutos)

            if inicio < fim_existente and fim > inicio_existente:
                raise HTTPException(status_code=409, detail="Horário indisponível")

        agendamento = Agendamento(
            barbeiro_id=payload.barbeiro_id,
            cliente_id=cliente.id,
            servico_id=payload.servico_id,
            data=data_agendamento,
            horario_inicio=horario_inicio_obj,
            status="pendente",
        )

        agendamento_criado = self.agendamento_repository.criar(agendamento)

        return AgendamentoResponse(
            id=agendamento_criado.id,
            barbeiro_id=agendamento_criado.barbeiro_id,
            barbeiro=barbeiro.nome,
            cliente=cliente.nome,
            servico=servico.nome,
            duracao=servico.duracao_minutos,
            data=agendamento_criado.data,
            horario_inicio=agendamento_criado.horario_inicio,
            status=agendamento_criado.status,
        )

    def cancelar_agendamento(self, agendamento_id: int):
        agendamento = self.agendamento_repository.buscar_por_id(agendamento_id)

        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

        self.agendamento_repository.cancelar(agendamento)
        return {"mensagem": "Agendamento cancelado"}
