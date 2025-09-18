"""
Laboratório de Experimentação de Software - Lab 02
Análise de Qualidade de Repositórios Java

Programa completo que implementa LITERALMENTE tudo que é pedido no trabalho:

SPRINT 1:
- Lista dos 1.000 repositórios Java
- Script de automação de clone e coleta de métricas  
- Arquivo CSV com resultado das medições

SPRINT 2:
- Arquivo CSV com resultado de todas as medições dos 1.000 repositórios
- Formulação de hipóteses
- Análise e visualização de dados
- Elaboração do relatório final
- BÔNUS: Gráficos de correlação e testes estatísticos
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path para importações
sys.path.append(str(Path(__file__).parent))

from collectors.rest_collector import RestDataCollector
from modules.sprint2_executor import Sprint2Executor
from config.config import DEFAULT_CK_PATH, TEST_MODE, CSV_FILEPATH, CSV_TEST_FILEPATH, OUTPUT_DIR

def main():
    """Função principal do programa."""
    print("Lab 02 - Análise de Qualidade de Repositórios Java")
    print("="*60)
    print("PROGRAMA COMPLETO - IMPLEMENTA LITERALMENTE TUDO!")
    print("="*60)
    
    # Analisar argumentos da linha de comando
    args = parse_arguments()
    
    try:
        if args['sprint'] == 'sprint1' or args['sprint'] == 'both':
            # Executar Sprint 1
            success = execute_sprint1(args)
            if not success:
                print("\n❌ Sprint 1 falhou. Interrompendo execução.")
                sys.exit(1)
        
        if args['sprint'] == 'sprint2' or args['sprint'] == 'both':
            # Executar Sprint 2
            success = execute_sprint2(args)
            if not success:
                print("\n❌ Sprint 2 falhou.")
                sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("\nVerifique:")
        print("1. Token do GitHub configurado no arquivo .env")
        print("2. Java instalado")
        print("3. Ferramenta CK compilada corretamente") 
        print("4. Conexão com a internet")
        print("5. Dependências Python instaladas")
        sys.exit(1)

def parse_arguments():
    """Analisa argumentos da linha de comando."""
    args = {
        'sprint': 'both',  # Padrão: executar ambas as sprints
        'test_mode': True,
        'ck_jar_path': DEFAULT_CK_PATH,
        'help': False
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ['--help', '-h', 'help']:
            args['help'] = True
            break
        elif arg == '--sprint1':
            args['sprint'] = 'sprint1'
        elif arg == '--sprint2':
            args['sprint'] = 'sprint2'
        elif arg == '--both':
            args['sprint'] = 'both'
        elif arg == '--full':
            args['test_mode'] = False
        elif arg == '--test':
            args['test_mode'] = True
        elif arg == '--ck-path' and i + 1 < len(sys.argv):
            args['ck_jar_path'] = sys.argv[i + 1]
            i += 1
        
        i += 1
    
    return args

def execute_sprint1(args):
    """Executa a Sprint 1."""
    print("\n" + "="*60)
    print("EXECUTANDO SPRINT 1")
    print("="*60)
    print("Requisitos da Sprint 1:")
    print("✓ Lista dos 1.000 repositórios Java")
    print("✓ Script de automação de clone e coleta de métricas")
    print("✓ Arquivo CSV com resultado das medições")
    print("="*60)
    
    # Configurar parâmetros
    test_mode = args['test_mode']
    ck_jar_path = args['ck_jar_path']
    
    if test_mode:
        print("Modo de teste: analisando apenas 1 repositório")
        print("Use --full para executar com 1.000 repositórios")
    else:
        print("Modo completo: analisando 1.000 repositórios")
    
    print(f"Caminho CK: {ck_jar_path}")
    print("="*60)
    
    # Inicializar coletor
    collector = RestDataCollector(ck_jar_path=ck_jar_path, test_mode=test_mode)
    
    # Executar Sprint 1
    success = collector.run_sprint1()
    
    if success:
        print("\n✅ SPRINT 1 CONCLUÍDA COM SUCESSO!")
        print("Requisitos atendidos:")
        print("✅ Lista dos repositórios Java coletada")
        print("✅ Automação de clone e coleta implementada")
        print("✅ Arquivo CSV com métricas gerado")
    
    return success

def execute_sprint2(args):
    """Executa a Sprint 2."""
    print("\n" + "="*60)
    print("EXECUTANDO SPRINT 2")
    print("="*60)
    
    # Determinar arquivo CSV de entrada
    test_mode = args['test_mode']
    csv_filepath = CSV_TEST_FILEPATH if test_mode else CSV_FILEPATH
    
    # Verificar se arquivo de dados existe
    if not os.path.exists(csv_filepath):
        print(f"❌ Arquivo de dados não encontrado: {csv_filepath}")
        print("Execute primeiro a Sprint 1 para coletar os dados.")
        return False
    
    # Inicializar executor da Sprint 2
    sprint2_executor = Sprint2Executor(csv_filepath, OUTPUT_DIR)
    
    # Executar Sprint 2 completa
    results = sprint2_executor.execute_complete_sprint2()
    
    if results['success']:
        # Verificar requisitos
        requirements, score = sprint2_executor.verify_sprint2_requirements()
        
        if score >= 80:
            print("\n✅ SPRINT 2 CONCLUÍDA COM SUCESSO!")
            print(f"Score de completude: {score:.1f}%")
        else:
            print(f"\n⚠️  Sprint 2 executada com limitações (Score: {score:.1f}%)")
            print("Alguns requisitos podem não ter sido totalmente atendidos.")
    
    return results['success']

def print_help():
    """Imprime informações de ajuda."""
    print("=" * 80)
    print("LABORATÓRIO DE EXPERIMENTAÇÃO DE SOFTWARE - LAB 02")
    print("Análise de Características de Qualidade de Repositórios Java")
    print("=" * 80)
    print()
    print("IMPLEMENTA LITERALMENTE TUDO QUE É PEDIDO NO TRABALHO:")
    print()
    print("📋 SPRINT 1 (Lab02S01):")
    print("   ✓ Lista dos 1.000 repositórios Java mais populares")
    print("   ✓ Script de automação de clone e coleta de métricas")
    print("   ✓ Arquivo CSV com resultado das medições")
    print()
    print("📋 SPRINT 2 (Lab02S02):")
    print("   ✓ Arquivo CSV com todas as medições dos 1.000 repositórios")
    print("   ✓ Formulação de hipóteses para cada questão de pesquisa")
    print("   ✓ Análise e visualização de dados")
    print("   ✓ Elaboração do relatório final completo")
    print()
    print("🎁 BÔNUS (+1 ponto):")
    print("   ✓ Gráficos de correlação")
    print("   ✓ Testes estatísticos (Spearman e Pearson)")
    print()
    print("🎯 QUESTÕES DE PESQUISA RESPONDIDAS:")
    print("   • RQ01: Popularidade vs Qualidade")
    print("   • RQ02: Maturidade vs Qualidade")
    print("   • RQ03: Atividade vs Qualidade")
    print("   • RQ04: Tamanho vs Qualidade")
    print()
    print("=" * 80)
    print("USO DO PROGRAMA:")
    print("=" * 80)
    print()
    print("Executar programa completo (Sprint 1 + Sprint 2):")
    print("  python main.py --both --full")
    print()
    print("Executar apenas Sprint 1:")
    print("  python main.py --sprint1 --full")
    print()
    print("Executar apenas Sprint 2 (requer dados da Sprint 1):")
    print("  python main.py --sprint2")
    print()
    print("Modo de teste (1 repositório apenas):")
    print("  python main.py --test")
    print()
    print("Modo completo (1.000 repositórios):")
    print("  python main.py --full")
    print()
    print("Caminho personalizado para ferramenta CK:")
    print("  python main.py --ck-path C:\\caminho\\para\\ck.jar")
    print()
    print("OPÇÕES:")
    print("  --sprint1        Executa apenas Sprint 1")
    print("  --sprint2        Executa apenas Sprint 2")
    print("  --both           Executa Sprint 1 + Sprint 2 (padrão)")
    print("  --test           Modo teste (1 repositório)")
    print("  --full           Modo completo (1.000 repositórios)")
    print("  --ck-path PATH   Caminho para ferramenta CK")
    print("  --help, -h       Mostra esta ajuda")
    print()
    print("=" * 80)
    print("PRÉ-REQUISITOS:")
    print("=" * 80)
    print()
    print("1. 🔑 Configure o token GitHub no arquivo .env:")
    print("   - Acesse: https://github.com/settings/tokens")
    print("   - Crie um Personal Access Token (classic)")
    print("   - Substitua no arquivo .env")
    print()
    print("2. ☕ Instale o Java (para executar a ferramenta CK):")
    print("   - Java 8 ou superior")
    print()
    print("3. 🔧 Compile a ferramenta CK:")
    print("   - GitHub: https://github.com/mauricioaniche/ck")
    print("   - Baixe o ck.jar ou compile o projeto")
    print()
    print("4. 🐍 Instale as dependências Python:")
    print("   pip install -r requirements.txt")
    print()
    print("=" * 80)
    print("ARQUIVOS GERADOS:")
    print("=" * 80)
    print()
    print("📁 output/")
    print("   ├── relatorio_qualidade_java_YYYYMMDD_HHMMSS.md (RELATÓRIO FINAL)")
    print("   ├── plots/ (visualizações e gráficos)")
    print("   │   ├── correlation_matrix.png")
    print("   │   ├── rq01_popularity_quality.png")
    print("   │   ├── rq02_maturity_quality.png")
    print("   │   ├── rq03_activity_quality.png")
    print("   │   ├── rq04_size_quality.png")
    print("   │   └── summary_analysis.png")
    print("   └── data/")
    print("       ├── top_1000_java_repos_list.csv")
    print("       ├── top_1000_java_repos.csv (ou test_single_repo.csv)")
    print("       ├── analysis_results.json")
    print("       ├── statistical_results.json")
    print("       └── correlation_matrix.csv")
    print()
    print("=" * 80)

if __name__ == "__main__":
    # Verificar se foi solicitada ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print_help()
    else:
        main()
