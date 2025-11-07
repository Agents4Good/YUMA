import questionary
import json
from wcwidth import wcswidth
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich.align import Align
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from utils.yuma.log_functions import write_log


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
    text = (
        "[bold cyan]✻ Obrigado por usar o Yuma CLI![/bold cyan]\n\n"
        f"⏳ Tempo de Execução: {runtime:.2f}s.\n"
        f"🧮 Tokens gastos (YUMA): {total_tokens_yuma:.2f}\n"
        f"💵 Custo total (YUMA): ${total_cost_yuma:.2f}"
    )

    console.print(Panel.fit(text, border_style="cyan"))


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
    """Imprime a arquitetura do sistema multiagente de forma formatada com Rich."""
    last_message = json.loads(last_message)
    
    # CABEÇALHO
    header_panel = Panel.fit(
        "[bold cyan]📐 ARQUITETURA DO SISTEMA MULTIAGENTE 🔧[/bold cyan]",
        border_style="cyan",
        padding=(1, 4),
    )

    console.print(Align.center(header_panel))

    # NÓS
    console.print(Rule("[bold yellow]🧶 NÓS[/bold yellow]", style="yellow"))
    for idx, node in enumerate(last_message["nodes"], start=1):
        console.print(
            f"[bold]{idx}.[/bold] [green]{node['node']}[/green]\n"
            f"   [dim]└─ {node['description']}[/dim]\n"
        )

    # INTERAÇÕES
    console.print(
        Rule("[bold magenta]🔄 INTERAÇÕES[/bold magenta]", style="magenta"))
    for idx, interaction in enumerate(last_message["interactions"], start=1):
        console.print(
            f"[bold]{idx}.[/bold] [cyan]{interaction['source']}[/cyan] → [cyan]{interaction['target']}[/cyan]\n"
            f"   [dim]└─ {interaction['description']}[/dim]\n"
        )

    # PAINEL FINAL
    instruction_text = Text()
    instruction_text.append(
        "MODIFIQUE A ARQUITETURA OU INSIRA:\n", style="bold white")
    instruction_text.append("'Prossiga para a geração'\n", style="bold green")
    instruction_text.append(
        "PARA INICIAR A GERAÇÃO DE CÓDIGO", style="bold white")

    console.print(
        Panel(
            Align.center(instruction_text),
            border_style="bright_black",
            padding=(1, 4),
        )
    )

    # SEPARADOR
    console.print(Align.center("[dim]🔸 🔸 🔸[/dim]\n"))