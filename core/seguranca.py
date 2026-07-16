from passlib.context import CryptContext

contexto_senha = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def gerar_hash(senha: str):
    return contexto_senha.hash(senha)


def verificar_senha(senha: str, hash_senha: str):
    if not senha or not hash_senha:
        return False

    if hash_senha == senha:
        return True

    try:
        return contexto_senha.verify(senha, hash_senha)
    except Exception:
        return False


#print(gerar_hash("123456"))
 