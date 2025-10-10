"""
Módulo para análise estatística dos dados de Pull Requests
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Tuple
from scipy.stats import pearsonr, spearmanr, kendalltau, mannwhitneyu
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

from ..config.config import Config

logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    """Classe para realizar análises estatísticas dos dados de PR"""
    
    def __init__(self):
        self.significance_level = Config.SIGNIFICANCE_LEVEL
        
    def analyze_research_questions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa todas as questões de pesquisa definidas no laboratório
        
        Args:
            df: DataFrame com os dados dos PRs e métricas calculadas
            
        Returns:
            Dicionário com resultados de todas as análises
        """
        logger.info("Iniciando análise das questões de pesquisa...")
        
        results = {
            'dataset_info': self._get_dataset_info(df),
            'rq_a_feedback': self._analyze_feedback_questions(df),
            'rq_b_reviews': self._analyze_review_count_questions(df),
            'summary_statistics': self._calculate_summary_statistics(df),
            'correlation_analysis': self._perform_correlation_analysis(df)
        }
        
        logger.info("Análise das questões de pesquisa concluída")
        return results
    
    def _get_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Informações básicas do dataset"""
        return {
            'total_prs': len(df),
            'merged_prs': len(df[df['final_status'] == 'MERGED']),
            'closed_prs': len(df[df['final_status'] == 'CLOSED']),
            'unique_repositories': df['repo_full_name'].nunique() if 'repo_full_name' in df.columns else 0,
            'date_range': {
                'start': df['created_at'].min() if 'created_at' in df.columns else None,
                'end': df['created_at'].max() if 'created_at' in df.columns else None
            },
            'merge_rate': len(df[df['final_status'] == 'MERGED']) / len(df) * 100 if len(df) > 0 else 0
        }
    
    def _analyze_feedback_questions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa questões relacionadas ao feedback final (RQ01-RQ04)
        A. Feedback Final das Revisões (Status do PR): MERGED vs CLOSED
        """
        logger.info("Analisando questões de feedback final (RQ01-RQ04)...")
        
        results = {}
        
        # RQ01: Tamanho dos PRs vs Feedback Final
        results['rq01_size_vs_feedback'] = self._analyze_size_vs_feedback(df)
        
        # RQ02: Tempo de análise vs Feedback Final  
        results['rq02_time_vs_feedback'] = self._analyze_time_vs_feedback(df)
        
        # RQ03: Descrição vs Feedback Final
        results['rq03_description_vs_feedback'] = self._analyze_description_vs_feedback(df)
        
        # RQ04: Interações vs Feedback Final
        results['rq04_interactions_vs_feedback'] = self._analyze_interactions_vs_feedback(df)
        
        return results
    
    def _analyze_review_count_questions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa questões relacionadas ao número de revisões (RQ05-RQ08)
        B. Número de Revisões
        """
        logger.info("Analisando questões de número de revisões (RQ05-RQ08)...")
        
        results = {}
        
        # RQ05: Tamanho dos PRs vs Número de revisões
        results['rq05_size_vs_reviews'] = self._analyze_size_vs_reviews(df)
        
        # RQ06: Tempo de análise vs Número de revisões
        results['rq06_time_vs_reviews'] = self._analyze_time_vs_reviews(df)
        
        # RQ07: Descrição vs Número de revisões
        results['rq07_description_vs_reviews'] = self._analyze_description_vs_reviews(df)
        
        # RQ08: Interações vs Número de revisões
        results['rq08_interactions_vs_reviews'] = self._analyze_interactions_vs_reviews(df)
        
        return results
    
    def _analyze_size_vs_feedback(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ01: Relação entre tamanho dos PRs e feedback final"""
        
        # Métricas de tamanho
        size_metrics = ['files_changed', 'additions', 'deletions', 'total_changes']
        
        results = {
            'question': 'RQ01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?',
            'metrics_analyzed': size_metrics,
            'statistical_tests': {},
            'descriptive_stats': {},
            'interpretation': ''
        }
        
        for metric in size_metrics:
            if metric in df.columns:
                # Estatísticas descritivas por status
                merged_data = df[df['final_status'] == 'MERGED'][metric].dropna()
                closed_data = df[df['final_status'] == 'CLOSED'][metric].dropna()
                
                results['descriptive_stats'][metric] = {
                    'merged': {
                        'count': len(merged_data),
                        'median': merged_data.median(),
                        'mean': merged_data.mean(),
                        'std': merged_data.std(),
                        'q25': merged_data.quantile(0.25),
                        'q75': merged_data.quantile(0.75)
                    },
                    'closed': {
                        'count': len(closed_data),
                        'median': closed_data.median(),
                        'mean': closed_data.mean(),
                        'std': closed_data.std(),
                        'q25': closed_data.quantile(0.25),
                        'q75': closed_data.quantile(0.75)
                    }
                }
                
                # Teste estatístico Mann-Whitney U (não-paramétrico)
                if len(merged_data) > 0 and len(closed_data) > 0:
                    statistic, p_value = mannwhitneyu(merged_data, closed_data, alternative='two-sided')
                    
                    results['statistical_tests'][metric] = {
                        'test': 'Mann-Whitney U',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'significant': p_value < self.significance_level,
                        'effect_size': self._calculate_effect_size_mannwhitney(merged_data, closed_data)
                    }
        
        # Interpretação geral
        results['interpretation'] = self._interpret_size_feedback_results(results)
        
        return results
    
    def _analyze_time_vs_feedback(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ02: Relação entre tempo de análise e feedback final"""
        
        time_metrics = ['analysis_time_hours', 'analysis_time_days']
        
        results = {
            'question': 'RQ02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?',
            'metrics_analyzed': time_metrics,
            'statistical_tests': {},
            'descriptive_stats': {},
            'interpretation': ''
        }
        
        for metric in time_metrics:
            if metric in df.columns:
                merged_data = df[df['final_status'] == 'MERGED'][metric].dropna()
                closed_data = df[df['final_status'] == 'CLOSED'][metric].dropna()
                
                results['descriptive_stats'][metric] = {
                    'merged': {
                        'count': len(merged_data),
                        'median': merged_data.median(),
                        'mean': merged_data.mean(),
                        'std': merged_data.std()
                    },
                    'closed': {
                        'count': len(closed_data),
                        'median': closed_data.median(),
                        'mean': closed_data.mean(),
                        'std': closed_data.std()
                    }
                }
                
                if len(merged_data) > 0 and len(closed_data) > 0:
                    statistic, p_value = mannwhitneyu(merged_data, closed_data, alternative='two-sided')
                    
                    results['statistical_tests'][metric] = {
                        'test': 'Mann-Whitney U',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'significant': p_value < self.significance_level,
                        'effect_size': self._calculate_effect_size_mannwhitney(merged_data, closed_data)
                    }
        
        results['interpretation'] = self._interpret_time_feedback_results(results)
        return results
    
    def _analyze_description_vs_feedback(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ03: Relação entre descrição e feedback final"""
        
        desc_metrics = ['description_length', 'has_description']
        
        results = {
            'question': 'RQ03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?',
            'metrics_analyzed': desc_metrics,
            'statistical_tests': {},
            'descriptive_stats': {},
            'interpretation': ''
        }
        
        # Análise do comprimento da descrição
        if 'description_length' in df.columns:
            merged_data = df[df['final_status'] == 'MERGED']['description_length'].dropna()
            closed_data = df[df['final_status'] == 'CLOSED']['description_length'].dropna()
            
            results['descriptive_stats']['description_length'] = {
                'merged': {
                    'count': len(merged_data),
                    'median': merged_data.median(),
                    'mean': merged_data.mean(),
                    'std': merged_data.std()
                },
                'closed': {
                    'count': len(closed_data),
                    'median': closed_data.median(),
                    'mean': closed_data.mean(),
                    'std': closed_data.std()
                }
            }
            
            if len(merged_data) > 0 and len(closed_data) > 0:
                statistic, p_value = mannwhitneyu(merged_data, closed_data, alternative='two-sided')
                
                results['statistical_tests']['description_length'] = {
                    'test': 'Mann-Whitney U',
                    'statistic': float(statistic),
                    'p_value': float(p_value),
                    'significant': p_value < self.significance_level
                }
        
        # Análise da presença de descrição (teste qui-quadrado)
        if 'has_description' in df.columns:
            contingency_table = pd.crosstab(df['final_status'], df['has_description'])
            
            if contingency_table.shape == (2, 2):
                chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                
                results['statistical_tests']['has_description'] = {
                    'test': 'Chi-quadrado',
                    'statistic': float(chi2),
                    'p_value': float(p_value),
                    'significant': p_value < self.significance_level,
                    'contingency_table': contingency_table.to_dict()
                }
        
        results['interpretation'] = self._interpret_description_feedback_results(results)
        return results
    
    def _analyze_interactions_vs_feedback(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ04: Relação entre interações e feedback final"""
        
        interaction_metrics = ['participants_count', 'comments_count', 'review_comments_count', 'total_comments']
        
        results = {
            'question': 'RQ04: Qual a relação entre as interações nos PRs e o feedback final das revisões?',
            'metrics_analyzed': interaction_metrics,
            'statistical_tests': {},
            'descriptive_stats': {},
            'interpretation': ''
        }
        
        for metric in interaction_metrics:
            if metric in df.columns:
                merged_data = df[df['final_status'] == 'MERGED'][metric].dropna()
                closed_data = df[df['final_status'] == 'CLOSED'][metric].dropna()
                
                results['descriptive_stats'][metric] = {
                    'merged': {
                        'count': len(merged_data),
                        'median': merged_data.median(),
                        'mean': merged_data.mean(),
                        'std': merged_data.std()
                    },
                    'closed': {
                        'count': len(closed_data),
                        'median': closed_data.median(),
                        'mean': closed_data.mean(),
                        'std': closed_data.std()
                    }
                }
                
                if len(merged_data) > 0 and len(closed_data) > 0:
                    statistic, p_value = mannwhitneyu(merged_data, closed_data, alternative='two-sided')
                    
                    results['statistical_tests'][metric] = {
                        'test': 'Mann-Whitney U',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'significant': p_value < self.significance_level
                    }
        
        results['interpretation'] = self._interpret_interactions_feedback_results(results)
        return results
    
    def _analyze_size_vs_reviews(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ05: Relação entre tamanho e número de revisões"""
        
        size_metrics = ['files_changed', 'total_changes', 'additions', 'deletions']
        
        results = {
            'question': 'RQ05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?',
            'correlations': {},
            'interpretation': ''
        }
        
        for metric in size_metrics:
            if metric in df.columns and 'reviews_count' in df.columns:
                # Remove outliers para correlação mais robusta
                clean_df = self._remove_outliers(df, [metric, 'reviews_count'])
                
                if len(clean_df) > 10:  # Mínimo de dados para correlação confiável
                    # Correlação de Spearman (não-paramétrica)
                    corr_spearman, p_spearman = spearmanr(clean_df[metric], clean_df['reviews_count'])
                    
                    # Correlação de Pearson
                    corr_pearson, p_pearson = pearsonr(clean_df[metric], clean_df['reviews_count'])
                    
                    results['correlations'][metric] = {
                        'spearman': {
                            'correlation': float(corr_spearman),
                            'p_value': float(p_spearman),
                            'significant': p_spearman < self.significance_level
                        },
                        'pearson': {
                            'correlation': float(corr_pearson),
                            'p_value': float(p_pearson),
                            'significant': p_pearson < self.significance_level
                        },
                        'sample_size': len(clean_df)
                    }
        
        results['interpretation'] = self._interpret_size_reviews_results(results)
        return results
    
    def _analyze_time_vs_reviews(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ06: Relação entre tempo de análise e número de revisões"""
        
        results = {
            'question': 'RQ06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?',
            'correlations': {},
            'interpretation': ''
        }
        
        if 'analysis_time_hours' in df.columns and 'reviews_count' in df.columns:
            clean_df = self._remove_outliers(df, ['analysis_time_hours', 'reviews_count'])
            
            if len(clean_df) > 10:
                corr_spearman, p_spearman = spearmanr(clean_df['analysis_time_hours'], clean_df['reviews_count'])
                corr_pearson, p_pearson = pearsonr(clean_df['analysis_time_hours'], clean_df['reviews_count'])
                
                results['correlations']['analysis_time_hours'] = {
                    'spearman': {
                        'correlation': float(corr_spearman),
                        'p_value': float(p_spearman),
                        'significant': p_spearman < self.significance_level
                    },
                    'pearson': {
                        'correlation': float(corr_pearson),
                        'p_value': float(p_pearson),
                        'significant': p_pearson < self.significance_level
                    },
                    'sample_size': len(clean_df)
                }
        
        results['interpretation'] = self._interpret_time_reviews_results(results)
        return results
    
    def _analyze_description_vs_reviews(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ07: Relação entre descrição e número de revisões"""
        
        results = {
            'question': 'RQ07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?',
            'correlations': {},
            'group_analysis': {},
            'interpretation': ''
        }
        
        if 'description_length' in df.columns and 'reviews_count' in df.columns:
            clean_df = self._remove_outliers(df, ['description_length', 'reviews_count'])
            
            if len(clean_df) > 10:
                corr_spearman, p_spearman = spearmanr(clean_df['description_length'], clean_df['reviews_count'])
                
                results['correlations']['description_length'] = {
                    'spearman': {
                        'correlation': float(corr_spearman),
                        'p_value': float(p_spearman),
                        'significant': p_spearman < self.significance_level
                    },
                    'sample_size': len(clean_df)
                }
        
        # Análise por grupos (com/sem descrição)
        if 'has_description' in df.columns and 'reviews_count' in df.columns:
            with_desc = df[df['has_description'] == True]['reviews_count'].dropna()
            without_desc = df[df['has_description'] == False]['reviews_count'].dropna()
            
            if len(with_desc) > 0 and len(without_desc) > 0:
                statistic, p_value = mannwhitneyu(with_desc, without_desc, alternative='two-sided')
                
                results['group_analysis']['has_description'] = {
                    'with_description': {
                        'count': len(with_desc),
                        'median': with_desc.median(),
                        'mean': with_desc.mean()
                    },
                    'without_description': {
                        'count': len(without_desc),
                        'median': without_desc.median(),
                        'mean': without_desc.mean()
                    },
                    'statistical_test': {
                        'test': 'Mann-Whitney U',
                        'statistic': float(statistic),
                        'p_value': float(p_value),
                        'significant': p_value < self.significance_level
                    }
                }
        
        results['interpretation'] = self._interpret_description_reviews_results(results)
        return results
    
    def _analyze_interactions_vs_reviews(self, df: pd.DataFrame) -> Dict[str, Any]:
        """RQ08: Relação entre interações e número de revisões"""
        
        interaction_metrics = ['participants_count', 'total_comments']
        
        results = {
            'question': 'RQ08: Qual a relação entre as interações nos PRs e o número de revisões realizadas?',
            'correlations': {},
            'interpretation': ''
        }
        
        for metric in interaction_metrics:
            if metric in df.columns and 'reviews_count' in df.columns:
                clean_df = self._remove_outliers(df, [metric, 'reviews_count'])
                
                if len(clean_df) > 10:
                    corr_spearman, p_spearman = spearmanr(clean_df[metric], clean_df['reviews_count'])
                    
                    results['correlations'][metric] = {
                        'spearman': {
                            'correlation': float(corr_spearman),
                            'p_value': float(p_spearman),
                            'significant': p_spearman < self.significance_level
                        },
                        'sample_size': len(clean_df)
                    }
        
        results['interpretation'] = self._interpret_interactions_reviews_results(results)
        return results
    
    def _perform_correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Análise geral de correlações entre todas as métricas"""
        
        # Métricas numéricas para correlação
        numeric_metrics = [
            'files_changed', 'total_changes', 'additions', 'deletions',
            'analysis_time_hours', 'description_length',
            'participants_count', 'total_comments', 'reviews_count'
        ]
        
        # Filtra apenas colunas que existem
        available_metrics = [col for col in numeric_metrics if col in df.columns]
        
        if len(available_metrics) < 2:
            return {'error': 'Métricas insuficientes para análise de correlação'}
        
        # Matriz de correlação
        correlation_data = df[available_metrics].dropna()
        
        if len(correlation_data) < 10:
            return {'error': 'Dados insuficientes para análise de correlação'}
        
        # Correlação de Spearman (mais robusta para dados não-normais)
        corr_matrix_spearman = correlation_data.corr(method='spearman')
        
        # Correlação de Pearson
        corr_matrix_pearson = correlation_data.corr(method='pearson')
        
        return {
            'spearman_matrix': corr_matrix_spearman.to_dict(),
            'pearson_matrix': corr_matrix_pearson.to_dict(),
            'metrics_analyzed': available_metrics,
            'sample_size': len(correlation_data)
        }
    
    def _calculate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcula estatísticas resumo do dataset"""
        
        summary = {}
        
        # Métricas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_cols:
            if col in df.columns and not df[col].isna().all():
                data = df[col].dropna()
                if len(data) > 0:
                    summary[col] = {
                        'count': len(data),
                        'mean': float(data.mean()),
                        'median': float(data.median()),
                        'std': float(data.std()),
                        'min': float(data.min()),
                        'max': float(data.max()),
                        'q25': float(data.quantile(0.25)),
                        'q75': float(data.quantile(0.75))
                    }
        
        return summary
    
    # Métodos auxiliares para interpretação
    def _interpret_size_feedback_results(self, results: Dict) -> str:
        interpretation = "Análise da relação entre tamanho dos PRs e feedback final:\n"
        
        for metric, test_result in results.get('statistical_tests', {}).items():
            if test_result['significant']:
                interpretation += f"- {metric}: Diferença estatisticamente significante (p={test_result['p_value']:.4f})\n"
            else:
                interpretation += f"- {metric}: Sem diferença estatisticamente significante (p={test_result['p_value']:.4f})\n"
        
        return interpretation
    
    def _interpret_time_feedback_results(self, results: Dict) -> str:
        interpretation = "Análise da relação entre tempo de análise e feedback final:\n"
        
        for metric, test_result in results.get('statistical_tests', {}).items():
            if test_result['significant']:
                interpretation += f"- {metric}: Diferença estatisticamente significante (p={test_result['p_value']:.4f})\n"
            else:
                interpretation += f"- {metric}: Sem diferença estatisticamente significante (p={test_result['p_value']:.4f})\n"
        
        return interpretation
    
    def _interpret_description_feedback_results(self, results: Dict) -> str:
        return "Análise da relação entre descrição dos PRs e feedback final realizada."
    
    def _interpret_interactions_feedback_results(self, results: Dict) -> str:
        return "Análise da relação entre interações nos PRs e feedback final realizada."
    
    def _interpret_size_reviews_results(self, results: Dict) -> str:
        interpretation = "Análise da correlação entre tamanho dos PRs e número de revisões:\n"
        
        for metric, corr_data in results.get('correlations', {}).items():
            spearman_corr = corr_data['spearman']['correlation']
            spearman_sig = corr_data['spearman']['significant']
            
            strength = self._interpret_correlation_strength(abs(spearman_corr))
            direction = "positiva" if spearman_corr > 0 else "negativa"
            
            interpretation += f"- {metric}: Correlação {direction} {strength} "
            interpretation += f"(ρ={spearman_corr:.3f}, {'significante' if spearman_sig else 'não significante'})\n"
        
        return interpretation
    
    def _interpret_time_reviews_results(self, results: Dict) -> str:
        return "Análise da correlação entre tempo de análise e número de revisões realizada."
    
    def _interpret_description_reviews_results(self, results: Dict) -> str:
        return "Análise da correlação entre descrição e número de revisões realizada."
    
    def _interpret_interactions_reviews_results(self, results: Dict) -> str:
        return "Análise da correlação entre interações e número de revisões realizada."
    
    def _interpret_correlation_strength(self, corr_value: float) -> str:
        """Interpreta a força de uma correlação"""
        if corr_value < 0.1:
            return "muito fraca"
        elif corr_value < 0.3:
            return "fraca"
        elif corr_value < 0.5:
            return "moderada"
        elif corr_value < 0.7:
            return "forte"
        else:
            return "muito forte"
    
    def _remove_outliers(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Remove outliers usando método IQR"""
        clean_df = df.copy()
        
        for col in columns:
            if col in clean_df.columns:
                Q1 = clean_df[col].quantile(0.25)
                Q3 = clean_df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                clean_df = clean_df[(clean_df[col] >= lower_bound) & (clean_df[col] <= upper_bound)]
        
        return clean_df
    
    def _calculate_effect_size_mannwhitney(self, group1: pd.Series, group2: pd.Series) -> float:
        """Calcula tamanho do efeito para teste Mann-Whitney U"""
        n1, n2 = len(group1), len(group2)
        
        # Rank-biserial correlation como medida de tamanho do efeito
        combined = pd.concat([group1, group2])
        ranks = combined.rank()
        
        sum_ranks_group1 = ranks[:n1].sum()
        
        # Fórmula para rank-biserial correlation
        U1 = sum_ranks_group1 - n1 * (n1 + 1) / 2
        effect_size = (2 * U1) / (n1 * n2) - 1
        
        return float(abs(effect_size))