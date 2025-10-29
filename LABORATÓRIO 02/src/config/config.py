import os

# Tentar carregar variáveis do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv não encontrado, carregando variáveis manualmente")

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN or GITHUB_TOKEN == 'your_github_token_here':
    print("⚠️ Token do GitHub não configurado - usando modo limitado")
    print("Para melhor funcionamento:")
    print("1. Acesse: https://github.com/settings/tokens")
    print("2. Crie um Personal Access Token (classic)")
    print("3. Configure no arquivo .env: GITHUB_TOKEN=seu_token_aqui")
    GITHUB_TOKEN = None

# URLs da API do GitHub
REST_API_URL = 'https://api.github.com/search/repositories'
GRAPHQL_API_URL = 'https://api.github.com/graphql'

# Headers para requisições
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json',
    'User-Agent': 'Java-Quality-Analysis/1.0'
}

if GITHUB_TOKEN:
    HEADERS['Authorization'] = f'token {GITHUB_TOKEN}'

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