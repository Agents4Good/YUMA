from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv(override=True)

model = ChatOpenAI(
    model=os.getenv("MODEL_ID"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
)

structured_model = ChatOpenAI(
    model=os.getenv("MODEL_ID"),
    base_url=os.getenv("BASE_URL_DEEP_INFRA"),
    model_kwargs={"response_format": {"type": "json_object"}},
)