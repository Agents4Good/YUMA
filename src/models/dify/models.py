from models import model
from tools.dify import (
    create_start_node,
    create_llm_node,
    create_answer_node,
    # create_start_with_logic_node,
    # create_end_with_logic_node,
    create_contains_logic_node,
    # create_not_contains_logic_node,
    # create_is_equals_logic_node,
    # create_not_equals_logic_node,
    # create_is_empty_logic_node,
    # create_not_empty_logic_node,
    create_http_node,
    create_edges,
    create_logic_edges
)


node_creator_dify_model = model.bind_tools(
    [
        create_start_node,
        create_llm_node,
        create_answer_node,
        # create_start_with_logic_node,
        # create_end_with_logic_node,
        create_contains_logic_node,
        # create_not_contains_logic_node,
        # create_is_equals_logic_node,
        # create_not_equals_logic_node,
        # create_is_empty_logic_node,
        # create_not_empty_logic_node,
        create_http_node
     ]
)


edge_creator_dify_model = model.bind_tools(
    [
        create_edges,
        create_logic_edges
    ]
)
