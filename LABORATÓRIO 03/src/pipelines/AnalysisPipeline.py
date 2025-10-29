import logging
import logging.config
import pandas as pd
import time
from pathlib import Path

from src.config.config import Config, LOGGING_CONFIG
from src.collectors.repo_selector import RepositorySelector
from src.collectors.github_collector import GitHubCollector
from src.collectors.graphql_collector import GraphQLGitHubCollector
from src.modules.metrics_calculator import MetricsCalculator
from src.modules.statistical_analyzer import StatisticalAnalyzer
from src.modules.data_visualizer import DataVisualizer
from src.modules.report_generator import ReportGenerator
from src.modules.methodology_validator import MethodologyValidator

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
        self.graphql_collector = GraphQLGitHubCollector()  # Coletor GraphQL otimizado
        self.metrics_calculator = MetricsCalculator()
        self.statistical_analyzer = StatisticalAnalyzer()
        self.data_visualizer = DataVisualizer()
        self.report_generator = ReportGenerator()
        self.methodology_validator = MethodologyValidator()
        self.logger = logging.getLogger(__name__)

    def run(self):
        """Executa o fluxo completo do pipeline de análise."""
        self.logger.info("=" * 60)
        self.logger.info("LABORATÓRIO 03 - ANÁLISE DE CODE REVIEW NO GITHUB")
        self.logger.info("=" * 60)
        
        repositories = []
        prs_data = []
        df_with_metrics = None
        analysis_results = {}
        plot_files = {}

        # Etapa 1: Seleção de repositórios
        if not self.args.skip_selection:
            repositories = self._select_repositories()
            if not repositories:
                self.logger.error("Falha na seleção de repositórios. Abortando.")
                return
        else:
            self.logger.info("Etapa 1: Seleção de repositórios pulada por parâmetro.")
            # Tenta carregar repositórios salvos
            repositories = self._load_saved_repositories()

        # Etapa 2: Coleta de Pull Requests
        if not self.args.skip_collection:
            prs_data = self._collect_prs(repositories)
        else:
            self.logger.info("Etapa 2: Coleta de PRs pulada por parâmetro.")
            # Tenta carregar dados de PRs salvos
            prs_data = self._load_saved_prs_data()

        # Etapa 3: Cálculo de métricas
        if not self.args.skip_metrics:
            df_with_metrics = self._calculate_metrics(prs_data)
        else:
            self.logger.info("Etapa 3: Cálculo de métricas pulado por parâmetro.")
            # Tenta carregar métricas salvas
            df_with_metrics = self._load_saved_metrics()

        # Etapa 4: Análise Estatística (LAB03S03)
        if df_with_metrics is not None and not df_with_metrics.empty:
            analysis_results = self._perform_statistical_analysis(df_with_metrics)
        else:
            self.logger.error("Nenhum dado disponível para análise estatística.")
            return

        # Etapa 5: Visualização de Dados (LAB03S03)
        if analysis_results:
            plot_files = self._create_visualizations(df_with_metrics, analysis_results)

        # Etapa 6: Geração do Relatório Final (LAB03S03)
        if analysis_results and plot_files:
            self._generate_final_report(df_with_metrics, analysis_results, plot_files)

        # Etapa 7: Validação de Conformidade com Metodologia
        if repositories and prs_data and df_with_metrics is not None and analysis_results:
            self._validate_methodology_compliance(repositories, prs_data, df_with_metrics, analysis_results)

        self.logger.info("=" * 60)
        self.logger.info("PIPELINE DE ANÁLISE FINALIZADO - LAB03S03 COMPLETO")
        self.logger.info("=" * 60)
        self.logger.info("\nArquivos gerados:")
        self.logger.info("1. Dados: output/data/")
        self.logger.info("2. Visualizações: output/plots/")
        self.logger.info("3. Relatório final: output/")
        self.logger.info("4. Resultados JSON: output/")

    def _select_repositories(self):
        """Executa a lógica de seleção de repositórios com fallback GraphQL -> REST."""
        self.logger.info("=== ETAPA 1: SELEÇÃO DE REPOSITÓRIOS ===")
        
        # Tenta GraphQL primeiro (mais eficiente)
        try:
            self.logger.info("Tentando coleta via GraphQL...")
            selected_repos = self.graphql_collector.search_popular_repositories(
                count=self.args.repos
            )
            
            if selected_repos:
                # Filtra apenas repositórios com PRs suficientes
                valid_repos = [repo for repo in selected_repos if repo.get('pr_count', 0) >= self.args.min_prs]
                
                if valid_repos:
                    filepath = self.graphql_collector.save_data_to_csv(valid_repos, "selected_repositories.csv")
                    self.logger.info(f"✓ GraphQL: {len(valid_repos)} repositórios selecionados e salvos em: {filepath}")
                    return valid_repos
        except Exception as e:
            self.logger.warning(f"GraphQL falhou: {e}")
        
        # Fallback para REST API (mais estável)
        try:
            self.logger.info("Usando fallback REST API...")
            selected_repos = self.repo_selector.select_repositories(
                count=self.args.repos, 
                min_prs=self.args.min_prs, 
                save=True
            )
            self.logger.info(f"✓ REST API: {len(selected_repos)} repositórios selecionados com sucesso.")
            return selected_repos
        except Exception as e:
            self.logger.error(f"✗ Erro na seleção de repositórios (REST): {e}", exc_info=True)
            return []

    def _collect_prs(self, repositories):
        """Executa a lógica de coleta de Pull Requests com fallback GraphQL -> REST."""
        if not repositories:
            self.logger.warning("Nenhum repositório fornecido para a coleta de PRs.")
            return []
            
        self.logger.info("=== ETAPA 2: COLETA DE PULL REQUESTS ===")
        
        # Limita repositórios se especificado
        repos_to_process = repositories
        if self.args.max_repos:
            repos_to_process = repositories[:self.args.max_repos]
            self.logger.info(f"Limitando coleta a {len(repos_to_process)} repositórios")
        
        all_prs = []
        
        # Tenta GraphQL primeiro
        try:
            self.logger.info("Tentando coleta via GraphQL...")
            for i, repo in enumerate(repos_to_process):
                owner = repo.get('owner') or repo.get('full_name', '').split('/')[0]
                name = repo.get('name') or repo.get('full_name', '').split('/')[-1]
                
                if not owner or not name:
                    self.logger.warning(f"Repositório inválido: {repo}")
                    continue
                
                self.logger.info(f"GraphQL: Coletando PRs [{i+1}/{len(repos_to_process)}]: {owner}/{name}")
                
                # Coleta PRs usando GraphQL com limite otimizado
                repo_prs = self.graphql_collector.collect_pull_requests_batch(
                    owner, name  # Usa Config.MAX_PRS_PER_REPO automaticamente
                )
                
                if repo_prs:
                    all_prs.extend(repo_prs)
                    self.logger.info(f"  ✓ {len(repo_prs)} PRs válidos coletados")
                else:
                    self.logger.warning(f"  ✗ Nenhum PR válido encontrado")
            
            # Salva dados coletados
            if all_prs:
                filepath = self.graphql_collector.save_data_to_csv(all_prs, "pull_requests_data.csv")
                self.logger.info(f"✓ GraphQL: {len(all_prs)} PRs totais coletados e salvos em: {filepath}")
                return all_prs
            
        except Exception as e:
            self.logger.warning(f"GraphQL falhou: {e}")
            all_prs = []  # Reset para tentar REST
        
        # Fallback para REST API
        try:
            self.logger.info("Usando fallback REST API para PRs...")
            for i, repo in enumerate(repos_to_process):
                owner = repo.get('owner') or repo.get('full_name', '').split('/')[0]
                name = repo.get('name') or repo.get('full_name', '').split('/')[-1]
                
                if not owner or not name:
                    continue
                
                repo_name = f"{owner}/{name}"
                self.logger.info(f"REST: Coletando PRs [{i+1}/{len(repos_to_process)}]: {repo_name}")
                
                try:
                    prs = self.pr_collector.collect_pull_requests(
                        repo_name, 
                        max_prs=200,
                        save=False
                    )
                    all_prs.extend(prs)
                    self.logger.info(f"  ✓ {len(prs)} PRs coletados via REST")
                    time.sleep(0.5)  # Rate limiting
                except Exception as e:
                    self.logger.warning(f"  ✗ Erro REST em {repo_name}: {e}")
                    continue
            
            # Salva todos os PRs via pr_collector
            if all_prs:
                # Cria dataframe e salva
                import pandas as pd
                df = pd.DataFrame(all_prs)
                output_dir = Path(__file__).parent.parent.parent / "output" / "data"
                output_dir.mkdir(parents=True, exist_ok=True)
                filepath = output_dir / "pull_requests_data.csv"
                df.to_csv(filepath, index=False)
                self.logger.info(f"✓ REST API: {len(all_prs)} PRs totais coletados e salvos em: {filepath}")
            
            return all_prs
            
        except Exception as e:
            self.logger.error(f"✗ Erro na coleta de PRs (REST): {e}", exc_info=True)
            return []

    def _calculate_metrics(self, prs_data):
        """Executa a lógica de cálculo de métricas."""
        if not prs_data:
            self.logger.warning("Nenhum dado de PR fornecido para cálculo de métricas.")
            return None
            
        self.logger.info("=== ETAPA 3: CÁLCULO DE MÉTRICAS ===")
        try:
            df_with_metrics = self.metrics_calculator.calculate_all_metrics(prs_data)
            filepath = self.metrics_calculator.save_metrics(df_with_metrics, "prs_with_metrics.csv")
            self.logger.info(f"✓ Métricas calculadas para {len(df_with_metrics)} PRs e salvas em: {filepath}")
            return df_with_metrics
        except Exception as e:
            self.logger.error(f"✗ Erro no cálculo de métricas: {e}", exc_info=True)
            return None
    
    def _perform_statistical_analysis(self, df_with_metrics):
        """Executa análise estatística das questões de pesquisa."""
        self.logger.info("=== ETAPA 4: ANÁLISE ESTATÍSTICA (RQ01-RQ08) ===")
        try:
            analysis_results = self.statistical_analyzer.analyze_research_questions(df_with_metrics)
            self.logger.info("✓ Análise estatística concluída para todas as questões de pesquisa")
            return analysis_results
        except Exception as e:
            self.logger.error(f"✗ Erro na análise estatística: {e}", exc_info=True)
            return {}
    
    def _create_visualizations(self, df_with_metrics, analysis_results):
        """Cria visualizações dos dados e resultados."""
        self.logger.info("=== ETAPA 5: CRIAÇÃO DE VISUALIZAÇÕES ===")
        try:
            plot_files = self.data_visualizer.create_all_visualizations(df_with_metrics, analysis_results)
            self.logger.info(f"✓ {len(plot_files)} visualizações criadas e salvas")
            return plot_files
        except Exception as e:
            self.logger.error(f"✗ Erro na criação de visualizações: {e}", exc_info=True)
            return {}
    
    def _generate_final_report(self, df_with_metrics, analysis_results, plot_files):
        """Gera o relatório final completo e valida conformidade."""
        self.logger.info("=== ETAPA 6: GERAÇÃO DO RELATÓRIO FINAL ===")
        try:
            report_path = self.report_generator.generate_final_report(df_with_metrics, analysis_results, plot_files)
            self.logger.info(f"✓ Relatório final gerado: {report_path}")
            return report_path
        except Exception as e:
            self.logger.error(f"✗ Erro na geração do relatório: {e}", exc_info=True)
            return None
    
    def _validate_methodology_compliance(self, repositories, prs_data, df_with_metrics, analysis_results):
        """Valida se a execução seguiu a metodologia do LAB03."""
        self.logger.info("=== VALIDAÇÃO DE CONFORMIDADE COM METODOLOGIA LAB03 ===")
        try:
            compliance_report = self.methodology_validator.generate_compliance_report(
                repositories, prs_data, df_with_metrics, analysis_results
            )
            
            # Log do relatório linha por linha para melhor visualização
            for line in compliance_report.split('\n'):
                if line.strip():
                    self.logger.info(line)
                    
        except Exception as e:
            self.logger.error(f"✗ Erro na validação de conformidade: {e}", exc_info=True)
    
    def _load_saved_repositories(self):
        """Carrega repositórios salvos de execução anterior."""
        try:
            repos_file = Config.DATA_DIR / "selected_repositories.csv"
            if repos_file.exists():
                df = pd.read_csv(repos_file)
                repositories = df.to_dict('records')
                self.logger.info(f"✓ Carregados {len(repositories)} repositórios salvos")
                return repositories
        except Exception as e:
            self.logger.warning(f"Erro ao carregar repositórios salvos: {e}")
        return []
    
    def _load_saved_prs_data(self):
        """Carrega dados de PRs salvos de execução anterior."""
        try:
            prs_file = Config.DATA_DIR / "pull_requests_data.csv"
            if prs_file.exists():
                df = pd.read_csv(prs_file)
                prs_data = df.to_dict('records')
                self.logger.info(f"✓ Carregados {len(prs_data)} PRs salvos")
                return prs_data
        except Exception as e:
            self.logger.warning(f"Erro ao carregar PRs salvos: {e}")
        return []
    
    def _load_saved_metrics(self):
        """Carrega métricas salvas de execução anterior."""
        try:
            metrics_file = Config.DATA_DIR / "prs_with_metrics.csv"
            if metrics_file.exists():
                df = pd.read_csv(metrics_file)
                self.logger.info(f"✓ Carregadas métricas para {len(df)} PRs")
                return df
        except Exception as e:
            self.logger.warning(f"Erro ao carregar métricas salvas: {e}")
        return None

def setup_environment():
    """Valida a configuração e inicializa o sistema de logging."""
    try:
        Config.validate_config()
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger.info("✓ Ambiente configurado e logging iniciado.")
    except ValueError as e:
        print(f"[ERRO CRÍTICO] Erro de configuração: {e}")
        sys.exit(1)