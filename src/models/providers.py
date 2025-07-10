class Provider:
    def __init__(self, provider_name, provider_url, conversation_models, toolcalling_models):
        self.provider_name = provider_name
        self.provider_url = provider_url
        self.conversation_models = conversation_models
        self.toolcalling_models = toolcalling_models
    
    def to_dict(self):
        return {
        "provider_name": self.provider_name,
        "provider_url": self.provider_url,
        "conversation_models": self.conversation_models,
        "toolcalling_models": self.toolcalling_models
        }
    
    
PROVIDERS = [
    Provider(
        "Deep Infra", "https://api.deepinfra.com/v1/openai",
        conversation_models={
            "Llama 3.3 70B Instruct": "meta-llama/Llama-3.3-70B-Instruct"
        },
        toolcalling_models={
            "Qwen 2.5 72B Instruct": "Qwen/Qwen2.5-72B-Instruct"
        }
    ),
    Provider(
        "ProviderB", "https://providerB.com",
        conversation_models={"bert": "id_201", "roberta": "id_202"},
        toolcalling_models={"tools-bert": "id_203", "tools-roberta": "id_204"}
    )
]
