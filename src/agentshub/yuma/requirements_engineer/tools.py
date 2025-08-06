from langchain_core.tools import tool


@tool()
def handoff_to_team(
    report : str,
    team_name : str
) -> str:
    """
    Tool para escolher qual time ficará responsável pela construção do sistema.
        
    Args:  
        report (str): Documentação com os requisitos do sistema.
        team_name (str): Nome do time responsãvel pela construção do sistema.

    Returns:
        str: String com o time responsável e a documentação.
    """
    return f"Time responsável: {team_name}\n\nDocumentação do sistema: {report}"
