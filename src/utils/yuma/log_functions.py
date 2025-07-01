from langgraph.types import Command
from pathlib import Path
import dataclasses
import threading
import json
import os
import re


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SEMAPHORE = threading.Semaphore(1)


def get_log_path():
    """Cria o caminho para os próximos arquivos de log."""
    logs_path = Path(PROJECT_ROOT) / "generated_files" / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)

    log_regex = re.compile(r"log_(\d+)\.log")
    existing_numbers = []

    for file in logs_path.iterdir():
        if file.is_file() and file.suffix == ".log":
            match = log_regex.match(file.name)
            if match:
                existing_numbers.append(int(match.group(1)))

    next_log_number = max(existing_numbers, default=0) + 1

    log_file = logs_path / f"log_{next_log_number}.log"
    log_raw_file = logs_path / f"log_{next_log_number}_raw.log"

    for f in (log_file, log_raw_file):
        f.touch(exist_ok=True)

    return log_file, log_raw_file


LOG_FILE_PATH, LOG_RAW_FILE_PATH = get_log_path()


def write_log(title, content):
    """Escreve o conteúdo em um arquivo de log com o título especificado."""
    SEMAPHORE.acquire()
    try:
        if isinstance(content, str):
            try:
                parsed_content = json.loads(content)
                content_to_write = json.dumps(parsed_content, indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                content_to_write = content
        else:
            content_to_write = json.dumps(content, indent=4, ensure_ascii=False, default=lambda o: o.__dict__)

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("============= " + title + " =============")
            log_file.write("\n\n" + content_to_write + "\n\n\n\n")

    finally:
        SEMAPHORE.release()


def _to_json_serializable(obj):
    """Recursivamente transforma qualquer objeto em algo que pode ser serializado por JSON."""
    if dataclasses.is_dataclass(obj):
        return {k: _to_json_serializable(v) for k, v in dataclasses.asdict(obj).items()}
    elif isinstance(obj, dict):
        return {str(k): _to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [_to_json_serializable(v) for v in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        return repr(obj)


def write_log_state(title, content: Command):
    """Escreve o conteúdo do retorno do Command em um arquivo de log com o título especificado."""
    SEMAPHORE.acquire()
    try:
        with open(LOG_RAW_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("============= " + title + " =============\n\n")
            serializable_content = _to_json_serializable(content)
            json.dump(serializable_content, log_file, indent=4, ensure_ascii=False)
            log_file.write("\n\n\n\n")
    finally:
        SEMAPHORE.release()
