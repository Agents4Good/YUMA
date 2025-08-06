from langchain_openai import ChatOpenAI
import dotenv
import os

dotenv.load_dotenv(override=True)

model_sys = ChatOpenAI(
    model=os.getenv("MODEL_ID_CONVERSATION")
)

model_dify = ChatOpenAI(
    model=os.getenv("MODEL_ID_TOOLCALLING")
)

structured_model = ChatOpenAI(
    model=os.getenv("MODEL_ID_CONVERSATION"),
    model_kwargs={"response_format": {"type": "json_object"}},
)