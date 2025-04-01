import requests
import yaml
import dotenv
import webbrowser

"""
    Para que a função funcione corretamente devem existir as seguintes variáveis no .env:
    EMAIL="seu_email_aqui"
    SENHA="sua_senha_aqui"
    Email e senha referentes ao login da plataforma Dify.
"""
dotenv.load_dotenv()

URL_IMPORT = "http://localhost/console/api/apps/imports"
URL_lOGIN = "http://localhost/console/api/login"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "
}
BASE_URL = "http://localhost/app/"


def login():
    email = dotenv.get_key(".env", "EMAIL")
    password = dotenv.get_key(".env", "SENHA")
    body = {
        "email": email,
        "language":"pt-BR",
        "remember_me": "true",
        "password": password
    }

    response = requests.post(URL_lOGIN, json=body, headers=HEADERS)
 
    token = response.json().get("data").get("access_token")

    return token

# Trocar o arquivo para o correto(após consertar o diretório de arquivos gerados)
def import_yaml():
    token = login()

    file = "test_mod.yml"

    with open(file, "r", encoding="utf-8") as file:
        yaml_content = yaml.dump(yaml.safe_load(file), line_break="\n ", allow_unicode=True)

    body = {
        "mode": "yaml-content",
        "yaml_content": yaml_content
    }

    HEADERS["Authorization"] += token

    response = requests.post(URL_IMPORT, json=body, headers=HEADERS
                             )
    link = BASE_URL + response.json().get("app_id") + "/workflow"

    webbrowser.open(link)

    return link