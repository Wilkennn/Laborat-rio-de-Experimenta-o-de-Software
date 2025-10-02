"""
LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub
Sprint 1: Lista de repositórios selecionados + Criação do script de coleta dos PRs e das métricas definidas

Este script implementa a primeira sprint do laboratório, incluindo:
1. Seleção de repositórios populares com critérios definidos
2. Coleta de dados de Pull Requests
3. Cálculo das métricas definidas
"""

import sys
import os
import logging
import logging.config
import argparse
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.config import Config, LOGGING_CONFIG
from src.collectors.repo_selector import RepositorySelector
from src.collectors.github_collector import GitHubCollector
from src.modules.metrics_calculator import MetricsCalculator

try:
    Config.validate_config()
except ValueError as e:
    # Se a validação falhar (ex: GITHUB_TOKEN faltando), o programa para aqui.
    print(f"Erro de configuração: {e}")
    sys.exit(1)

# 2. AGORA CONFIGURE O LOGGING
# A configuração funcionará porque o diretório para o log já foi criado.
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.info("Iniciando a Sprint 1 do Laboratório 03.")
logger.info("Configuração validada e logging iniciado com sucesso.")

def setup_environment():
    """Configura ambiente e valida configurações"""
    try:
        Config.validate_config()
        logger.info("✓ Configurações validadas com sucesso")
        return True
    except Exception as e:
        logger.error(f"✗ Erro na configuração: {str(e)}")
        return False

def sprint1_select_repositories(count: int = 200, min_prs: int = 100):
    """
    Sprint 1 - Etapa 1: Seleção de repositórios
    
    Args:
        count: Número de repositórios populares a buscar inicialmente
        min_prs: Número mínimo de PRs por repositório
    """
    logger.info("=== SPRINT 1 - ETAPA 1: SELEÇÃO DE REPOSITÓRIOS ===")
    
    try:
        # Inicializa seletor de repositórios
        repo_selector = RepositorySelector()
        
        # Executa seleção completa
        selected_repos = repo_selector.select_repositories(
            count=count, 
            min_prs=min_prs, 
            save=True
        )
        
        if selected_repos:
            logger.info(f"✓ {len(selected_repos)} repositórios selecionados com sucesso")
            
            # Log dos repositórios selecionados
            logger.info("Repositórios selecionados:")
            for i, repo in enumerate(selected_repos[:10]):  # Mostra os 10 primeiros
                logger.info(f"  {i+1}. {repo['full_name']} ({repo['stars']} stars, {repo.get('pr_count', 'N/A')} PRs)")
            
            if len(selected_repos) > 10:
                logger.info(f"  ... e mais {len(selected_repos) - 10} repositórios")
            
            return selected_repos
        else:
            logger.error("✗ Nenhum repositório foi selecionado")
            return []
            
    except Exception as e:
        logger.error(f"✗ Erro na seleção de repositórios: {str(e)}")
        return []

def sprint1_collect_prs(repositories, max_repos: int = None):
    """
    Sprint 1 - Etapa 2: Coleta de Pull Requests
    
    Args:
        repositories: Lista de repositórios selecionados
        max_repos: Número máximo de repositórios para coletar (para testes)
    """
    logger.info("=== SPRINT 1 - ETAPA 2: COLETA DE PULL REQUESTS ===")
    
    if not repositories:
        logger.error("✗ Nenhum repositório fornecido para coleta")
        return []
    
    try:
        # Limita número de repositórios se especificado
        if max_repos and max_repos < len(repositories):
            repositories = repositories[:max_repos]
            logger.info(f"Limitando coleta a {max_repos} repositórios para teste")
        
        # Inicializa coletor do GitHub
        github_collector = GitHubCollector()
        
        # Coleta PRs de todos os repositórios
        all_prs = github_collector.collect_multiple_repositories(repositories)
        
        if all_prs:
            logger.info(f"✓ {len(all_prs)} PRs coletados com sucesso")
            
            # Salva dados coletados
            filepath = github_collector.save_prs_data(all_prs, "pull_requests_data.csv")
            logger.info(f"✓ Dados salvos em: {filepath}")
            
            return all_prs
        else:
            logger.error("✗ Nenhum PR foi coletado")
            return []
            
    except Exception as e:
        logger.error(f"✗ Erro na coleta de PRs: {str(e)}")
        return []

