from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage
from models import structured_model
from utils.yuma import write_log, write_log_state
from .prompt import YAML_ANALYZER
from schema.dify import DifyState
from utils import read_file_after_keyword
from utils.yuma.io_functions import get_generated_files_path
from .structured_output import YamlAnalyzerOutput
from utils import extract_json
from utils.dify import build_few_shot
from .examples import EXAMPLES

def _human_message(yaml: str, architecture: str):
    return HumanMessage(content="A partir dos exemplos citados, realize a análise para a seguinte situação: Aqui está o YAML:\n" + yaml +
                        "\n\nAqui está a ARQUITETURA ORIGINAL:\n" + architecture)

def yaml_analyzer(state: DifyState) -> Command:
    yaml_path = get_generated_files_path("dify.yaml")
    yaml = read_file_after_keyword(yaml_path, "graph")
    architecture = state["architecture_output"].model_dump_json()
    
    instruction = _human_message(yaml, architecture)
    
    messages = build_few_shot(YAML_ANALYZER, EXAMPLES, instruction)
    
    response = structured_model().invoke(messages)
    response = extract_json(response.content, YamlAnalyzerOutput)
    if "Nenhum nó ou aresta" in response.message:
        response.agents = []
        
    write_log("yaml_analyzer response", response.model_dump_json())
    
    _return = Command(goto="__end__")
    if response.agents:
        response_message = HumanMessage(content="Construa os componentes faltantes QUE VOCÊ É ESPECIALIZADO: " + response.message)
        _return = Command(update={"messages": [response_message], "human_message": response_message}, goto=response.agents)

    write_log_state("yaml_analyzer - return", _return)
    
    return _return