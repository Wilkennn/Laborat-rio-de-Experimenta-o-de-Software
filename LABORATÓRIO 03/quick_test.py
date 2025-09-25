"""
Script de exemplo para execução rápida da Sprint 1
Configurado para coletar apenas alguns repositórios para teste
"""
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config.config import Config
from src.collectors.repo_selector import RepositorySelector
import logging

# Configura logging básico
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def quick_test():
    """Teste rápido da seleção de repositórios"""
    
    logger.info("=== TESTE RÁPIDO - LAB03 SPRINT 1 ===")
    
    # Verifica se token está configurado
    if not Config.GITHUB_TOKEN:
        logger.warning("⚠️  GITHUB_TOKEN não configurado!")
        logger.info("Para usar o script:")
        logger.info("1. Crie um arquivo .env baseado no .env.example")
        logger.info("2. Configure seu token do GitHub")
        logger.info("3. Execute novamente")
        return False
    
    try:
        # Cria diretórios necessários
        Config.validate_config()
        
        # Inicializa seletor
        repo_selector = RepositorySelector()
        
        # Busca apenas 10 repositórios populares (teste rápido)
        logger.info("Buscando 10 repositórios mais populares...")
        top_repos = repo_selector.get_top_repositories(count=10)
        
        if top_repos:
            logger.info(f"✓ {len(top_repos)} repositórios encontrados:")
            for i, repo in enumerate(top_repos):
                logger.info(f"  {i+1}. {repo['full_name']} ({repo['stars']} stars)")
            
            # Salva resultado
            filepath = repo_selector.save_repositories(top_repos, "test_repositories.csv")
            logger.info(f"✓ Dados salvos em: {filepath}")
            
            logger.info("✓ Teste concluído com sucesso!")
            return True
        else:
            logger.error("✗ Nenhum repositório encontrado")
            return False
            
    except Exception as e:
        logger.error(f"✗ Erro no teste: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Tudo funcionando! Agora você pode executar:")
        print("   python main.py --max-repos 5")
    else:
        print("\n❌ Verifique a configuração e tente novamente.")