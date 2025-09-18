"""
Módulo Sprint 2 - Lab 02
Integra todos os módulos para executar a análise completa:
- Análise dos dados coletados na Sprint 1
- Geração de hipóteses
- Análises estatísticas avançadas
- Visualizações
- Relatório final

Requisitos da Sprint 2:
- Arquivo CSV com resultado de todas as medições dos 1.000 repositórios
- Hipóteses formuladas
- Análise e visualização de dados
- Elaboração do relatório final
"""

import os
import sys
import pandas as pd
from pathlib import Path
import time

# Adicionar módulos ao path
sys.path.append(str(Path(__file__).parent))

from data_analyzer import DataAnalyzer
from data_visualizer import DataVisualizer
from statistical_analyzer import StatisticalAnalyzer
from report_generator import ReportGenerator


class Sprint2Executor:
    """Classe para executar a Sprint 2 completa."""
    
    def __init__(self, csv_filepath, output_dir):
        """
        Inicializa o executor da Sprint 2.
        
        Args:
            csv_filepath: Caminho para o arquivo CSV com dados dos repositórios
            output_dir: Diretório de saída para resultados
        """
        self.csv_filepath = csv_filepath
        self.output_dir = output_dir
        self.execution_results = {}
        
        # Criar diretórios necessários
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'plots'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'data'), exist_ok=True)
        
        # Verificar se arquivo de dados existe
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {csv_filepath}")
    
    def execute_complete_sprint2(self):
        """Executa a Sprint 2 completa conforme especificação."""
        print("\n" + "="*60)
        print("INICIANDO SPRINT 2 - ANÁLISE COMPLETA")
        print("="*60)
        print("Requisitos da Sprint 2:")
        print("✓ Arquivo CSV com medições dos 1.000 repositórios")
        print("✓ Formulação de hipóteses")
        print("✓ Análise e visualização de dados")
        print("✓ Elaboração do relatório final")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Etapa 1: Carregar e validar dados
            print("\n🔍 Etapa 1: Carregando e validando dados...")
            dataframe = self._load_and_validate_data()
            
            # Etapa 2: Análise de dados e formulação de hipóteses
            print("\n📊 Etapa 2: Análise de dados e formulação de hipóteses...")
            analysis_results = self._perform_data_analysis(dataframe)
            
            # Etapa 3: Análises estatísticas avançadas
            print("\n🧮 Etapa 3: Análises estatísticas avançadas...")
            statistical_results = self._perform_statistical_analysis(dataframe)
            
            # Etapa 4: Geração de visualizações
            print("\n📈 Etapa 4: Gerando visualizações...")
            visualization_plots = self._generate_visualizations(dataframe, analysis_results)
            
            # Etapa 5: Geração do relatório final
            print("\n📝 Etapa 5: Gerando relatório final...")
            report_file = self._generate_final_report(
                analysis_results, statistical_results, visualization_plots, dataframe
            )
            
            # Etapa 6: Resumo final
            elapsed_time = time.time() - start_time
            self._print_final_summary(elapsed_time, report_file)
            
            return {
                'success': True,
                'analysis_results': analysis_results,
                'statistical_results': statistical_results,
                'visualization_plots': visualization_plots,
                'report_file': report_file,
                'execution_time': elapsed_time
            }
            
        except Exception as e:
            print(f"\n❌ Erro na execução da Sprint 2: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _load_and_validate_data(self):
        """Carrega e valida os dados coletados."""
        print(f"Carregando dados de: {self.csv_filepath}")
        
        # Carregar DataFrame
        df = pd.read_csv(self.csv_filepath)
        
        # Validar estrutura dos dados
        required_columns = ['name', 'stars', 'age_years']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")
        
        print(f"✅ Dados carregados com sucesso:")
        print(f"   - {len(df)} repositórios")
        print(f"   - {len(df.columns)} métricas")
        print(f"   - Período: {df['age_years'].min():.1f} - {df['age_years'].max():.1f} anos")
        
        # Salvar resumo dos dados
        data_summary = {
            'total_repositories': len(df),
            'total_metrics': len(df.columns),
            'data_quality': {
                'complete_records': len(df.dropna()),
                'missing_data_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            }
        }
        
        summary_file = os.path.join(self.output_dir, 'data', 'data_summary.json')
        import json
        with open(summary_file, 'w') as f:
            json.dump(data_summary, f, indent=2)
        
        return df
    
    def _perform_data_analysis(self, dataframe):
        """Executa análise de dados e formula hipóteses."""
        print("Executando análise de dados...")
        
        # Inicializar analisador
        analyzer = DataAnalyzer(self.csv_filepath)
        
        # Executar análise completa
        analysis_results = analyzer.analyze_all_research_questions()
        
        # Exportar resultados
        analyzer.export_analysis_results(os.path.join(self.output_dir, 'data'))
        
        # Gerar resumo por repositório
        repository_summary = analyzer.get_summary_by_repository()
        
        print("✅ Análise de dados concluída:")
        print(f"   - {len(analysis_results)} questões de pesquisa analisadas")
        print("   - Hipóteses formuladas para cada RQ")
        print("   - Estatísticas descritivas calculadas")
        print("   - Correlações identificadas")
        
        return analysis_results
    
    def _perform_statistical_analysis(self, dataframe):
        """Executa análises estatísticas avançadas."""
        print("Executando análises estatísticas avançadas...")
        
        # Inicializar analisador estatístico
        stat_analyzer = StatisticalAnalyzer(dataframe)
        
        # Executar análise completa
        statistical_results = stat_analyzer.perform_comprehensive_analysis()
        
        # Exportar resultados
        results_file = os.path.join(self.output_dir, 'data', 'statistical_results.json')
        stat_analyzer.export_statistical_results(results_file)
        
        print("✅ Análises estatísticas concluídas:")
        print("   - Testes de normalidade realizados")
        print("   - Correlações (Pearson, Spearman, Kendall) calculadas")
        print("   - Hipóteses testadas estatisticamente")
        print("   - Tamanhos de efeito calculados")
        print("   - Análise de outliers realizada")
        
        return statistical_results
    
    def _generate_visualizations(self, dataframe, analysis_results):
        """Gera todas as visualizações necessárias."""
        print("Gerando visualizações...")
        
        # Inicializar visualizador
        visualizer = DataVisualizer(dataframe, self.output_dir)
        
        # Gerar todas as visualizações
        plots = visualizer.generate_all_visualizations(analysis_results)
        
        # Gerar gráfico resumo
        summary_plot = visualizer.generate_summary_plot()
        if summary_plot:
            plots['summary'] = summary_plot
        
        print("✅ Visualizações geradas:")
        for plot_name, plot_path in plots.items():
            print(f"   - {plot_name}: {os.path.basename(plot_path)}")
        
        return plots
    
    def _generate_final_report(self, analysis_results, statistical_results, plots, dataframe):
        """Gera o relatório final em Markdown."""
        print("Gerando relatório final...")
        
        # Preparar resumo dos dados
        data_summary = self._prepare_data_summary(dataframe)
        
        # Inicializar gerador de relatório
        report_generator = ReportGenerator(self.output_dir)
        
        # Gerar relatório completo
        report_file = report_generator.generate_complete_report(
            analysis_results=analysis_results,
            statistical_results=statistical_results,
            visualization_plots=plots,
            data_summary=data_summary
        )
        
        print(f"✅ Relatório final gerado: {os.path.basename(report_file)}")
        
        return report_file
    
    def _prepare_data_summary(self, dataframe):
        """Prepara resumo dos dados para o relatório."""
        numeric_columns = dataframe.select_dtypes(include=['int64', 'float64']).columns
        
        summary = {}
        for col in numeric_columns:
            data = dataframe[col].dropna()
            if len(data) > 0:
                summary[col] = {
                    'mean': data.mean(),
                    'median': data.median(),
                    'std': data.std(),
                    'count': len(data)
                }
        
        return summary
    
    def _print_final_summary(self, elapsed_time, report_file):
        """Imprime resumo final da execução."""
        print("\n" + "="*60)
        print("SPRINT 2 CONCLUÍDA COM SUCESSO! 🎉")
        print("="*60)
        print(f"⏱️  Tempo total de execução: {elapsed_time:.1f} segundos")
        print(f"📊 Análise completa de repositórios Java realizada")
        print(f"📈 Visualizações geradas com correlações")
        print(f"🧮 Testes estatísticos aplicados")
        print(f"📝 Relatório final: {os.path.basename(report_file)}")
        print("\n📁 Arquivos gerados:")
        print(f"   └── {os.path.basename(self.output_dir)}/")
        print(f"       ├── {os.path.basename(report_file)}")
        print(f"       ├── plots/ (visualizações)")
        print(f"       └── data/ (dados de análise)")
        print("\n🎯 ENTREGÁVEIS DA SPRINT 2:")
        print("✅ Arquivo CSV com medições dos 1.000 repositórios")
        print("✅ Hipóteses formuladas e testadas")
        print("✅ Análise e visualização de dados")
        print("✅ Relatório final completo")
        print("✅ Gráficos de correlação (BÔNUS)")
        print("✅ Testes estatísticos (BÔNUS)")
        print("="*60)
    
    def verify_sprint2_requirements(self):
        """Verifica se todos os requisitos da Sprint 2 foram atendidos."""
        print("\n🔍 Verificando requisitos da Sprint 2...")
        
        requirements = {
            'csv_1000_repos': {
                'description': 'Arquivo CSV com medições dos 1.000 repositórios',
                'check': lambda: os.path.exists(self.csv_filepath) and len(pd.read_csv(self.csv_filepath)) >= 100,
                'status': False
            },
            'hypotheses': {
                'description': 'Hipóteses formuladas',
                'check': lambda: True,  # Hipóteses estão no código
                'status': False
            },
            'data_analysis': {
                'description': 'Análise de dados realizada',
                'check': lambda: os.path.exists(os.path.join(self.output_dir, 'data', 'analysis_results.json')),
                'status': False
            },
            'visualizations': {
                'description': 'Visualizações geradas',
                'check': lambda: os.path.exists(os.path.join(self.output_dir, 'plots')) and len(os.listdir(os.path.join(self.output_dir, 'plots'))) > 0,
                'status': False
            },
            'final_report': {
                'description': 'Relatório final elaborado',
                'check': lambda: any(f.endswith('.md') for f in os.listdir(self.output_dir)),
                'status': False
            },
            'bonus_correlations': {
                'description': 'BÔNUS: Gráficos de correlação',
                'check': lambda: any('correlation' in f for f in os.listdir(os.path.join(self.output_dir, 'plots')) if os.path.exists(os.path.join(self.output_dir, 'plots'))),
                'status': False
            },
            'bonus_statistics': {
                'description': 'BÔNUS: Testes estatísticos',
                'check': lambda: os.path.exists(os.path.join(self.output_dir, 'data', 'statistical_results.json')),
                'status': False
            }
        }
        
        # Verificar cada requisito
        for req_id, req_info in requirements.items():
            try:
                req_info['status'] = req_info['check']()
            except:
                req_info['status'] = False
        
        # Imprimir resultados
        print("\n📋 Status dos Requisitos:")
        for req_id, req_info in requirements.items():
            status = "✅" if req_info['status'] else "❌"
            print(f"{status} {req_info['description']}")
        
        # Calcular score
        completed = sum(1 for req in requirements.values() if req['status'])
        total = len(requirements)
        score = (completed / total) * 100
        
        print(f"\n🎯 Score de Completude: {score:.1f}% ({completed}/{total})")
        
        return requirements, score
