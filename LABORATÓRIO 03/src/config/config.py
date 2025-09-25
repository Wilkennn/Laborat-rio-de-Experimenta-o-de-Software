"""
Configurações do projeto Lab03 - Análise de Code Review no GitHub
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações gerais do projeto"""
    
    # GitHub API
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_API_BASE_URL = 'https://api.github.com'
    
    # Parâmetros de coleta
    TOP_REPOS_COUNT = 200
    MIN_PRS_PER_REPO = 100
    MIN_REVIEW_TIME_HOURS = 1
    
    # Rate limiting
    REQUESTS_PER_HOUR = 5000  # GitHub API limit for authenticated requests
    SLEEP_TIME = 3600 / REQUESTS_PER_HOUR  # Seconds between requests
    
    # Caminhos de arquivo
    OUTPUT_DIR = 'output'
    DATA_DIR = 'output/data'
    PLOTS_DIR = 'output/plots'
    
    # Arquivos de saída
    REPOS_LIST_FILE = 'output/data/selected_repositories.csv'
    PRS_DATA_FILE = 'output/data/pull_requests_data.csv'
    ANALYSIS_RESULTS_FILE = 'output/data/analysis_results.json'
    
    # Configurações de análise
    CORRELATION_METHODS = ['pearson', 'spearman']
    SIGNIFICANCE_LEVEL = 0.05
    
    # Métricas a serem coletadas
    METRICS = {
        'size': ['files_changed', 'additions', 'deletions', 'total_changes'],
        'time': ['analysis_time_hours', 'analysis_time_days'],
        'description': ['description_length', 'has_description'],
        'interactions': ['participants_count', 'comments_count', 'review_comments_count']
    }
    
    # Status de PR que interessam
    PR_STATES = ['closed', 'merged']
    
    @classmethod
    def validate_config(cls):
        """Valida se as configurações estão corretas"""
        if not cls.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN não configurado. Defina a variável de ambiente ou no arquivo .env")
        
        # Cria diretórios se não existirem
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.PLOTS_DIR, exist_ok=True)
        
        return True

# Configurações específicas para logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'output/lab03.log',
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}