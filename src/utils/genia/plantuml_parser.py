import json
from utils.genia.io_functions import get_generated_files_path
from plantuml import PlantUML
from utils.genia import write_log

def json_to_plantuml(data: str) -> str:
    """
    Converte um JSON de nodes e interações para um diagrama de sequência em PlantUML.
    """
    data = json.loads(data)

    plantuml_code = """
    @startuml

    ' Definição dos nodes
    """

    nodes = {node["node"] for node in data["nodes"]}
    for node in nodes:
        plantuml_code += f"participant {node}\n"

    plantuml_code += "\n' Definição das interações\n"

    for interaction in data["interactions"]:
        source = interaction["source"]
        target = interaction["target"]
        description = interaction["description"]
        plantuml_code += f"{source} -> {target}: {description}\n"

    plantuml_code += "@enduml"

    return plantuml_code


def generate_diagram(plantuml_code, max_retries: int = 3):
    """Salva o código PlantUML em um arquivo e gera o diagrama"""
    puml_file = get_generated_files_path("sequence_diagram.puml")

    with open(puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)

    plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")

    for attempt in range(max_retries):
        try:
            plantuml_server.processes_file(puml_file)
            return
        except Exception:
            if attempt == max_retries:
                write_log("PlantUML", "Falha ao gerar diagrama após várias tentativas.")    
