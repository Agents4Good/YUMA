from utils.yuma.log_functions import write_log
from wcwidth import wcswidth
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import questionary
import sys
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings


console = Console()

bindings = KeyBindings()

WIDTH = 70


@bindings.add('escape', 'enter')
def _(event):
    """
    Quando Alt+Enter for pressionado,
    insere uma nova linha (caractere '\n') no buffer.
    O 'Enter' sozinho funcionará para submeter.
    """
    event.app.current_buffer.insert_text('\n')


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


def print_node_header(node_id: str, agente_name: str, message: str):
    """Exibe de forma estilizada o cabeçalho do validador de código."""
    msg = f"🤖 {node_id.upper()} - {agente_name}\n\n"
    msg += message
    console.print(Panel(msg, border_style="green", style="bold"))


def welcome_message():
    """Realiza o print da mensagem de boas-vindas."""
    console.print(
        Panel.fit(
            """[bold cyan]✻ Bem-vindo ao Yuma![/bold cyan]\n
Yuma é um sistema para geração, simulação e execução de fluxos multiagentes em plataformas low-code.\n
Arquivos salvos em: [yellow]/generated_files/[/yellow]""",
            border_style="cyan",
        )
    )
    # Caixa de dicas
    console.print(
        Panel(
            """[bold]Dicas para começar:[/bold]\n
[green]✔[/green] Use o Yuma para projetar, simular e executar fluxos de agentes
[green]✔[/green] Seja específico, como se estivesse pedindo a outro engenheiro
[green]✔[/green] Use [bold]/sair[/bold] para encerrar o sistema [bold]YUMA[/bold]""",
            border_style="green",
        )
    )

    # Caixa de sugestão de input
    console.print(
        Panel.fit(
            '[bold yellow]>[/bold yellow] Experimente: "gostaria de criar um agente gerador de plano de aulas"',
            border_style="yellow",
        )
    )


def display_actions_plan():
    """Realiza o print da mensagem de plano de ações."""
    # Mensagem inicial do sistema
    mensagem = """[bold cyan]✻ YUMA: Entendi![/bold cyan].

    📋 [bold]Plano de Execução para criação do seu sistema:[/bold]
    1. 📝 Coleta de Requisitos
    2. 🏗️  Proposta de Arquitetura  
    3. ⚙️  Geração do Fluxo de agentes 
    """

    # Exibir mensagem em uma caixinha azul
    console.print(Panel(mensagem, border_style="blue"))

    # Perguntar ação ao usuário
    acao = questionary.select(
        "O que deseja fazer?",
        choices=[
            "Prosseguir",
            "Cancelar"
        ]
    ).ask()

    # Respostas
    if acao == "Prosseguir":
        console.print("[green]➡ Prosseguindo com a execução...[/green]\n")
        return True
    elif acao == "Cancelar":
        console.print("[red]❌ Operação cancelada pelo usuário.[/red]\n")
        return False
    

def end_message(runtime, total_tokens_yuma, total_cost_yuma):
    """Realiza o print da mensagem de boas-vindas."""
    console.print(
        Panel.fit(
            f"""[bold cyan]✻ Obrigado por usar o Yuma CLI![/bold cyan]\n
⏳ Tempo de Execução: {runtime}s.\n
🪙 Tokens gastos (YUMA): {total_tokens_yuma} \n
💵 Custo total (YUMA): ${total_cost_yuma}\n
            """,
            border_style="cyan",
        )
    )


# def get_pretty_input():
#     """Solicita a entrada do usuário de forma formatada."""
#     user_name = "👤 Usuário"
#     message = "📝 Digite sua entrada ('q' para sair)"
#     print(
#         f"{user_name}{' ' * (WIDTH - (wcswidth(message) + wcswidth(user_name)))}{message}"
#     )
#     print("━" * WIDTH)
#     user_input = input().strip()
#     write_log("User Input", user_input)
#     return user_input


def get_pretty_input():
    message = [
        ('fg: pink bold', '╭─ Entrada Yuma (alt-enter to break-line)\n'),
        ('fg: pink bold', '╰─> ')
    ]

    try:
        user_input = prompt(
            message,
            key_bindings=bindings,
            prompt_continuation='    '
        )
    except EOFError:
        user_input = "/sair"

    if user_input.strip().lower() in {"/sair", "sair", "/exit", "quit"}:
        console.print("[red]Encerrando Yuma CLI...[/red]")
        user_input = None

    print() 
    
    if user_input is not None:
        write_log("User Input", user_input)
    
    return user_input


def print_architecture(last_message):
    """Imprime a arquitetura do sistema multiagente de forma formatada."""
    title_padding = (WIDTH // 4) - 2
    message = f"{' ' * title_padding}📐 ARQUITETURA DO SISTEMA MULTIAGENTE 🔧\n\n"
    message += "🧶 ────── NÓS:\n\n"
    for idx, node in enumerate(last_message.nodes, start=1):
        message += f"  {idx}. {node.node}\n     └─ {node.description}\n\n"

    message += "🔄 ────── INTERAÇÕES:\n\n"
    for idx, interaction in enumerate(last_message.interactions, start=1):
        message += f"  {idx}. {interaction.source} ─> {interaction.target}\n     └─ {interaction.description}"
        if idx < len(last_message.interactions):
            message += "\n\n"


    final_message1 = "MODIFIQUE A ARQUITETURA OU INSIRA:"
    final_message2 = "'Prossiga para a geração'"
    final_message3 = "PARA INICIAR A GERAÇÃO DE CÓDIGO"

    paddings1 = _calcule_padding(final_message1)
    paddings2 = _calcule_padding(final_message2)
    paddings3 = _calcule_padding(final_message3)

    message += "┌" + "─" * (WIDTH - 2) + "┐"
    message += f"│{' ' * paddings1[0]}{final_message1}{' ' * paddings1[1]}│"
    message += f"│{' ' * paddings2[0]}{final_message2}{' ' * paddings2[1]}│"
    message += f"│{' ' * paddings3[0]}{final_message3}{' ' * paddings3[1]}│"
    message += "└" + "─" * (WIDTH - 2) + "┘"
    message += "\n"

    line_padding = (WIDTH // 2) - 3
    message += f"{' ' * line_padding}🔸 🔸 🔸"
    message += "\n"

    return message


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
