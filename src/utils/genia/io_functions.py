from langgraph.graph.state import CompiledStateGraph
from pathlib import Path
import threading
import json
import os

from wcwidth import wcswidth

HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer "}
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SEMAPHORE = threading.Semaphore(1)


def get_generated_files_path(file_name: str) -> str:
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)


def get_log_path():
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    logs_path = os.path.join(dir_path, "logs")
    os.makedirs(logs_path, exist_ok=True)
    logs_count = sum(1 for f in Path(logs_path).iterdir() if f.is_file())
    return os.path.join(logs_path, f"log_{logs_count}.log")


LOG_FILE_PATH = get_log_path()


def get_dotenv_path(file=".env") -> str:
    return os.path.join(PROJECT_ROOT, file)


def print_graph(graph: CompiledStateGraph, filename="graph_image.png") -> None:
    """
    Renderiza um grafo e seus subgrafos recursivamente.
    """
    if not isinstance(graph, CompiledStateGraph):
        raise TypeError(
            "O parâmetro 'graph' deve ser uma instância de CompiledStateGraph"
        )

    file_path = get_generated_files_path(filename)
    graph_obj = graph.get_graph()
    graph_image = graph_obj.draw_mermaid_png()

    with open(file_path, "wb") as f:
        f.write(graph_image)

    for node_id, node in graph_obj.nodes.items():
        if isinstance(node.data, CompiledStateGraph):
            subgraph_filename = f"subgraph_{node_id}.png"
            print_graph(node.data, filename=subgraph_filename)


def write_log(title, content):
    SEMAPHORE.acquire()
    try:
        try:
            parsed_content = json.loads(content)
            content_to_write = json.dumps(parsed_content, indent=4, ensure_ascii=False)
        except json.JSONDecodeError:
            content_to_write = content

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write("============= " + title + " =============")
            log_file.write("\n\n" + content_to_write + "\n\n\n\n")

    finally:
        SEMAPHORE.release()


## Pretty Prints Functions ##

WIDTH = 70


def print_conversation_header(num_conversation):
    title = f"💬 CONVERSATION TURN {num_conversation}"
    content_width = WIDTH - 2

    title_width = wcswidth(title)
    total_padding = content_width - title_width
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    print("╔" + "═" * content_width + "╗")
    print(f"║{' ' * left_padding}{title}{' ' * right_padding}║")
    print("╚" + "═" * content_width + "╝")
    print("\n")


def print_node_header(node_id, content):
    write_log(f"Node Response - {node_id}", content)
    title = f"🤖 {node_id}"

    print(title)
    print("━" * WIDTH)
    print(content)
    print("\n")


def get_pretty_input():
    user_name = "👤 Usuário"
    message = "📝 Digite sua entrada ('q' para sair)"
    print(
        f"{user_name}{' ' * (WIDTH - (wcswidth(message) + wcswidth(user_name)))}{message}"
    )
    print("━" * WIDTH)
    user_input = input().strip()
    write_log("User Input", user_input)
    return user_input


def print_architecture(last_message):
    title_padding = (WIDTH // 4) - 2
    title = f"{' ' * title_padding}📐 ARQUITETURA DO SISTEMA MULTIAGENTE 🔧\n\n"
    nodes = "🧶 ────── NÓS:\n\n"
    for idx, node in enumerate(last_message.nodes, start=1):
        nodes += f"  {idx}. {node.node}\n     └─ {node.description}\n\n"

    interactions = "🔄 ────── INTERAÇÕES:\n\n"
    for idx, interaction in enumerate(last_message.interactions, start=1):
        interactions += f"  {idx}. {interaction.source} ─> {interaction.targets}\n     └─ {interaction.description}"
        if idx < len(last_message.interactions):
            interactions += "\n\n"

    print_node_header("architecture_agent", title + nodes + interactions)

    final_message1 = "MODIFIQUE A ARQUITETURA OU INSIRA:"
    final_message2 = "'Prossiga para a geração'"
    final_message3 = "PARA INICIAR A GERAÇÃO DE CÓDIGO"

    paddings1 = _calcule_padding(final_message1)
    paddings2 = _calcule_padding(final_message2)
    paddings3 = _calcule_padding(final_message3)

    print("┌" + "─" * (WIDTH - 2) + "┐")
    print(f"│{' ' * paddings1[0]}{final_message1}{' ' * paddings1[1]}│")
    print(f"│{' ' * paddings2[0]}{final_message2}{' ' * paddings2[1]}│")
    print(f"│{' ' * paddings3[0]}{final_message3}{' ' * paddings3[1]}│")
    print("└" + "─" * (WIDTH - 2) + "┘")
    print("\n")

    line_padding = (WIDTH // 2) - 3
    print(f"{' ' * line_padding}🔸 🔸 🔸")
    print("\n")


def _calcule_padding(content):
    content_width = WIDTH - 2
    final_message_width = wcswidth(content)
    total_padding = content_width - final_message_width
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return left_padding, right_padding


def print_break_line():
    padding = (WIDTH // 2) - 3
    print("\n")
    print(f"{' ' * padding}🔸 🔸 🔸")
    print("\n")
