# Analisador de Repositórios Populares do GitHub

Este projeto coleta e analisa dados dos 1.000 repositórios com o maior número de estrelas no GitHub para identificar tendências em linguagens de programação, licenças e outras características.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação. Orquestra a coleta e a análise dos dados.
- `src/config.py`: Gerencia a configuração, como o token da API do GitHub e caminhos de arquivos.
- `src/data_collector.py`: Módulo responsável por buscar os dados da API do GitHub.
- `src/data_analyzer.py`: Módulo responsável por analisar os dados coletados e gerar visualizações.
- `output/`: Diretório (criado automaticamente) para salvar os dados em CSV e os gráficos gerados.

## Como Configurar

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd github_top_repos_analyzer
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Token da API:**
    - Crie um arquivo chamado `.env` na raiz do projeto.
    - Adicione seu Token de Acesso Pessoal do GitHub a ele:
      ```
      GITHUB_TOKEN="ghp_seu_token_aqui"
      ```

## Como Executar

Após a configuração, basta executar o script principal:

```bash
python main.py