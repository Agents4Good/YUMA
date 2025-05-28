from utils.genia.log_functions import write_log
from wcwidth import wcswidth


WIDTH = 70


def print_conversation_header(num_conversation):
    """Realiza o print do cabeçalho da conversa com o número do turno."""
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
    """Realiza o print da resposta de um nó com o ID e o conteúdo."""
    write_log(f"Node Response - {node_id}", content)
    title = f"🤖 {node_id}"

    print(title)
    print("━" * WIDTH)
    print(content)
    print("\n")


def get_pretty_input():
    """Solicita a entrada do usuário de forma formatada."""
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
    """Imprime a arquitetura do sistema multiagente de forma formatada."""
    title_padding = (WIDTH // 4) - 2
    title = f"{' ' * title_padding}📐 ARQUITETURA DO SISTEMA MULTIAGENTE 🔧\n\n"
    nodes = "🧶 ────── NÓS:\n\n"
    for idx, node in enumerate(last_message.nodes, start=1):
        nodes += f"  {idx}. {node.node}\n     └─ {node.description}\n\n"

    interactions = "🔄 ────── INTERAÇÕES:\n\n"
    for idx, interaction in enumerate(last_message.interactions, start=1):
        interactions += f"  {idx}. {interaction.source} ─> {interaction.target}\n     └─ {interaction.description}"
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
    """Imprime uma linha de quebra de forma formatada."""
    padding = (WIDTH // 2) - 3
    print("\n")
    print(f"{' ' * padding}🔸 🔸 🔸")
    print("\n")
