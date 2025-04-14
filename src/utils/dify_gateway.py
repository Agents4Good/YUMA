from playwright.sync_api import sync_playwright
import time
import requests
import webbrowser
import os
import dotenv
import yaml

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "
}

def get_dotenv_path(file=".env") -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    return os.path.join(PROJECT_ROOT, file)

dotenv_path = get_dotenv_path()


def get_path(file_name: str) -> str:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    dir_path = os.path.join(PROJECT_ROOT, "generated_files")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, file_name)


def wait_for_token(page, key="console_token", timeout=120000):
    """Espera até o token estar disponível no localStorage ou atinge timeout."""
    print(f"Aguardando o login... (timeout: {timeout}s)")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            token = page.evaluate(f"() => localStorage.getItem('{key}')")
        except Exception as e:
            print(e)
        if token:
            return token
        time.sleep(1)
    raise TimeoutError("Token não foi encontrado no localStorage dentro do tempo limite.")


def get_dify_web_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(dotenv.get_key(dotenv_path, "DIFY_WEB_URL_BASE"))

        token = wait_for_token(page)

        print("✅ TOKEN capturado.")

        browser.close()
        return token


def dify_import_yaml_web(body, url_import, url_base):
    token = get_dify_web_token()
    HEADERS["Authorization"] += token

    try:
        response = requests.post(url_import, json=body, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to import YAML: {e}")

    link = f"{url_base}/app/{response.json().get('app_id')}/workflow"

    webbrowser.open(link)

    return link


def dify_login_local():
    """
    Para que a função funcione corretamente devem existir as seguintes variáveis no .env:
    EMAIL="email_de_login_do_dify"
    SENHA="senha_do_dify"
    Email e senha referentes ao login da plataforma Dify.
    """
    email = dotenv.get_key(dotenv_path, "EMAIL")
    if email is None:
        raise ValueError("Variável de ambiente EMAIL não encontrada no arquivo .env.")
    password = dotenv.get_key(dotenv_path, "SENHA")
    if password is None:
        raise ValueError("Variável de ambiente SENHA não encontrada no arquivo .env.")
    url_login = dotenv.get_key(dotenv_path,"DIFY_URL_LOGIN")
    body = {
        "email": email,
        "language":"pt-BR",
        "remember_me": "true",
        "password": password
    }

    try:
        response = requests.post(url_login, json=body, headers=HEADERS)
        response.raise_for_status()
        token = response.json().get("data").get("access_token")
        return token
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to login: {e}")


def dify_import_yaml_local(body, url_import, url_base):
    token = dify_login_local()
    HEADERS["Authorization"] += token

    try:
        response = requests.post(url_import, json=body, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to import YAML: {e}")


    link = url_base + response.json().get("app_id") + "/workflow"

    webbrowser.open(link)

    return link


def dify_import_yaml(file="dify.yaml", target="web"):
    file_path = get_path(file)
    url_import = dotenv.get_key(dotenv_path, "DIFY_URL_IMPORT") if target == "local" else dotenv.get_key(dotenv_path, "DIFY_WEB_URL_IMPORT")
    url_base = dotenv.get_key(dotenv_path, "DIFY_BASE_URL") if target == "local" else dotenv.get_key(dotenv_path, "DIFY_WEB_URL_BASE")
    
    with open(file_path, "r", encoding="utf-8") as file:
        yaml_content = yaml.dump(yaml.safe_load(file), line_break="\n ", allow_unicode=True)

    body = {
        "mode": "yaml-content",
        "yaml_content": yaml_content
    }
    
    return dify_import_yaml_local(body, url_import, url_base) if target == "local" else dify_import_yaml_web(body, url_import, url_base)
    
   