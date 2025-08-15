import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env que está na raiz do projeto
load_dotenv()

# --- Configurações da API do GitHub ---
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise ValueError("Token do GitHub não encontrado. Verifique seu arquivo .env na raiz do projeto.")

# URL base da API de busca de repositórios
API_URL = 'https://api.github.com/search/repositories'

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}


# --- Configurações da Coleta de Dados ---
# Número de repositórios por página (o máximo permitido pela API é 100)
REPOS_PER_PAGE = 100

# Total de repositórios para busca
TOTAL_REPOS_TO_FETCH = 1000

# --- Configurações de Caminhos de Saída ---
# Define os nomes dos diretórios onde os resultados serão salvos
OUTPUT_DIR = "output"
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")

# Define o caminho completo para o arquivo CSV de saída
CSV_FILEPATH = os.path.join(DATA_DIR, "top_1000_repos.csv")