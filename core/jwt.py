from datetime import datetime, timedelta

from jose import jwt

CHAVE_SECRETA = "minha-chave-super-secreta"
ALGORITMO = "HS256"
MINUTOS_EXPIRACAO_TOKEN_ACESSO = 1


# Geração token
def criar_token(dados: dict):
    dados_token = dados.copy()  

    expira = datetime.utcnow() + timedelta(minutes=MINUTOS_EXPIRACAO_TOKEN_ACESSO)

    dados_token.update({"exp": expira})

    return jwt.encode(
        dados_token,
        CHAVE_SECRETA,
        algorithm=ALGORITMO,
    )

# Verificação token