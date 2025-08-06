from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv(override=True)

model_sys = ChatOpenAI(
    model=os.getenv("MODEL_ID_CONVERSATION"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
)

model_dify = ChatOpenAI(
    model=os.getenv("MODEL_ID_TOOLCALLING"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
)

structured_model = ChatOpenAI(
    model=os.getenv("MODEL_ID_CONVERSATION"),
    base_url=os.getenv("BASE_URL_DEEP_INFRA"),
    #model_kwargs={"response_format": {"type": "json_object"}},
)