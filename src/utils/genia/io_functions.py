from langgraph.graph.state import CompiledStateGraph
import os

from wcwidth import wcswidth


HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "
}


def get_generated_files_path(file_name: str) -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)


def get_dotenv_path(file=".env") -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    return os.path.join(PROJECT_ROOT, file)


def print_graph(graph: CompiledStateGraph, filename="graph_image.png") -> None:
    """
    Renderiza um grafo e seus subgrafos recursivamente.
    """
    if not isinstance(graph, CompiledStateGraph):
        raise TypeError("O parâmetro 'graph' deve ser uma instância de CompiledStateGraph")

    file_path = get_generated_files_path(filename)
    graph_obj = graph.get_graph()
    graph_image = graph_obj.draw_mermaid_png()

    with open(file_path, "wb") as f:
        f.write(graph_image)

    for node_id, node in graph_obj.nodes.items():
        if isinstance(node.data, CompiledStateGraph):
            subgraph_filename = f"subgraph_{node_id}.png"
            print_graph(node.data, filename=subgraph_filename)


WIDTH = 70  # Largura total da linha

def print_conversation_header(num_conversation):
    title = f"💬 CONVERSATION TURN {num_conversation}"
    content_width = WIDTH - 2  # bordas ║║

    title_width = wcswidth(title)
    total_padding = content_width - title_width
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding

    print("╔" + "═" * content_width + "╗")
    print(f"║{' ' * left_padding}{title}{' ' * right_padding}║")
    print("╚" + "═" * content_width + "╝")
    print("\n")


def print_node_header(node_id, content):
    title = f"🤖 {node_id}"
    
    print(title)
    print("━" * WIDTH)
    print(content)
    print("\n")


def get_human_input():
    print(f"👤 Usuário{' ' * 38}(Digite 'q' para sair)")
    print("━" * WIDTH)
    return input("📝 Digite sua entrada: ")


def print_break_line():
    padding = (WIDTH // 2) - 3
    print("\n")
    print(f"{' ' * padding}🔸 🔸 🔸")
    print("\n")
