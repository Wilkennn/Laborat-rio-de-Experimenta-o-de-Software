"""
Configurações do projeto Lab03 - Análise de Code Review no GitHub
Versão ajustada com pathlib e type hinting.
"""
import os
from dotenv import load_dotenv
import logging
import logging.config
from pathlib import Path
from typing import List, Dict, ClassVar

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações gerais do projeto"""

    # GitHub API
    GITHUB_TOKEN: ClassVar[str] = os.getenv('GITHUB_TOKEN', '')
    GITHUB_API_BASE_URL: ClassVar[str] = 'https://api.github.com'

    # Parâmetros de coleta
    TOP_REPOS_COUNT: ClassVar[int] = 200
    MIN_PRS_PER_REPO: ClassVar[int] = 100
    MIN_REVIEW_TIME_HOURS: ClassVar[int] = 1

    # Rate limiting
    REQUESTS_PER_HOUR: ClassVar[int] = 5000  # GitHub API limit for authenticated requests
    SLEEP_TIME: ClassVar[float] = 3600 / REQUESTS_PER_HOUR  # Seconds between requests

    # Caminhos de arquivo (usando pathlib)
    OUTPUT_DIR: ClassVar[Path] = Path('output')
    DATA_DIR: ClassVar[Path] = OUTPUT_DIR / 'data'
    PLOTS_DIR: ClassVar[Path] = OUTPUT_DIR / 'plots'

    # Arquivos de saída
    REPOS_LIST_FILE: ClassVar[Path] = DATA_DIR / 'selected_repositories.csv'
    PRS_DATA_FILE: ClassVar[Path] = DATA_DIR / 'pull_requests_data.csv'
    ANALYSIS_RESULTS_FILE: ClassVar[Path] = DATA_DIR / 'analysis_results.json'

    # Configurações de análise
    CORRELATION_METHODS: ClassVar[List[str]] = ['pearson', 'spearman']
    SIGNIFICANCE_LEVEL: ClassVar[float] = 0.05

    # Métricas a serem coletadas
    METRICS: ClassVar[Dict[str, List[str]]] = {
        'size': ['files_changed', 'additions', 'deletions', 'total_changes'],
        'time': ['analysis_time_hours', 'analysis_time_days'],
        'description': ['description_length', 'has_description'],
        'interactions': ['participants_count', 'comments_count', 'review_comments_count']
    }

    # Status de PR que interessam
    PR_STATES: ClassVar[List[str]] = ['closed', 'merged']

    @classmethod
    def validate_config(cls) -> bool:
        """Valida se as configurações estão corretas"""
        if not cls.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN não configurado. Defina a variável de ambiente ou no arquivo .env")

        # Cria diretórios se não existirem (usando pathlib)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.PLOTS_DIR.mkdir(exist_ok=True)

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
            'filename': str(Config.OUTPUT_DIR / 'lab03.log'),
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