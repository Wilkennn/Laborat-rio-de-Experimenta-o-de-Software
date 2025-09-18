#!/usr/bin/env python3
"""
Script de configuração inicial para o Lab 02
Análise de Qualidade de Repositórios Java
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é adequada."""
    print("🐍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def check_git():
    """Verifica se o Git está instalado."""
    print("📦 Verificando Git...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git OK: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Git não encontrado")
    print("   Instale em: https://git-scm.com/download")
    return False

def check_java():
    """Verifica se o Java está instalado."""
    print("☕ Verificando Java...")
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stderr.split('\n')[0]
            print(f"✅ Java OK: {version_line}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Java não encontrado")
    print("   Instale em: https://www.oracle.com/java/technologies/downloads/")
    return False

def install_python_dependencies():
    """Instala as dependências Python."""
    print("📚 Instalando dependências Python...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def setup_ck_tool():
    """Configura a ferramenta CK se não estiver presente."""
    print("🔧 Verificando ferramenta CK...")
    
    # Verificar se CK já existe
    default_ck_path = r"C:\Users\Nery\Desktop\ck\target\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
    if os.path.exists(default_ck_path):
        print(f"✅ CK encontrada em: {default_ck_path}")
        return True
    
    # Procurar CK em outros locais comuns
    possible_paths = [
        "ck/target/ck-*-jar-with-dependencies.jar",
        "../ck/target/ck-*-jar-with-dependencies.jar",
        "~/ck/target/ck-*-jar-with-dependencies.jar"
    ]
    
    for path_pattern in possible_paths:
        import glob
        matches = glob.glob(os.path.expanduser(path_pattern))
        if matches:
            print(f"✅ CK encontrada em: {matches[0]}")
            return True
    
    print("⚠️  Ferramenta CK não encontrada")
    print("📋 Para instalar a ferramenta CK:")
    print("   1. git clone https://github.com/mauricioaniche/ck")
    print("   2. cd ck")
    print("   3. mvn clean package")
    print("   4. O JAR estará em target/")
    
    setup_ck = input("\n❓ Deseja que eu tente baixar e compilar a CK? (s/N): ").lower().strip()
    
    if setup_ck == 's':
        try:
            print("📦 Clonando repositório CK...")
            subprocess.run(['git', 'clone', 'https://github.com/mauricioaniche/ck'], check=True)
            
            print("🔨 Compilando CK (isso pode demorar)...")
            subprocess.run(['mvn', 'clean', 'package'], cwd='ck', check=True)
            
            print("✅ CK compilada com sucesso!")
            return True
            
        except subprocess.CalledProcessError:
            print("❌ Erro ao configurar CK automaticamente")
            print("   Configure manualmente seguindo as instruções acima")
            return False
        except FileNotFoundError:
            print("❌ Maven não encontrado")
            print("   Instale Maven: https://maven.apache.org/install.html")
            return False
    
    return False

def setup_github_token():
    """Configura o token do GitHub."""
    print("🔑 Configurando token do GitHub...")
    
    env_file = Path('src/.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if 'your_github_token_here' not in content:
                print("✅ Token do GitHub já configurado")
                return True
    
    print("📋 Para continuar, você precisa de um token do GitHub:")
    print("   1. Acesse: https://github.com/settings/tokens")
    print("   2. Clique em 'Generate new token (classic)'")
    print("   3. Selecione escopo 'public_repo'")
    print("   4. Copie o token gerado")
    
    token = input("\n🔑 Cole seu token do GitHub aqui: ").strip()
    
    if not token:
        print("❌ Token não fornecido")
        return False
    
    # Testar token
    print("🔍 Testando token...")
    headers = {'Authorization': f'token {token}'}
    response = requests.get('https://api.github.com/user', headers=headers)
    
    if response.status_code == 200:
        print("✅ Token válido!")
        
        # Salvar no arquivo .env
        env_content = f"GITHUB_TOKEN={token}\nPROJECT_NAME=java-quality-analysis\nOUTPUT_DIR=output\n"
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"💾 Token salvo em: {env_file}")
        return True
    else:
        print(f"❌ Token inválido: {response.status_code}")
        return False

def create_directories():
    """Cria os diretórios necessários."""
    print("📁 Criando estrutura de diretórios...")
    
    directories = [
        'src/output/data',
        'src/output/plots',
        'temp_repos'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Diretórios criados")

def run_test():
    """Executa um teste básico."""
    print("🧪 Executando teste básico...")
    
    try:
        os.chdir('src')
        result = subprocess.run([sys.executable, 'main.py'], timeout=300, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Teste básico passou!")
            return True
        else:
            print(f"❌ Teste falhou: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Teste demorou muito (timeout 5 minutos)")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        os.chdir('..')

def main():
    """Função principal do setup."""
    print("🚀 SETUP - Lab 02: Análise de Qualidade de Repositórios Java")
    print("="*60)
    
    checks = [
        ("Python", check_python_version),
        ("Git", check_git),
        ("Java", check_java),
        ("Dependências Python", install_python_dependencies),
        ("Ferramenta CK", setup_ck_tool),
        ("Token GitHub", setup_github_token),
        ("Diretórios", create_directories),
    ]
    
    failed_checks = []
    
    for name, check_func in checks:
        try:
            if not check_func():
                failed_checks.append(name)
        except Exception as e:
            print(f"❌ Erro em {name}: {e}")
            failed_checks.append(name)
        print()
    
    print("="*60)
    
    if failed_checks:
        print("❌ SETUP INCOMPLETO")
        print("Itens que precisam de atenção:")
        for item in failed_checks:
            print(f"   • {item}")
        print("\nResolva os problemas acima e execute o setup novamente.")
    else:
        print("✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("   1. cd src")
        print("   2. python main.py        # Teste com 1 repositório")
        print("   3. python main.py --full # Coleta completa (1.000 repos)")
        
        run_test_now = input("\n❓ Executar teste agora? (s/N): ").lower().strip()
        if run_test_now == 's':
            run_test()

if __name__ == "__main__":
    main()
