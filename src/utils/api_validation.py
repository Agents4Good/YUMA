from openai import AuthenticationError
import openai
import os


def validate_key(key: str):
    try:
        client = openai.OpenAI(
            api_key=key, base_url=os.getenv("BASE_URL_DEEP_INFRA")
        )
        client.models.list()
    
    except AuthenticationError:
        return False
    else:
        return True
