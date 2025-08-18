# Simple Agent Template

> Descrição em alto nível dos componentes de um agente simples.

Um **agente simples** é definido pelo padrão:
- **Input** → recebe uma entrada do usuário ou sistema.
- **Reasoning** → processa a tarefa baseada em um prompt.
- **Output** → retorna a resposta sem memória, planejamento ou interação externa.

---

## Estrutura do Agente

### 1. Identificação
- **Nome do agente:** `<agent_name>`
- **Papel:** `<descrição breve da persona que o agente deve assumir>`
- **Tarefa:** `<descrição breve do que o agente faz>`  

### 2. Modelo
- **LLM usado:** `<modelo (ex: gpt-4o)>`
- **Configuração do modelo:**  
  - Temperatura: `<valor>`  
  - Máx. tokens: `<valor>`  
  - Outras configs: `<se houver>`

### 3. Prompt
- **System Prompt:**  
Prompt do sistema contendo papel e tarefa do agente

- **Mensagem do Usuário (HumanMessage):**  
Recebe o input inicial do usuário.

- **Resposta do Agente (AIMessage):**  
Retorna a resposta processada pelo modelo.

### 4. Fluxo
1. Entrada do usuário é capturada.  
2. Prompt do sistema + input do usuário são enviados ao modelo.  
3. O modelo gera uma resposta.  
4. O ciclo encerra (não há memória, nem repetição).

### 5. Execução
- **Entrada esperada:** `<tipo de input (ex: texto)>`
- **Saída gerada:** `<tipo de output (ex: texto)>`
- **Modo de execução:**  
- Interativo (via terminal ou UI simples).  
- Script direto (chamando função `execute_graph` ou equivalente).  

---

## Exemplo de Uso

- **Usuário:** "Qual a capital da França?"  
- **Agente:** "A capital da França é Paris."