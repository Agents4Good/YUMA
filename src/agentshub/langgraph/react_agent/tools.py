from langchain_core.tools import tool
from pathlib import Path
from utils.yuma import get_generated_files_path


GENERATED_PATH = Path(get_generated_files_path("user_system"))
GENERATED_PATH.mkdir(parents=True, exist_ok=True)

AGENT_DIR = GENERATED_PATH / "agent"
AGENT_DIR.mkdir(parents=True, exist_ok=True)

AGENT_PATH = AGENT_DIR / "agent.py"
TOOLS_PATH = AGENT_DIR / "tools.py"
DOCUMENTATION_PATH = AGENT_DIR / "documentation.md"
MAIN_PATH = GENERATED_PATH / "main.py"

AGENT_CACHE = {
    "name": "",
    "prompt": ""
}

AGENT_TEMPLATE = '''
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from .tools import {tools}
from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatOpenAI(model="gpt-4o")

tools = [{tools}]
model_with_tools = model.bind_tools(tools)

def {agent_name}(state: MessagesState) -> MessagesState:
    prompt = SystemMessage(content="""{prompt}""")

    messages = state['messages'] + [prompt]
    response = model_with_tools.invoke(messages)
    
    return {{'messages' : [response]}}
'''
@tool
def criar_agente_react(prompt: str, agent_name: str, tools_name: list) -> str:
    """
    Cria e salva um agente ReAct em um arquivo .py

    Args:
      prompt (str): Prompt do agente ReAct que será gerado
      agent_name (str): Nome do agente que será criado
      tools_name (str): Lista de nomes das tools que serão usadas pelo agente gerado

    Returns:
      str: String com o nome do agente e as tools que ele utiliza
    """
    tools_list = ", ".join(tools_name)
    agent = AGENT_TEMPLATE.format(
      prompt=prompt, agent_name=agent_name, tools=tools_list)
    print("executou a tool")
  
    AGENT_CACHE["name"] = agent_name
    AGENT_CACHE["prompt"] = prompt

    with open(AGENT_PATH, "w", encoding="utf-8") as f:
        f.write(agent)
        
    _criar_main(agent_name)
    return f"O agente {agent_name} foi criado com as seguintes ferramentas {tools_list}"


TOOL_TEMPLATE = '''
@tool
def {tool_name}({params}):
    """
    {description}
  
    Args:
    {params_doc}
  
    Returns:
    {return_doc}
    """
    {code}
'''
@tool
def criar_tool(tool_name: str, params: list, description: str, params_doc: str, return_doc: str, code: str) -> str:
    """
    Gera uma tool do LangChain com base nas informações fornecidas.

    Args:
        tool_name (str): Nome da função/tool.
        params (list): Lista de parâmetros no formato "nome: tipo".
        description (str): Descrição geral da função.
        params_doc (str): Documentação dos parâmetros (um por linha).
        return_doc (str): Documentação da saída/retorno.
        code (str): CORPO da função (código Python).

    Returns:
        str: Confirmação que a tool foi criada
    """
    tool_code = TOOL_TEMPLATE.format(
      tool_name=tool_name,
      params=", ".join(params),
      description=description,
      params_doc=params_doc,
      return_doc=return_doc,
      code=code
    )
  
    TOOLS_PATH.touch(exist_ok=True)

    with open(TOOLS_PATH, "r+", encoding="utf-8") as f:
        existing_content = f.read()
        f.seek(0, 2)

        if existing_content.strip():
            f.write("\n\n" + tool_code)
        else:
            f.write("from langchain_core.tools import tool\n\n")
            f.write(tool_code)

    return f"A tool '{tool_name}' foi adicionada ao arquivo tools.py com sucesso."


DOCUMENTATION_TEMPLATE = """
# {agent_name}

Tipo: Agente ReAct
Role: {role}

### Exemplos de uso
```
{example}
```

### System Prompt
```
{prompt}
```

### Modo de Ativação

O agente deve ser ativado quando:
{activation_mode}

### Modelo de Linguagem

É necessário que o modelo seja capaz de utilizar ferramentas. 

Modelo utilizado em testes:
- gpt-4o

### Tools

{tools_description}

### Testes e Validação

Foi utilizado para a realização dos testes a biblioteca Deepeval do Python
"""
@tool
def criar_documentacao(role: str, example: str, activation_mode: str, tools_description: list) -> str:
    """
    Gera uma documentação estruturada para um agente ReAct

    Args:
        role (str): Descrição do papel/função do agente.
        example (str): Exemplo de uso do agente
        activation_mode (str): Descrição das condições ou modo de ativação do agente (ex. entrada do usuário).
        tools_description (str): Lista contendo descrições das ferramentas usadas pelo agente.

    Returns:
        str: Confirmação que a documentação foi criada
    """
    agent_name = AGENT_CACHE["name"]
    
    documentation_code = DOCUMENTATION_TEMPLATE.format(
        agent_name=agent_name,
        role=role,
        example=example,
        prompt=AGENT_CACHE["prompt"],
        activation_mode=activation_mode,
        tools_description="\n\n".join(tools_description)
    )
    with open(DOCUMENTATION_PATH, "w", encoding="utf-8") as f:
        f.write(documentation_code)
    
    return f"A documentação do agente {agent_name} foi criada com sucesso."
    
MAIN_TEMPLATE = """
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from .agent.agent import {agent_name}, tools
from dotenv import load_dotenv

load_dotenv(override=True)


def edge_condicional(state: MessagesState) -> str:
    if state["messages"][-1].tool_calls:
        return "tools"

    return END


def build_graph():
    tool_node = ToolNode(tools)

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", {agent_name})
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", edge_condicional, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()


def execute_graph(input: str) -> str:
    initial_state = MessagesState(messages=[HumanMessage(input)])
    graph = build_graph()

    result = graph.invoke(initial_state)
    return result["messages"]


if __name__ == "__main__":
    messages = execute_graph(input("$ "))
    for message in messages:
        print(message)
        if isinstance(message, AIMessage) and message.tool_calls:
            print("Tool Call:", message.tool_calls)
"""
def _criar_main(agent_name: str) -> None:
    main_code = MAIN_TEMPLATE.format(agent_name=agent_name)
    with open(MAIN_PATH, "w", encoding="utf-8") as f:
        f.write(main_code)


