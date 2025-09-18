"""
Módulo de Análise de Dados - Lab 02
Responsável por responder às questões de pesquisa do laboratório:
- RQ01: Relação entre popularidade e qualidade
- RQ02: Relação entre maturidade e qualidade  
- RQ03: Relação entre atividade e qualidade
- RQ04: Relação entre tamanho e qualidade
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import os


class DataAnalyzer:
    """Classe para análise estatística dos dados coletados."""
    
    def __init__(self, csv_filepath):
        """
        Inicializa o analisador com o arquivo CSV de dados.
        
        Args:
            csv_filepath: Caminho para o arquivo CSV com os dados dos repositórios
        """
        self.csv_filepath = csv_filepath
        self.df = None
        self.analysis_results = {}
        self.hypotheses = {}
        
        # Carregar dados
        self._load_data()
        
        # Definir hipóteses
        self._define_hypotheses()
    
    def _load_data(self):
        """Carrega e prepara os dados para análise."""
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {self.csv_filepath}")
        
        self.df = pd.read_csv(self.csv_filepath)
        print(f"Dados carregados: {len(self.df)} repositórios")
        
        # Limpar dados e tratar valores ausentes
        self._clean_data()
    
    def _clean_data(self):
        """Limpa e prepara os dados para análise."""
        # Substituir valores NaN por 0 nas métricas numéricas
        numeric_columns = [
            'stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years',
            'loc_total', 'loc_comments_total', 'classes_count', 'methods_count',
            'cbo_avg', 'cbo_max', 'dit_avg', 'dit_max', 'lcom_avg', 'lcom_max',
            'wmc_avg', 'noc_avg', 'cc_avg'
        ]
        
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        
        # Remover repositórios com dados muito incompletos
        quality_cols = ['cbo_avg', 'dit_avg', 'lcom_avg']
        valid_repos = self.df[quality_cols].sum(axis=1) > 0
        self.df = self.df[valid_repos].copy()
        
        print(f"Repositórios válidos após limpeza: {len(self.df)}")
    
    def _define_hypotheses(self):
        """Define as hipóteses informais para cada questão de pesquisa."""
        self.hypotheses = {
            'RQ01': {
                'question': 'Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?',
                'hypothesis': 'Repositórios mais populares (mais estrelas) tendem a ter melhor qualidade de código, '
                            'com menor acoplamento (CBO), menor profundidade de herança (DIT) e maior coesão (menor LCOM).',
                'variables': {
                    'independent': ['stars', 'forks', 'watchers'],
                    'dependent': ['cbo_avg', 'dit_avg', 'lcom_avg']
                }
            },
            'RQ02': {
                'question': 'Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?',
                'hypothesis': 'Repositórios mais maduros (mais antigos) tendem a ter qualidade mais estabilizada, '
                            'com métricas de qualidade em níveis intermediários devido ao refatoramento ao longo do tempo.',
                'variables': {
                    'independent': ['age_years'],
                    'dependent': ['cbo_avg', 'dit_avg', 'lcom_avg']
                }
            },
            'RQ03': {
                'question': 'Qual a relação entre a atividade dos repositórios e as suas características de qualidade?',
                'hypothesis': 'Repositórios mais ativos (mais releases e contribuidores) tendem a ter melhor qualidade '
                            'devido à revisão contínua e melhoria incremental do código.',
                'variables': {
                    'independent': ['releases', 'contributors'],
                    'dependent': ['cbo_avg', 'dit_avg', 'lcom_avg']
                }
            },
            'RQ04': {
                'question': 'Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?',
                'hypothesis': 'Repositórios maiores (mais LOC e classes) tendem a ter pior qualidade devido à '
                            'complexidade inerente de sistemas grandes, com maior acoplamento e menor coesão.',
                'variables': {
                    'independent': ['loc_total', 'classes_count', 'methods_count'],
                    'dependent': ['cbo_avg', 'dit_avg', 'lcom_avg']
                }
            }
        }
    
    def analyze_all_research_questions(self):
        """Executa análise completa para todas as questões de pesquisa."""
        print("\nIniciando análise das questões de pesquisa")
        print("=" * 50)
        
        for rq_id in ['RQ01', 'RQ02', 'RQ03', 'RQ04']:
            print(f"\nAnalisando {rq_id}...")
            self.analysis_results[rq_id] = self._analyze_research_question(rq_id)
        
        print("\nAnálise concluída para todas as questões!")
        return self.analysis_results
    
    def _analyze_research_question(self, rq_id):
        """Analisa uma questão de pesquisa específica."""
        rq_data = self.hypotheses[rq_id]
        independent_vars = rq_data['variables']['independent']
        dependent_vars = rq_data['variables']['dependent']
        
        results = {
            'question': rq_data['question'],
            'hypothesis': rq_data['hypothesis'],
            'descriptive_stats': {},
            'correlations': {},
            'statistical_tests': {}
        }
        
        # Estatísticas descritivas
        all_vars = independent_vars + dependent_vars
        for var in all_vars:
            if var in self.df.columns:
                results['descriptive_stats'][var] = self._calculate_descriptive_stats(var)
        
        # Análise de correlação
        for indep_var in independent_vars:
            for dep_var in dependent_vars:
                if indep_var in self.df.columns and dep_var in self.df.columns:
                    correlation_key = f"{indep_var}_vs_{dep_var}"
                    results['correlations'][correlation_key] = self._calculate_correlation(indep_var, dep_var)
        
        return results
    
    def _calculate_descriptive_stats(self, variable):
        """Calcula estatísticas descritivas para uma variável."""
        data = self.df[variable].dropna()
        
        if len(data) == 0:
            return {'error': 'Sem dados válidos'}
        
        return {
            'count': len(data),
            'mean': round(data.mean(), 3),
            'median': round(data.median(), 3),
            'std': round(data.std(), 3),
            'min': round(data.min(), 3),
            'max': round(data.max(), 3),
            'q25': round(data.quantile(0.25), 3),
            'q75': round(data.quantile(0.75), 3)
        }
    
    def _calculate_correlation(self, var1, var2):
        """Calcula correlação entre duas variáveis."""
        # Remover valores ausentes
        data = self.df[[var1, var2]].dropna()
        
        if len(data) < 10:  # Mínimo de 10 observações
            return {'error': 'Dados insuficientes para correlação'}
        
        x = data[var1]
        y = data[var2]
        
        # Correlação de Pearson (linear)
        pearson_corr, pearson_p = stats.pearsonr(x, y)
        
        # Correlação de Spearman (monotônica)
        spearman_corr, spearman_p = stats.spearmanr(x, y)
        
        return {
            'sample_size': len(data),
            'pearson': {
                'correlation': round(pearson_corr, 4),
                'p_value': round(pearson_p, 4),
                'significant': pearson_p < 0.05
            },
            'spearman': {
                'correlation': round(spearman_corr, 4),
                'p_value': round(spearman_p, 4),
                'significant': spearman_p < 0.05
            }
        }
    
    def get_summary_by_repository(self):
        """Retorna sumarização dos dados por repositório conforme solicitado."""
        if self.df is None or self.df.empty:
            return None
        
        # Métricas de processo
        process_metrics = ['stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years']
        
        # Métricas de qualidade
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'loc_total', 'classes_count', 'methods_count']
        
        summary = {}
        
        # Sumarização por repositório (média, mediana, desvio padrão)
        for metric in process_metrics + quality_metrics:
            if metric in self.df.columns:
                data = self.df[metric].dropna()
                summary[metric] = {
                    'mean': round(data.mean(), 3),
                    'median': round(data.median(), 3),
                    'std': round(data.std(), 3),
                    'count': len(data)
                }
        
        return summary
    
    def get_correlation_matrix(self):
        """Gera matriz de correlação entre todas as métricas."""
        # Selecionar métricas numéricas relevantes
        metrics = [
            'stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years',
            'loc_total', 'classes_count', 'methods_count',
            'cbo_avg', 'dit_avg', 'lcom_avg'
        ]
        
        # Filtrar apenas colunas que existem
        available_metrics = [m for m in metrics if m in self.df.columns]
        
        if not available_metrics:
            return None
        
        # Calcular matriz de correlação
        correlation_data = self.df[available_metrics].corr()
        
        return correlation_data
    
    def interpret_results(self):
        """Interpreta os resultados das análises."""
        interpretations = {}
        
        for rq_id, results in self.analysis_results.items():
            interpretation = {
                'hypothesis_confirmed': [],
                'hypothesis_rejected': [],
                'key_findings': [],
                'unexpected_results': []
            }
            
            # Analisar correlações significativas
            for corr_key, corr_data in results['correlations'].items():
                if 'error' not in corr_data:
                    # Verificar significância estatística
                    if corr_data['spearman']['significant']:
                        correlation = corr_data['spearman']['correlation']
                        vars_pair = corr_key.replace('_vs_', ' vs ')
                        
                        if abs(correlation) > 0.3:  # Correlação moderada ou forte
                            finding = f"Correlação significativa entre {vars_pair}: {correlation:.3f}"
                            interpretation['key_findings'].append(finding)
                            
                            # Verificar se confirma ou rejeita hipótese
                            if self._correlation_supports_hypothesis(rq_id, corr_key, correlation):
                                interpretation['hypothesis_confirmed'].append(finding)
                            else:
                                interpretation['hypothesis_rejected'].append(finding)
            
            interpretations[rq_id] = interpretation
        
        return interpretations
    
    def _correlation_supports_hypothesis(self, rq_id, correlation_key, correlation_value):
        """Verifica se a correlação suporta a hipótese da questão de pesquisa."""
        # Lógica simplificada para determinar se a correlação suporta a hipótese
        
        if rq_id == 'RQ01':  # Popularidade vs Qualidade
            # Esperamos correlação negativa com CBO/DIT/LCOM (menor = melhor)
            if any(metric in correlation_key for metric in ['cbo', 'dit', 'lcom']):
                return correlation_value < 0
        
        elif rq_id == 'RQ02':  # Maturidade vs Qualidade
            # Relacionamento complexo, aceitar correlações moderadas
            return abs(correlation_value) > 0.2
        
        elif rq_id == 'RQ03':  # Atividade vs Qualidade
            # Esperamos correlação negativa com CBO/DIT/LCOM
            if any(metric in correlation_key for metric in ['cbo', 'dit', 'lcom']):
                return correlation_value < 0
        
        elif rq_id == 'RQ04':  # Tamanho vs Qualidade
            # Esperamos correlação positiva com CBO/DIT/LCOM (maior tamanho = pior qualidade)
            if any(metric in correlation_key for metric in ['cbo', 'dit', 'lcom']):
                return correlation_value > 0
        
        return False
    
    def export_analysis_results(self, output_dir):
        """Exporta os resultados da análise para arquivos."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar resultados completos em JSON
        import json
        results_file = os.path.join(output_dir, 'analysis_results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)
        
        # Salvar resumo por repositório
        summary = self.get_summary_by_repository()
        if summary:
            summary_file = os.path.join(output_dir, 'repository_summary.json')
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Salvar matriz de correlação
        correlation_matrix = self.get_correlation_matrix()
        if correlation_matrix is not None:
            correlation_file = os.path.join(output_dir, 'correlation_matrix.csv')
            correlation_matrix.to_csv(correlation_file)
        
        print(f"Resultados exportados para: {output_dir}")
        return {
            'results_file': results_file,
            'summary_file': summary_file if summary else None,
            'correlation_file': correlation_file if correlation_matrix is not None else None
        }
