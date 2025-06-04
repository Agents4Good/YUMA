from langchain_core.messages import HumanMessage


def _human_message(node_type: str, architecture: str):
    return HumanMessage(
        f"A partir dos exemplos, construa os nós de {node_type} indicados nessa arquitetura:\n {architecture}")
