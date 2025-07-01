from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages import HumanMessage
from agentshub.yuma.architect import ArchitectureOutput, Node, Interaction


def _yaml_example():
    return """
    graph:
        edges:
        - id: edge_1
        source: processa_requisicao
        target: pesquisa_noticias
        type: custom
        - id: edge_2
        source: pesquisa_noticias
        target: verifica_relevancia
        type: custom
        nodes:
        - data:
            desc: ''
            title: Processa Requisicao
            type: start
            variables: []
        id: processa_requisicao
        type: custom
        - data:
            context:
            enabled: true
            variable_selector:
            - pesquisa_noticias
            - text
            desc: ''
            model:
            completion_params:
                temperature: 0.5
            mode: chat
            name: claude-3-haiku-20240307
            provider: langgenius/anthropic/anthropic
            prompt_template:
            - role: system
            text: 'Você é um especialista em verificar a relevância de notícias

                Verifique a relevância das notícias encontradas para o tema'
            - role: user
            text: '{{#context#}}'
            title: Verifica Relevância
            type: llm
            variables: []
            vision:
            enabled: false
        id: verifica_relevancia
        type: custom
        - data:
            answer: '{{#verifica_relevancia.text#}}'
            desc: ''
            title: Resposta Final
            type: answer
            variables: []
        id: envia_resposta
        type: custom
        - data:
            agent_parameters:
            instruction:
                type: constant
                value: 'Você é um agente especialista em pesquisa de notícias em tempo
                real. Faça uma pesquisa na web sobre o tema informado pelo usuário e
                retorne as notícias relevantes.

                Utilize obrigatoriamente a ferramenta de busca web disponível para gerar
                todas as respostas.

                As respostas devem ser redigidas exclusivamente em português brasileiro.

                Sempre que possível, inclua referências com links diretos para as fontes
                utilizadas.'
            model:
                type: constant
                value:
                completion_params:
                    temperature: 0.5
                mode: chat
                model: claude-3-haiku-20240307
                model_type: llm
                provider: langgenius/anthropic/anthropic
            query:
                type: constant
                value: '{{#sys.query#}}'
            tools:
                type: constant
                value:
                - enabled: true
                extra:
                    description: A search engine tool built specifically for AI agents
                    (LLMs), delivering real-time, accurate, and factual results at speed.
                parameters:
                    days:
                    auto: 1
                    query:
                    auto: 1
                    search_depth:
                    auto: 1
                    time_range:
                    auto: 1
                    topic:
                    auto: 1
                provider_name: langgenius/tavily/tavily
                schemas:
                - auto_generate: null
                    form: llm
                    human_description:
                    pt_BR: The search query you want to execute with Tavily.
                    label:
                    pt_BR: Query
                    llm_description: The search query.
                    name: query
                    options: []
                    required: true
                    type: string
                - auto_generate: null
                    default: basic
                    form: llm
                    human_description:
                    pt_BR: The depth of the search.
                    label:
                    pt_BR: Search Depth
                    llm_description: The depth of the search. 'basic' for standard search,
                    'advanced' for more comprehensive results.
                    name: search_depth
                    options:
                    - label:
                        pt_BR: Basic
                    value: basic
                    - label:
                        pt_BR: Advanced
                    value: advanced
                    required: false
                    type: select
                - auto_generate: null
                    default: general
                    form: llm
                    human_description:
                    pt_BR: The category of the search.
                    label:
                    pt_BR: Topic
                    llm_description: The category of the search. Options include 'general',
                    'news', or 'finance'.
                    name: topic
                    options:
                    - label:
                        pt_BR: General
                    value: general
                    - label:
                        pt_BR: News
                    value: news
                    - label:
                        pt_BR: Finance
                    value: finance
                    required: false
                    type: select
                - auto_generate: null
                    default: 3
                    form: llm
                    human_description:
                    pt_BR: The number of days back from the current date to include
                        in the search results (only applicable when "topic" is "news").
                    label:
                    pt_BR: Days
                    llm_description: The number of days back from the current date to
                    include in the search results. Only applicable when "topic" is "news".
                    min: 1
                    name: days
                    options: []
                    required: false
                    type: number
                - auto_generate: null
                    default: not_specified
                    form: llm
                    human_description:
                    pt_BR: The time range back from the current date to filter results.
                    label:
                    pt_BR: Time Range
                    llm_description: The time range back from the current date to filter
                    results. Options include 'not_specified', 'day', 'week', 'month',
                    or 'year'.
                    name: time_range
                    options:
                    - label:
                        pt_BR: Not Specified
                    value: not_specified
                    - label:
                        pt_BR: Day
                    value: day
                    - label:
                        pt_BR: Week
                    value: week
                    - label:
                        pt_BR: Month
                    value: month
                    - label:
                        pt_BR: Year
                    value: year
                    required: false
                    type: select
                - auto_generate: null
                    default: 5
                    form: form
                    human_description:
                    pt_BR: The maximum number of search results to return.
                    label:
                    pt_BR: Max Results
                    llm_description: The maximum number of search results to return. Range
                    is 1-20.
                    max: 20
                    min: 1
                    name: max_results
                    options: []
                    required: false
                    type: number
                - auto_generate: null
                    default: 0
                    form: form
                    human_description:
                    pt_BR: Include a list of query-related images in the response.
                    label:
                    pt_BR: Include Images
                    llm_description: When set to true, includes a list of query-related
                    images in the response.
                    name: include_images
                    options: []
                    required: false
                    type: boolean
                - auto_generate: null
                    default: 0
                    form: form
                    human_description:
                    pt_BR: When include_images is True, adds descriptive text for each
                        image.
                    label:
                    pt_BR: Include Image Descriptions
                    llm_description: When include_images is True and this is set to true,
                    adds descriptive text for each image.
                    name: include_image_descriptions
                    options: []
                    required: false
                    type: boolean
                - auto_generate: null
                    default: 0
                    form: form
                    human_description:
                    pt_BR: Include a short answer to the original query in the response.
                    label:
                    pt_BR: Include Answer
                    llm_description: When set to true, includes a short answer to the
                    original query in the response.
                    name: include_answer
                    options: []
                    required: false
                    type: boolean
                - auto_generate: null
                    default: 0
                    form: form
                    human_description:
                    pt_BR: Include the cleaned and parsed HTML content of each search
                        result.
                    label:
                    pt_BR: Include Raw Content
                    llm_description: When set to true, includes the cleaned and parsed
                    HTML content of each search result.
                    name: include_raw_content
                    options: []
                    required: false
                    type: boolean
                - auto_generate: null
                    form: form
                    human_description:
                    pt_BR: A comma-separated list of domains to specifically include
                        in the search results.
                    label:
                    pt_BR: Include Domains
                    llm_description: A comma-separated list of domains to specifically
                    include in the search results.
                    name: include_domains
                    options: []
                    required: false
                    type: string
                - auto_generate: null
                    form: form
                    human_description:
                    pt_BR: A comma-separated list of domains to specifically exclude
                        from the search results.
                    label:
                    pt_BR: Exclude Domains
                    llm_description: A comma-separated list of domains to specifically
                    exclude from the search results.
                    name: exclude_domains
                    options: []
                    required: false
                    type: string
                settings:
                    exclude_domains:
                    value: null
                    include_answer:
                    value: 0
                    include_domains:
                    value: null
                    include_image_descriptions:
                    value: 0
                    include_images:
                    value: 0
                    include_raw_content:
                    value: 0
                    max_results:
                    value: 5
                tool_description: A search engine tool built specifically for AI agents
                    (LLMs), delivering real-time, accurate, and factual results at speed.
                tool_label: Tavily Search
                tool_name: tavily_search
                type: builtin
            agent_strategy_label: FunctionCalling
            agent_strategy_name: function_calling
            agent_strategy_provider_name: langgenius/agent/agent
            desc: ''
            title: Pesquisa de Notícias
            type: agent
        id: pesquisa_noticias
        type: custom
    """

