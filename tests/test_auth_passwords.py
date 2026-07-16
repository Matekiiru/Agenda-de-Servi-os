import unittest

from core.seguranca import gerar_hash, verificar_senha


class PasswordHashingTests(unittest.TestCase):
    def test_verificar_senha_aceita_senha_texto_puro_legacy(self):
        senha_legacy = "123456"

        self.assertTrue(verificar_senha(senha_legacy, senha_legacy))

    def test_verificar_senha_aceita_hash_bcrypt(self):
        senha = "123456"
        hash_senha = gerar_hash(senha)

        self.assertTrue(verificar_senha(senha, hash_senha))


if __name__ == "__main__":
    unittest.main()
