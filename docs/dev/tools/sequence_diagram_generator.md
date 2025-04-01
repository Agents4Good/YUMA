# Documentação da Função `sequence_diagram_generator`

## Descrição
A função `sequence_diagram_generator` converte a saída de um agente de arquitetura em um diagrama de sequência no formato PlantUML e gera uma imagem correspondente.

## Assinatura
```python
@tool("sequence_diagram_generator")
def sequence_diagram_generator(architecture_output: str):
```

## Parâmetros
- `architecture_output` (str): A saída do agente de arquitetura no formato JSON.

## Funcionalidade
1. Converte a representação JSON do `architecture_output` para o formato PlantUML utilizando a função `json_to_plantuml`.
2. Gera uma imagem do diagrama de sequência utilizando a função `generate_diagram`.

## Retorno
- Retorna o caminho do arquivo de imagem gerado.

## Exemplo de Uso
```python
diagram_path = sequence_diagram_generator(architecture_output_json)
print(f"Diagrama gerado em: {diagram_path}")
```

## Observações
- A função faz uso de `json_to_plantuml` para converter JSON em PlantUML.
- A função `generate_diagram` renderiza o diagrama em imagem.
- Certifique-se de que o PlantUML esteja instalado e configurado corretamente para gerar o diagrama.

