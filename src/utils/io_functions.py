from langgraph.graph.state import CompiledStateGraph
import os
import requests
import yaml
import dotenv
import webbrowser

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "
}

def get_path(file_name: str) -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)

def get_dotenv_path(file=".env") -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    return os.path.join(PROJECT_ROOT, file)

def print_graph(graph: CompiledStateGraph, filename="graph_image.png") -> None:
    """
    Renderiza um grafo e seus subgrafos recursivamente.
    """
    if not isinstance(graph, CompiledStateGraph):
        raise TypeError("O parâmetro 'graph' deve ser uma instância de CompiledStateGraph")

    file_path = get_path(filename)
    graph_obj = graph.get_graph()
    graph_image = graph_obj.draw_mermaid_png()

    with open(file_path, "wb") as f:
        f.write(graph_image)

    for node_id, node in graph_obj.nodes.items():
        if isinstance(node.data, CompiledStateGraph):
            subgraph_filename = f"subgraph_{node_id}.png"
            print_graph(node.data, filename=subgraph_filename)

dotenv_path = get_dotenv_path()

def login():
    """
    Para que a função funcione corretamente devem existir as seguintes variáveis no .env:
    EMAIL="email_de_login_do_dify"
    SENHA="senha_do_dify"
    Email e senha referentes ao login da plataforma Dify.
    """
    email = dotenv.get_key(dotenv_path, "EMAIL")
    if email is None:
        raise ValueError("Variável de ambiente EMAIL não encontrada no arquivo .env.")
    password = dotenv.get_key(dotenv_path, "SENHA")
    if password is None:
        raise ValueError("Variável de ambiente SENHA não encontrada no arquivo .env.")
    url_login = dotenv.get_key(dotenv_path,"DIFY_URL_LOGIN")
    body = {
        "email": email,
        "language":"pt-BR",
        "remember_me": "true",
        "password": password
    }

    try:
        response = requests.post(url_login, json=body, headers=HEADERS)
        response.raise_for_status()
        token = response.json().get("data").get("access_token")
        return token
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to login: {e}")

# Trocar o arquivo para o correto(após consertar o diretório de arquivos gerados)
def import_yaml(file="dify.yaml"):
    token = login()
    file_path = get_path(file)
    url_import = dotenv.get_key(dotenv_path, "DIFY_URL_IMPORT")
    url_base = dotenv.get_key(dotenv_path, "DIFY_BASE_URL")

    with open(file_path, "r", encoding="utf-8") as file:
        yaml_content = yaml.dump(yaml.safe_load(file), line_break="\n ", allow_unicode=True)

    body = {
        "mode": "yaml-content",
        "yaml_content": yaml_content
    }

    HEADERS["Authorization"] += token

    try:
        response = requests.post(url_import, json=body, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to import YAML: {e}")


    link = url_base + response.json().get("app_id") + "/workflow"

    webbrowser.open(link)

    return link