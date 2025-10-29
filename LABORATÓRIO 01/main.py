import logging
import sys
from src.collectors.rest_collector import RestDataCollector
from src.collectors.graphql_collector import GraphQLDataCollector
from src.modules.data_analyzer import DataAnalyzer
from src.modules.data_visualizer import DataVisualizer
from src.modules.report_generator import ReportGenerator
from src import config

def setup_logging():
    """Configura o sistema de logging para exibir mensagens informativas."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def select_collector():
    """Seleciona a classe do coletor de dados com base na configuração."""
    collectors = {
        'GRAPHQL': GraphQLDataCollector,
        'REST': RestDataCollector
    }
    collector_class = collectors.get(config.API_METHOD.upper())
    
    if not collector_class:
        raise ValueError(f"Método de API desconhecido ou não suportado: {config.API_METHOD}")
        
    return collector_class()

def main():
    """Orquestra o fluxo completo de coleta, análise e geração de relatório."""
    setup_logging()
    
    logging.info("=====================================================")
    logging.info("=== ANALISADOR DE REPOSITÓRIOS POPULARES DO GITHUB ===")
    logging.info(f"=== Método de Coleta: {config.API_METHOD}")
    logging.info(f"=== Repositórios: {config.TOTAL_REPOS_TO_FETCH}")
    logging.info("=====================================================\n")

    try:
        # Etapa 1: Coleta de Dados
        logging.info("--- Iniciando Etapa 1: Coleta de dados da API ---")
        collector = select_collector()
        collector.run()
        logging.info("--- Etapa 1 Concluída ---\n")

        # Etapa 2: Análise dos Dados
        logging.info("--- Iniciando Etapa 2: Análise dos dados coletados ---")
        analyzer = DataAnalyzer()
        analysis_results = analyzer.run_all_analyses()
        logging.info("--- Etapa 2 Concluída ---\n")

        # Etapa 3: Geração de Gráficos
        logging.info("--- Iniciando Etapa 3: Geração de visualizações ---")
        visualizer = DataVisualizer()
        plot_paths = visualizer.generate_all_plots()
        logging.info("--- Etapa 3 Concluída ---\n")

        # Etapa 4: Geração do Relatório
        logging.info("--- Iniciando Etapa 4: Geração do relatório final ---")
        report_generator = ReportGenerator(analysis_results, plot_paths)
        report_path = report_generator.save_report()
        logging.info("--- Etapa 4 Concluída ---\n")

        logging.info("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        logging.info(f"Dados salvos em: {config.CSV_FILEPATH}")
        logging.info(f"Gráficos salvos em: {config.PLOTS_DIR}")
        logging.info(f"Relatório final salvo em: {report_path}")

    except FileNotFoundError as e:
        logging.error(f"Erro de arquivo não encontrado: {e}. Verifique se a etapa de coleta foi executada corretamente.")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"Erro de configuração: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante a execução: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()