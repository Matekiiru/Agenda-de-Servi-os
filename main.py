from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base
from core.database import motor

from rotas.saude import roteador as saude_roteador
from rotas.usuarios import roteador as usuarios_roteador

Base.metadata.create_all(bind=motor)


app = FastAPI(
    title="Mini API estudantes",
    description="Primeira API do curso de programador WEB",
    version="1.0.0"
)

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(saude_roteador)
app.include_router(usuarios_roteador)

@app.get("/")
def root():
    return {
        "application": "MiniAPI",
        "version": "1.0.0",
        "saude": "/saude",
        "saude_banco": "/saude/db"
    }