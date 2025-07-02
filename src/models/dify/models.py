from models import toolcalling_model
from tools.dify import (
    create_start_node,
    create_llm_node,
    create_answer_node,
    create_start_with_logic_node,
    create_end_with_logic_node,
    create_contains_logic_node,
    create_not_contains_logic_node,
    create_is_equals_logic_node,
    create_not_equals_logic_node,
    create_is_empty_logic_node,
    create_not_empty_logic_node,
    create_http_node,
    create_agent_node,
    create_edges,
    create_logic_edges,
    create_extractor_document_node,
)

def start_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_start_node]
)

def llm_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_llm_node]
)

def answer_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_answer_node]
)

def logic_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_contains_logic_node,
     create_not_contains_logic_node,
     create_start_with_logic_node,
     create_end_with_logic_node,
     create_is_equals_logic_node,
     create_not_equals_logic_node,
     create_is_empty_logic_node,
     create_not_empty_logic_node,
     ]
)

def http_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_http_node]
)

def extractor_document_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_extractor_document_node]
)

def edge_creator_dify_model():
    return toolcalling_model().bind_tools(
    [create_edges,
     create_logic_edges]
)

def agent_node_creator_model():
    return toolcalling_model().bind_tools(
    [create_agent_node]
)