def _architecture_example():
    nodes = [Node(node="processa_requisicao", description="Nó inicial que recebe a requisição do usuário e será mapeado para o Start Node do Dify"),
             Node(node="pesquisa_noticias", description="Nó responsável por pesquisar notícias relevantes com base na requisição do usuário, será mapeado para o Agent Node do Dify"),
             Node(node="verifica_relevancia", description="Nó que verifica a relevância das notícias encontradas para a requisição do usuário, será mapeado para o LLM Node do Dify"),
             Node(node="envia_resposta", description="Nó que envia a resposta final ao usuário com as notícias relevantes, será mapeado para o Answer Node do Dify")]

    interactions = [Interaction(source="processa_requisicao", target="pesquisa_noticias", description="Passagem da requisição para pesquisa de notícias"),
                    Interaction(source="pesquisa_noticias", target="verifica_relevancia", description="Verificação da relevância das notícias encontradas"),
                    Interaction(source="verifica_relevancia", target="envia_resposta", description="Envio da resposta ao usuário com notícias relevantes")]

    return ArchitectureOutput(nodes=nodes, interactions=interactions, route_next=True).model_dump_json()


EXAMPLES = [
    HumanMessage(name="human_example",
                 content=f'Aqui está o YAML: \n" + {_yaml_example()}' +
                 f'\n\nAqui está a ARQUITETURA ORIGINAL:\n" + {_architecture_example()}'),
    AIMessage(name="revisor_exemple",
              content='{ ' +
                  '"message": ' +
                  '"A edge entre verifica_relevancia e envia_resposta está faltando" ' +
                  '"agents": [ ' +
                  '"edge_creator" ' +
                  '] ' +
              '}')
]
