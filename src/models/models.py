from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

model = ChatOpenAI(
    model=os.getenv("MODEL_ID"), base_url=os.getenv("BASE_URL_DEEP_INFRA")
)
