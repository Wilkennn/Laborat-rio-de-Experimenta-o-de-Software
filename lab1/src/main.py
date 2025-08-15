# Importa os módulos que contêm a lógica principal
from src import data_collector
from src import data_analyzer
from src import config

def main():
    """
    Ponto de entrada principal da aplicação.
    Orquestra a coleta e a análise dos dados dos repositórios do GitHub.
    """
    # Imprime um cabeçalho para o usuário
    print("=====================================================")
    print("=== ANALISADOR DE REPOSITÓRIOS POPULARES DO GITHUB ===")
    print("=====================================================\n")

    # --- Etapa 1: Coleta de Dados ---
    print("--- Etapa 1: Coletando dados da API do GitHub ---")
    data_collector.collect_and_save_data()
    print("-----------------------------------------------------\n")

    # # --- Etapa 2: Análise dos Dados ---
    # print("--- Etapa 2: Analisando dados e gerando gráficos ---")
    # data_analyzer.run_analysis()
    # print("-----------------------------------------------------\n")

    # # --- Finalização ---
    # print("=====================================================")
    # print("===          PROCESSO FINALIZADO COM SUCESSO          ===")
    # print(f"Os dados foram salvos em: {config.CSV_FILEPATH}")
    # print(f"Os gráficos foram salvos no diretório: {config.PLOTS_DIR}")
    # print("=====================================================")


if __name__ == "__main__":
    main()