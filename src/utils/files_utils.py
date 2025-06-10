from utils.yuma import write_log

def read_file_after_keyword(file_path: str, keyword: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            index = content.find(keyword)
            if index != -1:
                return content[index:]
            else:
                write_log(f"read_file_after_keyword - Palavra-chave não encontrada.")
                return ""
    except FileNotFoundError:
        write_log(f"read_file_after_keyword - Arquivo não encontrado", file_path)
    except Exception as e:
        write_log(f"read_file_after_keyword - Erro ao ler o arquivo", str(e))
