import bcrypt
from cryptography.fernet import Fernet
import base64

def gerar_chave():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def abrir_chave():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        return gerar_chave()

key = abrir_chave()
f = Fernet(key)

def hash_senha(senha: str) -> str:
    senha_hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    return senha_hash_bytes.decode('utf-8')

def verificar_senha(senha_digitada: str, senha_salva_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_salva_hash.encode('utf-8'))
    except ValueError:
        return False
    except Exception as e:
        print(f"Erro inesperado ao verificar senha: {e}")
        return False

def criptografar_dados(dados):
    if not isinstance(dados, bytes):
        dado_bytes = dados.encode('utf-8')
    else:
        dado_bytes = dados
    return f.encrypt(dado_bytes).decode('utf-8')

def descriptografar_dados(dado_criptografado):
    if not isinstance(dado_criptografado, bytes):
        dado_bytes = dado_criptografado.encode('utf-8')
    else:
        dado_bytes = dado_criptografado
    return f.decrypt(dado_bytes).decode('utf-8')

