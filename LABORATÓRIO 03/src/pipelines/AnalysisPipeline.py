import logging
import logging.config

from src.config.config import Config, LOGGING_CONFIG
from src.collectors.repo_selector import RepositorySelector
from src.collectors.github_collector import GitHubCollector
from src.modules.metrics_calculator import MetricsCalculator

class AnalysisPipeline:
    """Orquestra a execução de todas as etapas do pipeline de análise."""

    def __init__(self, args):
        """
        Inicializa o pipeline com os argumentos da linha de comando.
        
        Args:
            args: Argumentos parseados do argparse.
        """
        self.args = args
        self.repo_selector = RepositorySelector()
        self.github_collector = GitHubCollector()
        self.metrics_calculator = MetricsCalculator()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Executa o fluxo completo do pipeline de análise."""
        self.logger.info("=" * 60)
        self.logger.info("LABORATÓRIO 03 - ANÁLISE DE CODE REVIEW NO GITHUB")
        self.logger.info("=" * 60)
        
        repositories = []
        prs_data = []

        # Etapa 1: Seleção de repositórios
        if not self.args.skip_selection:
            repositories = self._select_repositories()
            if not repositories:
                self.logger.error("Falha na seleção de repositórios. Abortando.")
                return
        else:
            self.logger.info("Etapa 1: Seleção de repositórios pulada por parâmetro.")

        # Etapa 2: Coleta de Pull Requests
        if not self.args.skip_collection:
            prs_data = self._collect_prs(repositories)
        else:
            self.logger.info("Etapa 2: Coleta de PRs pulada por parâmetro.")

        # Etapa 3: Cálculo de métricas
        if not self.args.skip_metrics:
            self._calculate_metrics(prs_data)
        else:
            self.logger.info("Etapa 3: Cálculo de métricas pulado por parâmetro.")

        self.logger.info("=" * 60)
        self.logger.info("PIPELINE DE ANÁLISE FINALIZADO")
        self.logger.info("=" * 60)
        self.logger.info("\nPróximos passos:")
        self.logger.info("1. Verificar os arquivos de dados gerados no diretório 'output/data/'.")
        self.logger.info("2. Utilizar os dados para análises e visualizações.")

    def _select_repositories(self):
        """Executa a lógica de seleção de repositórios."""
        self.logger.info("=== ETAPA 1: SELEÇÃO DE REPOSITÓRIOS ===")
        try:
            selected_repos = self.repo_selector.select_repositories(
                count=self.args.repos, 
                min_prs=self.args.min_prs, 
                save=True
            )
            self.logger.info(f"✓ {len(selected_repos)} repositórios selecionados com sucesso.")
            return selected_repos
        except Exception as e:
            self.logger.error(f"✗ Erro na seleção de repositórios: {e}", exc_info=True)
            return []

    def _collect_prs(self, repositories):
        """Executa a lógica de coleta de Pull Requests."""
        if not repositories:
            self.logger.warning("Nenhum repositório fornecido para a coleta de PRs.")
            return []
            
        self.logger.info("=== ETAPA 2: COLETA DE PULL REQUESTS ===")
        try:
            all_prs = self.github_collector.collect_multiple_repositories(
                repositories, 
            )
            filepath = self.github_collector.save_prs_data(all_prs, "pull_requests_data.csv")
            self.logger.info(f"✓ {len(all_prs)} PRs coletados e salvos em: {filepath}")
            return all_prs
        except Exception as e:
            self.logger.error(f"✗ Erro na coleta de PRs: {e}", exc_info=True)
            return []

    def _calculate_metrics(self, prs_data):
        """Executa a lógica de cálculo de métricas."""
        if not prs_data:
            self.logger.warning("Nenhum dado de PR fornecido para cálculo de métricas.")
            return
            
        self.logger.info("=== ETAPA 3: CÁLCULO DE MÉTRICAS ===")
        try:
            df_with_metrics = self.metrics_calculator.calculate_all_metrics(prs_data)
            filepath = self.metrics_calculator.save_metrics(df_with_metrics, "prs_with_metrics.csv")
            self.logger.info(f"✓ Métricas calculadas para {len(df_with_metrics)} PRs e salvas em: {filepath}")
        except Exception as e:
            self.logger.error(f"✗ Erro no cálculo de métricas: {e}", exc_info=True)

def setup_environment():
    """Valida a configuração e inicializa o sistema de logging."""
    try:
        Config.validate_config()
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger.info("✓ Ambiente configurado e logging iniciado.")
    except ValueError as e:
        print(f"[ERRO CRÍTICO] Erro de configuração: {e}")
        sys.exit(1)