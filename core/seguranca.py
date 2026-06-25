from passlib.context import CryptContext

contexto_senha = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    return contexto_senha.hash(senha)

def verificar_senha(senha: str, hash_senha: str):
    return contexto_senha.verify(senha, hash_senha)

#print(gerar_hash("123456"))
 