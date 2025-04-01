import yaml
from pathlib import Path
import threading

semaphore = threading.Semaphore(1)

def insert_node_yaml(file: str, node: dict):
    semaphore.acquire()
    file = Path(file)
    with open(file, "r") as infile:
        data = yaml.safe_load(infile)

    data["workflow"]["graph"]["nodes"].append(node)

    with open(file, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    semaphore.release()


def insert_edge_yaml(file: str, edge: dict):
    semaphore.acquire()
    file = Path(file)
    with open(file, "r") as infile:
        data = yaml.safe_load(infile)

    data["workflow"]["graph"]["edges"].append(edge)

    with open(file, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    semaphore.release()