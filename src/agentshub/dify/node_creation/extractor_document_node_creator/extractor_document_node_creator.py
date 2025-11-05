from schema.dify import DifyState
from .prompt import EXTRACTOR_DOCUMENT
from langgraph.types import Command
from agentshub import only_tools_agent
from .examples import EXAMPLES
from utils.dify import build_few_shot
from utils.yuma import write_log_state
from ..human_message import _human_message
from .tools import create_extractor_document_node
from models import model_dify


extractor_document_node_creator_model = model_dify.bind_tools(
    [create_extractor_document_node]
)

def extractor_document_node_creator(state: DifyState) -> Command:
    archictecure = state["architecture_output"].model_dump_json()
    human_message = state.get(
        "human_message", _human_message("EXTRAÇÃO DE DOCUMENTOS", archictecure))
    new_messages = build_few_shot(EXTRACTOR_DOCUMENT, EXAMPLES, human_message)
    
    _return = only_tools_agent(extractor_document_node_creator_model, state["messages"] + new_messages)
    write_log_state("extractor_document_node_creator - return", _return)
    return _return
