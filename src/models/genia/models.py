from langchain_openai import ChatOpenAI
import os


architecture_model = ChatOpenAI(
                        model=os.getenv("MODEL_ID"),
                        base_url=os.getenv("BASE_URL_DEEP_INFRA"),
                        model_kwargs={"response_format": {"type": "json_object"}}
                        )
