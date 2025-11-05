def create_logic_node(
    title: str,
    node_id: str,
    value: str,
    comparison_operator: str,
    context_variable: str,
) -> dict:
    logic_node = {
        "id": node_id,
        "type": "custom",
        "data": {
            "cases": [
                {
                    "case_id": "true",
                    "conditions": [
                        {
                            "comparison_operator": comparison_operator,
                            "value": value,
                            "varType": "string",
                            "variable_selector": (
                                [
                                    context_variable.split(".")[0],
                                    context_variable.split(".")[1],
                                ]
                                if context_variable
                                else []
                            ),
                        }
                    ],
                    "logical_operator": "and",
                }
            ],
            "desc": "",
            "title": title,
            "type": "if-else",
        },
    }
    return logic_node