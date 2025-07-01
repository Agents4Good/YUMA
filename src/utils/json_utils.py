from langchain_core.output_parsers import JsonOutputParser
import re
import json
from utils.yuma import write_log


def extract_json(content, response_format):
    parser = JsonOutputParser(pydantic_object=response_format)
    response = None

    try:
        if isinstance(content, str) and "```" in content:
            pattern = r"```(?:json)?\s*({.*?})\s*```"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                raw_json_str = match.group(1)
                parsed = parser.parse(raw_json_str)
                response = response_format(**parsed)
                
            write_log("extract_json - Resposta é uma string com JSON", response)

        elif isinstance(content, str):
            json_start = content.find('{')
            if json_start != -1:
                raw_json_str = content[json_start:]
                parsed = json.loads(raw_json_str)
                response = response_format(**parsed)
                
            write_log("extract_json - Resposta é uma string", response)

        else:
            write_log("extract_json - Resposta não é uma string ou JSON válido", content)
            
        return response

    except Exception as e:
        write_log("extract_json - Erro ao parsear JSON", str(e))
        write_log("extract_json - Resposta bruta", content)
