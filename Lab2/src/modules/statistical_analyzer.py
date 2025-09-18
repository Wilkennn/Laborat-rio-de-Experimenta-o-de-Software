"""
Módulo de Análise Estatística Avançada - Lab 02
Responsável por testes estatísticos avançados, validação de hipóteses
e análises de confiança estatística.
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import spearmanr, pearsonr, kendalltau, shapiro, normaltest
import warnings
warnings.filterwarnings('ignore')


class StatisticalAnalyzer:
    """Classe para análises estatísticas avançadas."""
    
    def __init__(self, dataframe):
        """
        Inicializa o analisador estatístico.
        
        Args:
            dataframe: DataFrame com os dados dos repositórios
        """
        self.df = dataframe
        self.statistical_results = {}
        self.significance_level = 0.05
        
    def perform_comprehensive_analysis(self):
        """Realiza análise estatística completa."""
        print("\nExecutando análise estatística avançada...")
        print("=" * 50)
        
        results = {
            'normality_tests': self._test_normality(),
            'correlation_analysis': self._comprehensive_correlation_analysis(),
            'hypothesis_testing': self._test_research_hypotheses(),
            'effect_size_analysis': self._calculate_effect_sizes(),
            'outlier_analysis': self._analyze_outliers(),
            'statistical_summary': self._generate_statistical_summary()
        }
        
        self.statistical_results = results
        return results
    
    def _test_normality(self):
        """Testa normalidade das variáveis usando múltiplos testes."""
        print("Testando normalidade das variáveis...")
        
        metrics = [
            'stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years',
            'loc_total', 'classes_count', 'methods_count',
            'cbo_avg', 'dit_avg', 'lcom_avg'
        ]
        
        normality_results = {}
        
        for metric in metrics:
            if metric in self.df.columns:
                data = self.df[metric].dropna()
                
                if len(data) > 8:  # Mínimo para testes
                    # Teste de Shapiro-Wilk (para n < 5000)
                    if len(data) < 5000:
                        shapiro_stat, shapiro_p = shapiro(data)
                    else:
                        shapiro_stat, shapiro_p = None, None
                    
                    # Teste de D'Agostino-Pearson
                    dagostino_stat, dagostino_p = normaltest(data)
                    
                    normality_results[metric] = {
                        'sample_size': len(data),
                        'shapiro_wilk': {
                            'statistic': shapiro_stat,
                            'p_value': shapiro_p,
                            'is_normal': shapiro_p > self.significance_level if shapiro_p else None
                        },
                        'dagostino_pearson': {
                            'statistic': dagostino_stat,
                            'p_value': dagostino_p,
                            'is_normal': dagostino_p > self.significance_level
                        },
                        'recommended_test': 'non_parametric' if (shapiro_p and shapiro_p < self.significance_level) or dagostino_p < self.significance_level else 'parametric'
                    }
        
        return normality_results
    
    def _comprehensive_correlation_analysis(self):
        """Análise de correlação usando múltiplos métodos."""
        print("Analisando correlações com múltiplos métodos...")
        
        # Definir pares de variáveis para análise baseados nas RQs
        variable_pairs = [
            # RQ01: Popularidade vs Qualidade
            ('stars', 'cbo_avg'), ('stars', 'dit_avg'), ('stars', 'lcom_avg'),
            ('forks', 'cbo_avg'), ('forks', 'dit_avg'), ('forks', 'lcom_avg'),
            # RQ02: Maturidade vs Qualidade  
            ('age_years', 'cbo_avg'), ('age_years', 'dit_avg'), ('age_years', 'lcom_avg'),
            # RQ03: Atividade vs Qualidade
            ('releases', 'cbo_avg'), ('releases', 'dit_avg'), ('releases', 'lcom_avg'),
            ('contributors', 'cbo_avg'), ('contributors', 'dit_avg'), ('contributors', 'lcom_avg'),
            # RQ04: Tamanho vs Qualidade
            ('loc_total', 'cbo_avg'), ('loc_total', 'dit_avg'), ('loc_total', 'lcom_avg'),
            ('classes_count', 'cbo_avg'), ('classes_count', 'dit_avg'), ('classes_count', 'lcom_avg')
        ]
        
        correlation_results = {}
        
        for var1, var2 in variable_pairs:
            if var1 in self.df.columns and var2 in self.df.columns:
                data = self.df[[var1, var2]].dropna()
                
                if len(data) >= 10:  # Mínimo para análise confiável
                    pair_key = f"{var1}_vs_{var2}"
                    
                    # Pearson (paramétrico)
                    pearson_corr, pearson_p = pearsonr(data[var1], data[var2])
                    
                    # Spearman (não-paramétrico)
                    spearman_corr, spearman_p = spearmanr(data[var1], data[var2])
                    
                    # Kendall Tau (não-paramétrico, robusto a outliers)
                    kendall_corr, kendall_p = kendalltau(data[var1], data[var2])
                    
                    correlation_results[pair_key] = {
                        'sample_size': len(data),
                        'pearson': {
                            'correlation': round(pearson_corr, 4),
                            'p_value': round(pearson_p, 4),
                            'significant': pearson_p < self.significance_level,
                            'interpretation': self._interpret_correlation(pearson_corr)
                        },
                        'spearman': {
                            'correlation': round(spearman_corr, 4),
                            'p_value': round(spearman_p, 4),
                            'significant': spearman_p < self.significance_level,
                            'interpretation': self._interpret_correlation(spearman_corr)
                        },
                        'kendall': {
                            'correlation': round(kendall_corr, 4),
                            'p_value': round(kendall_p, 4),
                            'significant': kendall_p < self.significance_level,
                            'interpretation': self._interpret_correlation(kendall_corr)
                        },
                        'recommended_method': self._recommend_correlation_method(data[var1], data[var2])
                    }
        
        return correlation_results
    
    def _test_research_hypotheses(self):
        """Testa as hipóteses específicas de cada questão de pesquisa."""
        print("Testando hipóteses das questões de pesquisa...")
        
        hypothesis_results = {}
        
        # RQ01: Popularidade → Melhor Qualidade (correlação negativa com CBO, DIT, LCOM)
        rq01_results = self._test_hypothesis_rq01()
        hypothesis_results['RQ01'] = rq01_results
        
        # RQ02: Maturidade → Qualidade Estabilizada
        rq02_results = self._test_hypothesis_rq02()
        hypothesis_results['RQ02'] = rq02_results
        
        # RQ03: Atividade → Melhor Qualidade
        rq03_results = self._test_hypothesis_rq03()
        hypothesis_results['RQ03'] = rq03_results
        
        # RQ04: Tamanho → Pior Qualidade (correlação positiva com CBO, DIT, LCOM)
        rq04_results = self._test_hypothesis_rq04()
        hypothesis_results['RQ04'] = rq04_results
        
        return hypothesis_results
    
    def _test_hypothesis_rq01(self):
        """Testa hipótese RQ01: Popularidade vs Qualidade."""
        results = {
            'hypothesis': 'Repositórios mais populares têm melhor qualidade (menor CBO, DIT, LCOM)',
            'tests': {},
            'conclusion': '',
            'confidence': 0
        }
        
        popularity_metrics = ['stars', 'forks']
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
        
        significant_negative_correlations = 0
        total_tests = 0
        
        for pop_metric in popularity_metrics:
            for qual_metric in quality_metrics:
                if pop_metric in self.df.columns and qual_metric in self.df.columns:
                    data = self.df[[pop_metric, qual_metric]].dropna()
                    
                    if len(data) >= 10:
                        corr, p_value = spearmanr(data[pop_metric], data[qual_metric])
                        
                        test_key = f"{pop_metric}_vs_{qual_metric}"
                        results['tests'][test_key] = {
                            'correlation': round(corr, 4),
                            'p_value': round(p_value, 4),
                            'significant': p_value < self.significance_level,
                            'supports_hypothesis': corr < 0 and p_value < self.significance_level
                        }
                        
                        total_tests += 1
                        if corr < 0 and p_value < self.significance_level:
                            significant_negative_correlations += 1
        
        if total_tests > 0:
            confidence = significant_negative_correlations / total_tests
            results['confidence'] = round(confidence, 3)
            
            if confidence >= 0.6:
                results['conclusion'] = 'Hipótese CONFIRMADA: Evidências suportam que popularidade está associada à melhor qualidade'
            elif confidence >= 0.3:
                results['conclusion'] = 'Hipótese PARCIALMENTE CONFIRMADA: Algumas evidências suportam a relação'
            else:
                results['conclusion'] = 'Hipótese REJEITADA: Evidências não suportam a relação esperada'
        
        return results
    
    def _test_hypothesis_rq02(self):
        """Testa hipótese RQ02: Maturidade vs Qualidade."""
        results = {
            'hypothesis': 'Repositórios mais maduros têm qualidade estabilizada (correlações moderadas)',
            'tests': {},
            'conclusion': '',
            'confidence': 0
        }
        
        if 'age_years' in self.df.columns:
            quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
            moderate_correlations = 0
            total_tests = 0
            
            for qual_metric in quality_metrics:
                if qual_metric in self.df.columns:
                    data = self.df[['age_years', qual_metric]].dropna()
                    
                    if len(data) >= 10:
                        corr, p_value = spearmanr(data['age_years'], data[qual_metric])
                        
                        test_key = f"age_vs_{qual_metric}"
                        results['tests'][test_key] = {
                            'correlation': round(corr, 4),
                            'p_value': round(p_value, 4),
                            'significant': p_value < self.significance_level,
                            'supports_hypothesis': abs(corr) > 0.1 and abs(corr) < 0.5  # Correlação moderada
                        }
                        
                        total_tests += 1
                        if abs(corr) > 0.1 and abs(corr) < 0.5:
                            moderate_correlations += 1
            
            if total_tests > 0:
                confidence = moderate_correlations / total_tests
                results['confidence'] = round(confidence, 3)
                
                if confidence >= 0.6:
                    results['conclusion'] = 'Hipótese CONFIRMADA: Maturidade mostra relacionamento moderado com qualidade'
                else:
                    results['conclusion'] = 'Hipótese REJEITADA: Maturidade não mostra relacionamento esperado'
        
        return results
    
    def _test_hypothesis_rq03(self):
        """Testa hipótese RQ03: Atividade vs Qualidade."""
        results = {
            'hypothesis': 'Repositórios mais ativos têm melhor qualidade (menor CBO, DIT, LCOM)',
            'tests': {},
            'conclusion': '',
            'confidence': 0
        }
        
        activity_metrics = ['releases', 'contributors']
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
        
        significant_negative_correlations = 0
        total_tests = 0
        
        for act_metric in activity_metrics:
            for qual_metric in quality_metrics:
                if act_metric in self.df.columns and qual_metric in self.df.columns:
                    data = self.df[[act_metric, qual_metric]].dropna()
                    
                    if len(data) >= 10:
                        corr, p_value = spearmanr(data[act_metric], data[qual_metric])
                        
                        test_key = f"{act_metric}_vs_{qual_metric}"
                        results['tests'][test_key] = {
                            'correlation': round(corr, 4),
                            'p_value': round(p_value, 4),
                            'significant': p_value < self.significance_level,
                            'supports_hypothesis': corr < 0 and p_value < self.significance_level
                        }
                        
                        total_tests += 1
                        if corr < 0 and p_value < self.significance_level:
                            significant_negative_correlations += 1
        
        if total_tests > 0:
            confidence = significant_negative_correlations / total_tests
            results['confidence'] = round(confidence, 3)
            
            if confidence >= 0.5:
                results['conclusion'] = 'Hipótese CONFIRMADA: Atividade está associada à melhor qualidade'
            else:
                results['conclusion'] = 'Hipótese REJEITADA: Atividade não está associada à melhor qualidade'
        
        return results
    
    def _test_hypothesis_rq04(self):
        """Testa hipótese RQ04: Tamanho vs Qualidade."""
        results = {
            'hypothesis': 'Repositórios maiores têm pior qualidade (maior CBO, DIT, LCOM)',
            'tests': {},
            'conclusion': '',
            'confidence': 0
        }
        
        size_metrics = ['loc_total', 'classes_count', 'methods_count']
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
        
        significant_positive_correlations = 0
        total_tests = 0
        
        for size_metric in size_metrics:
            for qual_metric in quality_metrics:
                if size_metric in self.df.columns and qual_metric in self.df.columns:
                    data = self.df[[size_metric, qual_metric]].dropna()
                    
                    if len(data) >= 10:
                        corr, p_value = spearmanr(data[size_metric], data[qual_metric])
                        
                        test_key = f"{size_metric}_vs_{qual_metric}"
                        results['tests'][test_key] = {
                            'correlation': round(corr, 4),
                            'p_value': round(p_value, 4),
                            'significant': p_value < self.significance_level,
                            'supports_hypothesis': corr > 0 and p_value < self.significance_level
                        }
                        
                        total_tests += 1
                        if corr > 0 and p_value < self.significance_level:
                            significant_positive_correlations += 1
        
        if total_tests > 0:
            confidence = significant_positive_correlations / total_tests
            results['confidence'] = round(confidence, 3)
            
            if confidence >= 0.5:
                results['conclusion'] = 'Hipótese CONFIRMADA: Tamanho está associado à pior qualidade'
            else:
                results['conclusion'] = 'Hipótese REJEITADA: Tamanho não está associado à pior qualidade'
        
        return results
    
    def _calculate_effect_sizes(self):
        """Calcula tamanhos de efeito para as correlações significativas."""
        print("Calculando tamanhos de efeito...")
        
        effect_sizes = {}
        
        # Para correlações, o próprio coeficiente é o tamanho do efeito
        # Interpretação: 0.1 = pequeno, 0.3 = médio, 0.5 = grande
        
        if hasattr(self, 'statistical_results') and 'correlation_analysis' in self.statistical_results:
            for pair, corr_data in self.statistical_results['correlation_analysis'].items():
                spearman_corr = corr_data['spearman']['correlation']
                
                effect_sizes[pair] = {
                    'effect_size': abs(spearman_corr),
                    'interpretation': self._interpret_effect_size(abs(spearman_corr)),
                    'direction': 'positive' if spearman_corr > 0 else 'negative',
                    'magnitude': abs(spearman_corr)
                }
        
        return effect_sizes
    
    def _analyze_outliers(self):
        """Identifica e analisa outliers nas variáveis principais."""
        print("Analisando outliers...")
        
        metrics = ['stars', 'forks', 'age_years', 'loc_total', 'cbo_avg', 'dit_avg', 'lcom_avg']
        outlier_analysis = {}
        
        for metric in metrics:
            if metric in self.df.columns:
                data = self.df[metric].dropna()
                
                if len(data) > 10:
                    # Método IQR
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = data[(data < lower_bound) | (data > upper_bound)]
                    
                    # Z-score method
                    z_scores = np.abs(stats.zscore(data))
                    z_outliers = data[z_scores > 3]
                    
                    outlier_analysis[metric] = {
                        'total_observations': len(data),
                        'iqr_outliers': {
                            'count': len(outliers),
                            'percentage': round(len(outliers) / len(data) * 100, 2),
                            'values': outliers.tolist()[:10]  # Primeiros 10
                        },
                        'zscore_outliers': {
                            'count': len(z_outliers),
                            'percentage': round(len(z_outliers) / len(data) * 100, 2)
                        },
                        'bounds': {
                            'iqr_lower': round(lower_bound, 3),
                            'iqr_upper': round(upper_bound, 3)
                        }
                    }
        
        return outlier_analysis
    
    def _generate_statistical_summary(self):
        """Gera resumo estatístico geral."""
        return {
            'sample_size': len(self.df),
            'significance_level': self.significance_level,
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'key_findings': self._extract_key_findings()
        }
    
    def _extract_key_findings(self):
        """Extrai os principais achados estatísticos."""
        findings = []
        
        if hasattr(self, 'statistical_results'):
            # Analisar correlações significativas
            if 'correlation_analysis' in self.statistical_results:
                significant_correlations = []
                for pair, data in self.statistical_results['correlation_analysis'].items():
                    if data['spearman']['significant'] and abs(data['spearman']['correlation']) > 0.3:
                        significant_correlations.append({
                            'pair': pair,
                            'correlation': data['spearman']['correlation'],
                            'interpretation': data['spearman']['interpretation']
                        })
                
                if significant_correlations:
                    findings.append(f"Encontradas {len(significant_correlations)} correlações significativas e moderadas/fortes")
                    
                    # Correlação mais forte
                    strongest = max(significant_correlations, key=lambda x: abs(x['correlation']))
                    findings.append(f"Correlação mais forte: {strongest['pair']} ({strongest['correlation']:.3f})")
        
        return findings
    
    def _interpret_correlation(self, correlation):
        """Interpreta o valor da correlação."""
        abs_corr = abs(correlation)
        if abs_corr < 0.1:
            return 'negligível'
        elif abs_corr < 0.3:
            return 'fraca'
        elif abs_corr < 0.5:
            return 'moderada'
        elif abs_corr < 0.7:
            return 'forte'
        else:
            return 'muito forte'
    
    def _interpret_effect_size(self, effect_size):
        """Interpreta o tamanho do efeito."""
        if effect_size < 0.1:
            return 'negligível'
        elif effect_size < 0.3:
            return 'pequeno'
        elif effect_size < 0.5:
            return 'médio'
        else:
            return 'grande'
    
    def _recommend_correlation_method(self, x, y):
        """Recomenda o método de correlação mais apropriado."""
        # Teste de normalidade simples
        try:
            _, p_x = normaltest(x)
            _, p_y = normaltest(y)
            
            if p_x > 0.05 and p_y > 0.05:
                return 'pearson'  # Ambas normais
            else:
                return 'spearman'  # Pelo menos uma não-normal
        except:
            return 'spearman'  # Padrão seguro
    
    def export_statistical_results(self, output_file):
        """Exporta resultados estatísticos para arquivo JSON."""
        import json
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.statistical_results, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados estatísticos exportados para: {output_file}")
        return output_file
