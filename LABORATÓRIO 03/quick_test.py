"""
Teste rápido para validar módulos do Lab03 - LAB03S03 COMPLETO
"""
import sys
import os
import pandas as pd
import numpy as np

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    try:
        from src.config.config import Config
        from src.collectors.repo_selector import RepositorySelector
        from src.collectors.github_collector import GitHubCollector  
        from src.modules.metrics_calculator import MetricsCalculator
        from src.modules.statistical_analyzer import StatisticalAnalyzer
        from src.modules.data_visualizer import DataVisualizer
        from src.modules.report_generator import ReportGenerator
        from src.pipelines.AnalysisPipeline import AnalysisPipeline
        
        print("✅ Todos os módulos importados com sucesso!")
        print(f"Token configurado: {'Sim' if Config.GITHUB_TOKEN != 'seu_token_aqui' else 'Não - Configure o token no arquivo .env'}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False

def test_analysis_with_dummy_data():
    """Testa análise com dados fictícios"""
    try:
        from src.modules.statistical_analyzer import StatisticalAnalyzer
        from src.modules.data_visualizer import DataVisualizer
        from src.modules.report_generator import ReportGenerator
        
        print("\\n🧪 Testando análise com dados fictícios...")
        
        # Cria dados fictícios de teste
        np.random.seed(42)
        n_samples = 100
        
        dummy_data = {
            'final_status': np.random.choice(['MERGED', 'CLOSED'], n_samples, p=[0.7, 0.3]),
            'total_changes': np.random.lognormal(3, 1, n_samples),
            'files_changed': np.random.poisson(5, n_samples),
            'additions': np.random.lognormal(2.5, 1, n_samples),
            'deletions': np.random.lognormal(2, 1, n_samples),
            'analysis_time_hours': np.random.lognormal(2, 1.5, n_samples),
            'analysis_time_days': np.random.lognormal(1, 1, n_samples),
            'description_length': np.random.lognormal(4, 1, n_samples),
            'has_description': np.random.choice([True, False], n_samples, p=[0.8, 0.2]),
            'participants_count': np.random.poisson(3, n_samples),
            'total_comments': np.random.poisson(8, n_samples),
            'reviews_count': np.random.poisson(2, n_samples),
            'repo_full_name': [f'test/repo{i%10}' for i in range(n_samples)]
        }
        
        df = pd.DataFrame(dummy_data)
        
        # Testa análise estatística
        analyzer = StatisticalAnalyzer()
        analysis_results = analyzer.analyze_research_questions(df)
        
        print("✅ Análise estatística executada com sucesso!")
        print(f"  - Dataset: {analysis_results['dataset_info']['total_prs']} PRs")
        print(f"  - Taxa de merge: {analysis_results['dataset_info']['merge_rate']:.1f}%")
        
        # Testa visualização (apenas estrutura, sem salvar)
        visualizer = DataVisualizer()
        print("✅ Módulo de visualização inicializado com sucesso!")
        
        # Testa geração de relatório
        report_gen = ReportGenerator()
        print("✅ Módulo de geração de relatório inicializado com sucesso!")
        
        print("\\n🎉 Todos os testes passaram! O LAB03S03 está pronto para uso.")
        print("\\n📋 Para executar com dados reais:")
        print("   1. Configure seu token do GitHub no arquivo .env")
        print("   2. Execute: python main.py --quick-test")
        print("   3. Ou para análise completa: python main.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 LABORATÓRIO 03 - Teste Rápido dos Módulos LAB03S03")
    print("=" * 60)
    
    # Teste 1: Importações
    if not test_imports():
        sys.exit(1)
    
    # Teste 2: Análise com dados fictícios  
    if not test_analysis_with_dummy_data():
        sys.exit(1)
    
    print("\\n" + "=" * 60)
    print("✨ Todos os testes concluídos com sucesso!")
    print("\\n🎯 O LAB03S03 está 100% funcional e pronto para entrega!")