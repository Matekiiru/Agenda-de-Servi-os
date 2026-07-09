# Agenda de Serviços - Barbearia

## Sobre o App

Este projeto é uma aplicação de agendamento para barbearia com backend em FastAPI e front-end em HTML/CSS/JavaScript.

A aplicação permite:

- Listar barbeiros disponíveis.
- Criar agendamentos para clientes com barbeiro, serviço, data e horário.
- Cancelar agendamentos existentes.
- Autenticar barbeiros via rota de login.
- Verificar o estado do serviço e da conexão com o banco de dados.

Funcionalidades principais:

- API com rotas organizadas em `rotas/` para saúde, usuários, barbeiros e agendamentos.
- Modelo de dados com SQLAlchemy em `models/`: barbeiro, cliente, serviço e agendamento.
- Repositórios em `repositories/` para acesso ao banco de dados.
- Serviços em `services/` com regras de criação de agendamento, verificação de conflitos e autenticação.
- Front-end estático com páginas HTML em `index.html`, `inicio.html`, `login.html`, `painel.html` e `agenda.html`.

Prints / visualização:
![Pagina Inicial](Prints\Captura de tela 2026-07-08 203600.png)



## Principais rotas da API

- `GET /` - Retorna informações básicas da aplicação.
- `GET /saude` - Verifica se a API está UP.
- `GET /saude/db` - Verifica a conexão com o banco de dados.
- `POST /usuarios/login` - Autentica barbeiro e gera token JWT.
- `GET /barbeiros` - Lista barbeiros cadastrados.
- `GET /agendamentos` - Lista agendamentos, opcionalmente filtrando por `barbeiro_id` e `data`.
- `POST /agendamentos` - Cria um novo agendamento.
- `DELETE /agendamentos/{agendamento_id}` - Cancela um agendamento.

## Como executar o código passo a passo

### 1. Clonar o repositório

```powershell
git clone <URL_DO_REPOSITORIO>
```

### 2. Entrar na pasta do projeto

```powershell
cd "Agenda-de-Servi-os"
```

### 3. Criar o ambiente virtual

```powershell
py -m venv venv
```

### 4. Ativar o ambiente virtual

No PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

No Prompt de Comando (cmd):

```cmd
venv\Scripts\activate.bat
```

### 5. Instalar as bibliotecas necessárias

```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib[bcrypt]
```

### 6. Configurar o banco de dados

O projeto usa PostgreSQL e a configuração está em `core/database.py`:

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/barbearia"
```

Ajuste essa string conforme suas credenciais:

- usuário
- senha
- host
- porta
- nome do banco de dados

Crie o banco de dados `barbearia` no PostgreSQL antes de executar a aplicação.

### 7. Executar a aplicação

```powershell
py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 8. Acessar a API

- Documentação interativa: `http://127.0.0.1:8000/docs`
- Rota raiz: `http://127.0.0.1:8000/`

## Observações

- O token JWT é gerado em `core/jwt.py` com tempo de expiração curto (1 minuto).
- O login de barbeiro depende de um registro existente em tabela `barbeiros`.
- Se quiser usar o front-end estático, abra os arquivos HTML no navegador ou crie um servidor estático simples.

Bom trabalho! Se precisar, posso ajudar a gerar um arquivo `requirements.txt` ou a ajustar a configuração do banco.
