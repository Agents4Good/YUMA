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


def yaml_analyzer(state: DifyState) -> Command:
    system_prompt = YAML_ANALYZER
    yaml_path = get_generated_files_path("dify.yaml")
    yaml = read_file_after_keyword(yaml_path, "graph")
    
    instruction = HumanMessage(content="Aqui está o YAML:\n" + yaml + 
                               "\n\nAqui está a ARQUITETURA ORIGINAL:\n" + state["architecture_output"].model_dump_json())
    
    messages = [SystemMessage(system_prompt), instruction]
    
    response = structured_model.invoke(messages)
    response = extract_json(response.content, YamlAnalyzerOutput)
    content_response = response.model_dump_json()
    
    write_log("yaml_analyzer response", content_response)
    _return = Command(update={"messages": [content_response]})
    write_log_state("yaml_analyzer - return", _return)
    
    return _return