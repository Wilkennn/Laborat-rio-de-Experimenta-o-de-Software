"""
LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub
Ponto de entrada (entrypoint) para a execução da análise.
"""

import sys
import os
import logging
import logging.config
import argparse
from src.config.config import Config, LOGGING_CONFIG
from src.pipelines.AnalysisPipeline import AnalysisPipeline

# Adiciona o diretório src ao path para encontrar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def setup_environment():
    """Valida a configuração e inicializa o sistema de logging."""
    try:
        logger = logging.getLogger(__name__)
        Config.validate_config()
        logging.config.dictConfig(LOGGING_CONFIG)
        logger.info("✓ Ambiente configurado e logging iniciado.")
    except ValueError as e:
        print(f"[ERRO CRÍTICO] Erro de configuração: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Lab03 - Pipeline Completo de Análise de Code Review no GitHub')
    
    # Argumentos para coleta (LAB03S01/S02)
    parser.add_argument('--repos', type=int, default=Config.TOP_REPOS_COUNT, 
                       help='Número de repositórios a buscar.')
    parser.add_argument('--min-prs', type=int, default=Config.MIN_PRS_PER_REPO, 
                       help='Mínimo de PRs por repositório.')
    parser.add_argument('--max-repos', type=int, 
                       help='Limita a coleta a N repositórios (para testes).')
    
    # Argumentos para controle de etapas
    parser.add_argument('--skip-selection', action='store_true', 
                       help='Pular a etapa de seleção de repositórios.')
    parser.add_argument('--skip-collection', action='store_true', 
                       help='Pular a etapa de coleta de PRs.')
    parser.add_argument('--skip-metrics', action='store_true', 
                       help='Pular a etapa de cálculo de métricas.')
    
    # Argumentos específicos para LAB03S03
    parser.add_argument('--only-analysis', action='store_true',
                       help='Executar apenas análise estatística, visualizações e relatório (LAB03S03).')
    parser.add_argument('--quick-test', action='store_true',
                       help='Modo teste rápido com dados limitados.')
    
    args = parser.parse_args()
    
    # Se modo apenas análise, pula coleta
    if args.only_analysis:
        args.skip_selection = True
        args.skip_collection = True  
        args.skip_metrics = True
    
    # Modo teste rápido
    if args.quick_test:
        args.max_repos = 5  # Apenas 5 repos para teste
        print("🧪 MODO TESTE RÁPIDO ATIVADO - Coletando apenas 5 repositórios")
    
    setup_environment()
    
    pipeline = AnalysisPipeline(args)
    pipeline.run()


if __name__ == "__main__":
    main()