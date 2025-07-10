from langchain_openai import ChatOpenAI
import os


def conversation_model():
    return ChatOpenAI(
        model=os.getenv("MODEL_ID_CONVERSATION"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
    )

def toolcalling_model():
    return ChatOpenAI(
        model=os.getenv("MODEL_ID_TOOLCALLING"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
    )

def structured_model():
    return ChatOpenAI(
        model=os.getenv("MODEL_ID_CONVERSATION"),
        base_url=os.getenv("BASE_URL_DEEP_INFRA"),
        model_kwargs={"response_format": {"type": "json_object"}},
    )