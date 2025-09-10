"""
Laboratório de Experimentação de Software - Lab 02
Análise de Qualidade de Repositórios Java
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path para importações
sys.path.append(str(Path(__file__).parent))

from collectors.rest_collector import RestDataCollector
from config.config import DEFAULT_CK_PATH, TEST_MODE

def main():
    """Função principal do programa."""
    print("Lab 02 - Análise de Qualidade de Repositórios Java")
    print("="*50)
    
    # Verificar modo de execução
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        test_mode = False
        print("Executando modo completo: 1.000 repositórios")
    else:
        test_mode = True
        print("Executando modo de teste: 1 repositório")
        print("Use --full para executar com 1.000 repositórios")
    
    print("="*50)
    
    try:
        # Verificar caminho do CK
        if len(sys.argv) > 2:
            ck_jar_path = sys.argv[2]
            print(f"Usando caminho personalizado para CK: {ck_jar_path}")
        else:
            ck_jar_path = DEFAULT_CK_PATH
            print(f"Usando caminho padrão para CK: {ck_jar_path}")
        
        # Inicializar coletor
        collector = RestDataCollector(ck_jar_path=ck_jar_path, test_mode=test_mode)
        
        # Executar Sprint 1
        success = collector.run_sprint1()
        
        if success:
            print("\nPrograma executado com sucesso!")
        else:
            print("\nErro na execução do programa")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("\nVerifique:")
        print("1. Token do GitHub configurado no arquivo .env")
        print("2. Java instalado")
        print("3. Ferramenta CK compilada corretamente")
        print("4. Conexão com a internet")
        sys.exit(1)

def print_help():
    """Imprime informações de ajuda."""
    print("Uso do programa:")
    print("  python main.py                    # Modo de teste (1 repositório)")
    print("  python main.py --full             # Modo completo (1.000 repositórios)")
    print("  python main.py --full <ck_path>   # Modo completo com caminho CK personalizado")
    print("\nPré-requisitos:")
    print("1. Configure o token GitHub no arquivo .env")
    print("2. Instale o Java (para executar a ferramenta CK)")
    print("3. Compile a ferramenta CK: https://github.com/mauricioaniche/ck")
    print("4. Instale as dependências Python: pip install -r requirements.txt")

if __name__ == "__main__":
    # Verificar se foi solicitada ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print_help()
    else:
        main()
