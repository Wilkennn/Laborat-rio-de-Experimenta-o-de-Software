from src.collectors.rest_collector import RestDataCollector
from src.collectors.graphql_collector import GraphQLDataCollector
from src.modules.data_analyzer import DataAnalyzer
from src.modules.data_visualizer import DataVisualizer
from src.modules.report_generator import ReportGenerator
from src import config

def main():
    print("=====================================================")
    print("=== ANALISADOR DE REPOSITÓRIOS POPULARES DO GITHUB ===")
    print(f"=== Método de Coleta: {config.API_METHOD} ===")
    print(f"=== Repositórios: {config.TOTAL_REPOS_TO_FETCH} ===")
    print("=====================================================\n")

    # Escolhe entre GraphQL ou REST
    collector = None
    if config.API_METHOD.upper() == 'GRAPHQL':
        collector = GraphQLDataCollector()
    elif config.API_METHOD.upper() == 'REST':
        collector = RestDataCollector()
    else:
        raise ValueError(f"Método de API desconhecido: {config.API_METHOD}")

    print("--- Etapa 1: Coletando dados da API do GitHub ---")
    if collector:
        collector.run()
    print("-----------------------------------------------------\n")
    
    print("--- Etapa 2: Analisando dados coletados ---")
    analyzer = DataAnalyzer()
    try:
        results = analyzer.run_all_analyses()
<<<<<<< HEAD
        print("Análise concluída!")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        return
    print("-----------------------------------------------------\n")
    
    print("--- Etapa 3: Gerando visualizações ---")
    try:
        visualizer = DataVisualizer()
        plots = visualizer.generate_all_plots()
        print("Visualizações criadas!")
    except Exception as e:
        print(f"Erro nos gráficos: {e}")
        plots = []
    print("-----------------------------------------------------\n")
    
    print("--- Etapa 4: Gerando relatório final ---")
    try:
        report_generator = ReportGenerator(results, plots)
        report_path = report_generator.save_report()
        print("Relatório gerado!")
    except Exception as e:
        print(f"Erro no relatório: {e}")
    print("-----------------------------------------------------\n")
    
    print("PROCESSO CONCLUÍDO")
    print(f"Dados: {config.CSV_FILEPATH}")
    print(f"Gráficos: {config.PLOTS_DIR}")
    if 'report_path' in locals():
        print(f"Relatório: {report_path}")
=======
        print("✅ Análise concluída!")
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        return
    except Exception as e:
        print(f"❌ Erro durante a análise: {e}")
        return
    print("-----------------------------------------------------\n")
    

>>>>>>> 91ceb91ae7ddfbbecd6224b33ac416d27011d201

if __name__ == "__main__":
    main()