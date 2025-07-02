from langchain_openai import ChatOpenAI
import os

CONVERSATION_MODELS = {
    "Llama 3.3 70B Instruct" : "meta-llama/Llama-3.3-70B-Instruct"
}

TOOLCALLING_MODELS = {
    "Qwen 2.5 72B Instruct" : "Qwen/Qwen2.5-72B-Instruct"
}

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