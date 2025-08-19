# Tool Agent Template

> Descrição em alto nível dos componentes de um agente com ferramentas.

Um **agente com ferramentas** estende o padrão do agente simples adicionando a capacidade de invocar **funções externas** (tools).  
O fluxo é:  
- **Input** → recebe entrada do usuário.  
- **Reasoning** → processa com base no prompt + decide se precisa de uma ferramenta.  
- **Tool Use** (opcional) → executa chamadas externas.  
- **Output** → retorna a resposta final ao usuário.  

---

## Estrutura do Agente

### 1. Identificação
- **Nome do agente:** `<agent_name>`  

### 2. Modelo
- **LLM usado:** `<modelo (ex: gpt-4o)>`  
- **Configuração do modelo:**  
  - Temperatura: `<valor>`  
  - Máx. tokens: `<valor>`  
  - Outras configs: `<se houver>`  

### 3. Definição da persona
- **Papel:** `<descrição breve da persona que o agente deve assumir>`
- **Tarefa:** `<descrição breve do que o agente faz>` 


### 4. Prompt
- **Mensagem do Usuário:**  
Recebe o input inicial do usuário.

- **Resposta do Agente (AIMessage):**  
Retorna a resposta processada pelo modelo.

### 5. Ferramentas
Cada ferramenta segue o padrão:  

- **Nome da ferramenta:** `<tool_name>`  
- **Descrição:** `<o que a ferramenta faz>`  
- **Parâmetros:**  
- `<param_name>: <descrição>`  
- **Retorno esperado:** `<o que a função retorna>`  

### 6. Fluxo
1. Usuário envia um input.  
2. Agente avalia se resolve diretamente ou se precisa de uma ferramenta.  
3. Se houver chamada de ferramenta:  
 - Executa a ferramenta.  
 - Resultado retorna ao agente.  
 - Agente continua o raciocínio.  
4. Se não houver ferramenta necessária:  
 - Resposta final é retornada ao usuário.  

### 7. Execução
- **Entrada esperada:** `<tipo de input>`  
- **Saída gerada:** `<tipo de output>`  
- **Modo de execução:**  
- Interativo (terminal ou UI).  