import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN or GITHUB_TOKEN == 'your_github_token_here':
    print("Atenção: Configure seu token do GitHub no arquivo .env")
    print("1. Acesse: https://github.com/settings/tokens")
    print("2. Crie um Personal Access Token (classic)")
    print("3. Substitua 'your_github_token_here' no arquivo .env pelo seu token")
    print("4. Execute novamente o programa")
    raise ValueError("Token do GitHub não configurado corretamente.")

# URLs da API do GitHub
REST_API_URL = 'https://api.github.com/search/repositories'
GRAPHQL_API_URL = 'https://api.github.com/graphql'

# Headers para requisições
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json',
    'User-Agent': 'Java-Quality-Analysis/1.0'
}

# Configurações de coleta
REPOS_PER_PAGE = 100  # Máximo permitido pela API do GitHub
TOTAL_REPOS_TO_FETCH = 1000  # Conforme especificado no laboratório

# Configurações para teste inicial (1 repositório)
TEST_MODE = True
TEST_REPOS_COUNT = 1

# Diretórios de saída
OUTPUT_DIR = "output"
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
TEMP_DIR = "temp_repos"

# Arquivos de saída
CSV_FILEPATH = os.path.join(DATA_DIR, f"top_{TOTAL_REPOS_TO_FETCH}_java_repos.csv")
CSV_TEST_FILEPATH = os.path.join(DATA_DIR, "test_single_repo.csv")
REPOS_LIST_FILEPATH = os.path.join(DATA_DIR, "top_1000_java_repos_list.csv")

# Caminho padrão para a ferramenta CK (pode ser alterado no main.py)
DEFAULT_CK_PATH = r"C:\Users\Nery\Desktop\ck-tool.jar"