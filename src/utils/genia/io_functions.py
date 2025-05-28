from langgraph.graph.state import CompiledStateGraph
import os


HEADERS = {"Content-Type": "application/json", "Authorization": "Bearer "}
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))


def get_generated_files_path(file_name: str) -> str:
    """Retorna o caminho completo para um arquivo na pasta 'generated_files'."""
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)


def get_dotenv_path(file=".env") -> str:
    """Retorna o caminho completo para o arquivo .env na raiz do projeto."""
    return os.path.join(PROJECT_ROOT, file)


def print_graph(graph: CompiledStateGraph, filename="graph_image.png") -> None:
    """Gera e salva uma imagem do sistema em forma de grafo."""
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
