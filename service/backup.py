import os
import shutil
from datetime import datetime
import sys

JSON_FILES = ["players.json", "teams.json", "scouts.json"] 

BACKUP_DIR = "backups"

def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_backup_recente = os.path.join(BACKUP_DIR, f"backup_{data}")

    try:
        os.makedirs(local_backup_recente)
        
        for filename in JSON_FILES:
            if os.path.exists(filename):
                shutil.copy(filename, local_backup_recente)
                print(f"Backup de '{filename}' criado em '{local_backup_recente}'")
            else:
                print(f"Aviso: O arquivo '{filename}' não foi encontrado, não foi feito backup.")
    
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return False, f"Erro ao criar backup: {e}"

def restore_backup(nome_pasta_backup):
    local_backup = os.path.join(BACKUP_DIR, nome_pasta_backup)

    if not os.path.exists(local_backup):
        return False, f"Erro: Pasta de backup '{nome_pasta_backup}' não encontrada."

    print(f"Restaurando do backup: {local_backup}. ATENÇÃO: Isso SOBRESCREVERÁ os arquivos atuais.")
    input("Pressione Enter para continuar ou Ctrl+C para cancelar...")

    try:
        for filename in JSON_FILES:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Removido arquivo existente: {filename}")
        for filename in JSON_FILES:
            source_file = os.path.join(local_backup, filename)
            if os.path.exists(source_file):
                shutil.copy(source_file, ".")
                print(f"Restaurado '{filename}' de '{local_backup}'")
        return True, f"Backup restaurado com sucesso de: {local_backup}"

    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False, f"Erro ao restaurar backup: {e}"

def list_backups():
    if not os.path.exists(BACKUP_DIR):
        print(f"O diretório '{BACKUP_DIR}' não existe. Nenhum backup encontrado.")
        return []
    
    backups = sorted([d for d in os.listdir(BACKUP_DIR) if os.path.isdir(os.path.join(BACKUP_DIR, d)) and d.startswith("backup_")], reverse=True)
    
    if not backups:
        print("Nenhum backup encontrado.")
    else:
        print("Backups disponíveis (mais recente primeiro):")
        for i, b in enumerate(backups):
            print(f"  {i+1}. {b}")
    return backups

if __name__ == "__backup__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python service/bakcup.py create               - Cria um novo backup.")
        print("  python service/bakcup.py list                 - Lista os backups disponíveis.")
        print("  python service/bakcup.py restore <nome_backup> - Restaura um backup específico.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create":
        success, message = create_backup()
        print(message)
    elif command == "list":
        list_backups()
    elif command == "restore":
        if len(sys.argv) < 3:
            print("Erro: O comando 'restore' requer o nome da pasta de backup.")
            print("Uso: python service/bakcup.py restore <nome_backup>")
            sys.exit(1)
        backup_name = sys.argv[2]
        success, message = restore_backup(backup_name)
        print(message)
    else:
        print(f"Comando desconhecido: {command}")
        print("Use 'create', 'list' ou 'restore'.")
        sys.exit(1)

#python service/backup.py create
#python service/backup.py list
#python service/backup.py restore