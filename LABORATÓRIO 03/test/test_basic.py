"""
Testes básicos para verificar funcionalidade do Lab03
"""
import sys
import os
import unittest
import logging

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config.config import Config

class TestLab03Basic(unittest.TestCase):
    """Testes básicos do Lab03"""
    
    def test_config_import(self):
        """Testa se a configuração pode ser importada"""
        self.assertIsNotNone(Config)
        self.assertIsNotNone(Config.GITHUB_API_BASE_URL)
    
    def test_directories_creation(self):
        """Testa se os diretórios necessários existem"""
        base_dir = os.path.join(os.path.dirname(__file__), '..')
        
        # Testa diretórios principais
        self.assertTrue(os.path.exists(os.path.join(base_dir, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_dir, 'output')))
        self.assertTrue(os.path.exists(os.path.join(base_dir, 'output', 'data')))
    
    def test_modules_import(self):
        """Testa se os módulos principais podem ser importados"""
        try:
            from src.collectors.repo_selector import RepositorySelector
            from src.collectors.github_collector import GitHubCollector
            from src.modules.metrics_calculator import MetricsCalculator
            
            # Testa instanciação básica (sem token)
            repo_selector = RepositorySelector(token='fake_token')
            github_collector = GitHubCollector(token='fake_token')
            metrics_calc = MetricsCalculator()
            
            self.assertIsNotNone(repo_selector)
            self.assertIsNotNone(github_collector)
            self.assertIsNotNone(metrics_calc)
            
        except ImportError as e:
            self.fail(f"Falha ao importar módulos: {e}")

if __name__ == '__main__':
    # Configura logging básico para os testes
    logging.basicConfig(level=logging.INFO)
    
    unittest.main()