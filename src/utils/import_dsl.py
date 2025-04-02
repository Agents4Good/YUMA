import requests
import yaml
import dotenv
import webbrowser

"""
    Para que a função funcione corretamente devem existir as seguintes variáveis no .env:
    EMAIL="email_de_login_do_dify"
    SENHA="senha_do_dify"
    Email e senha referentes ao login da plataforma Dify.
"""
dotenv.load_dotenv()

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "
}

def login():
    email = dotenv.get_key(".env", "EMAIL")
    password = dotenv.get_key(".env", "SENHA")
    url_login = dotenv.get_key(".env","DIFY_URL_LOGIN")
    body = {
        "email": email,
        "language":"pt-BR",
        "remember_me": "true",
        "password": password
    }

    response = requests.post(url_login, json=body, headers=HEADERS)
 
    token = response.json().get("data").get("access_token")

    return token

# Trocar o arquivo para o correto(após consertar o diretório de arquivos gerados)
def import_yaml(file="test_mod.yml"):
    token = login()
    url_import = dotenv.get_key(".env", "DIFY_URL_IMPORT")
    url_base = dotenv.get_key(".env", "DIFY_BASE_URL")

    with open(file, "r", encoding="utf-8") as file:
        yaml_content = yaml.dump(yaml.safe_load(file), line_break="\n ", allow_unicode=True)

    body = {
        "mode": "yaml-content",
        "yaml_content": yaml_content
    }

    HEADERS["Authorization"] += token

    response = requests.post(url_import, json=body, headers=HEADERS)


    link = url_base + response.json().get("app_id") + "/workflow"

    webbrowser.open(link)

    return link