def sprint1_calculate_metrics(prs_data):
    """
    Sprint 1 - Etapa 3: Cálculo de métricas
    
    Args:
        prs_data: Dados dos Pull Requests coletados
    """
    logger.info("=== SPRINT 1 - ETAPA 3: CÁLCULO DE MÉTRICAS ===")
    
    if not prs_data:
        logger.error("✗ Nenhum dado de PR fornecido para cálculo de métricas")
        return None
    
    try:
        # Inicializa calculador de métricas
        metrics_calculator = MetricsCalculator()
        
        # Calcula todas as métricas
        df_with_metrics = metrics_calculator.calculate_all_metrics(prs_data)
        
        if not df_with_metrics.empty:
            logger.info(f"✓ Métricas calculadas para {len(df_with_metrics)} PRs")
            
            # Gera estatísticas resumo
            summary = metrics_calculator.get_summary_statistics(df_with_metrics)
            
            # Log de estatísticas básicas
            logger.info(f"Estatísticas gerais:")
            logger.info(f"  - Total de PRs: {summary.get('total_prs', 0)}")
            logger.info(f"  - PRs merged: {summary.get('merged_prs', 0)}")
            logger.info(f"  - PRs closed: {summary.get('closed_prs', 0)}")
            logger.info(f"  - Taxa de merge: {summary.get('merge_rate', 0):.1f}%")
            
            # Salva DataFrame com métricas
            filepath = metrics_calculator.save_metrics(df_with_metrics, "prs_with_metrics.csv")
            logger.info(f"✓ Métricas salvas em: {filepath}")
            
            return df_with_metrics, summary
        else:
            logger.error("✗ Erro no cálculo das métricas")
            return None, None
            
    except Exception as e:
        logger.error(f"✗ Erro no cálculo de métricas: {str(e)}")
        return None, None

def main():
    """Função principal - executa Sprint 1 completa"""
    parser = argparse.ArgumentParser(description='Lab03 Sprint 1 - Seleção de repositórios e coleta de dados')
    parser.add_argument('--repos', type=int, default=200, help='Número de repositórios a buscar inicialmente')
    parser.add_argument('--min-prs', type=int, default=100, help='Número mínimo de PRs por repositório')
    parser.add_argument('--max-repos', type=int, help='Número máximo de repositórios para coletar (teste)')
    parser.add_argument('--skip-selection', action='store_true', help='Pular seleção de repositórios')
    parser.add_argument('--skip-collection', action='store_true', help='Pular coleta de PRs')
    parser.add_argument('--skip-metrics', action='store_true', help='Pular cálculo de métricas')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("LABORATÓRIO 03 - SPRINT 1")
    logger.info("Caracterizando a Atividade de Code Review no GitHub")
    logger.info("=" * 60)
    
    # 1. Configura ambiente
    if not setup_environment():
        sys.exit(1)
    
    repositories = []
    prs_data = []
    
    # 2. Seleção de repositórios
    if not args.skip_selection:
        repositories = sprint1_select_repositories(args.repos, args.min_prs)
        if not repositories:
            logger.error("Falha na seleção de repositórios. Abortando.")
            sys.exit(1)
    else:
        logger.info("Seleção de repositórios pulada por parâmetro")
    
    # 3. Coleta de Pull Requests
    if not args.skip_collection and repositories:
        prs_data = sprint1_collect_prs(repositories, args.max_repos)
        if not prs_data:
            logger.error("Falha na coleta de PRs. Continuando para métricas...")
    else:
        logger.info("Coleta de PRs pulada por parâmetro")
    
    # 4. Cálculo de métricas
    if not args.skip_metrics and prs_data:
        df_metrics, summary = sprint1_calculate_metrics(prs_data)
        if df_metrics is not None:
            logger.info("✓ Sprint 1 concluída com sucesso!")
        else:
            logger.error("Falha no cálculo das métricas")
    else:
        logger.info("Cálculo de métricas pulado por parâmetro")
    
    logger.info("=" * 60)
    logger.info("SPRINT 1 FINALIZADA")
    logger.info("=" * 60)
    
    # Instruções para próximos passos
    logger.info("\nPróximos passos:")
    logger.info("1. Verificar arquivos gerados em output/data/")
    logger.info("2. Analisar dados coletados")
    logger.info("3. Preparar para Sprint 2: Dataset completo + Relatório com hipóteses")

if __name__ == "__main__":
    main()