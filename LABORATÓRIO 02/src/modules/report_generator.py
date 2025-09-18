"""
Módulo de Geração de Relatório - Lab 02
Responsável por gerar o relatório final em Markdown com todos os resultados,
análises e visualizações conforme especificado no laboratório.
"""

import os
import json
from datetime import datetime
import pandas as pd


class ReportGenerator:
    """Classe para geração do relatório final em Markdown."""
    
    def __init__(self, output_dir):
        """
        Inicializa o gerador de relatório.
        
        Args:
            output_dir: Diretório onde o relatório será salvo
        """
        self.output_dir = output_dir
        self.report_content = []
        self.timestamp = datetime.now()
        
        # Criar diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_complete_report(self, analysis_results, statistical_results, 
                               visualization_plots, data_summary):
        """
        Gera o relatório completo conforme especificação do laboratório.
        
        Args:
            analysis_results: Resultados da análise de dados
            statistical_results: Resultados dos testes estatísticos
            visualization_plots: Caminhos dos gráficos gerados
            data_summary: Resumo dos dados coletados
        """
        print("\nGerando relatório final...")
        print("=" * 30)
        
        # Inicializar conteúdo
        self.report_content = []
        
        # Estrutura do relatório conforme especificação
        self._add_header()
        self._add_introduction_and_hypotheses(analysis_results)
        self._add_methodology()
        self._add_results_by_research_question(analysis_results, statistical_results, visualization_plots)
        self._add_discussion(analysis_results, statistical_results)
        self._add_conclusions()
        self._add_appendices(data_summary, visualization_plots)
        
        # Salvar relatório
        report_filename = os.path.join(self.output_dir, f'relatorio_qualidade_java_{self.timestamp.strftime("%Y%m%d_%H%M%S")}.md')
        self._save_report(report_filename)
        
        print(f"Relatório gerado: {report_filename}")
        return report_filename
    
    def _add_header(self):
        """Adiciona cabeçalho do relatório."""
        self.report_content.extend([
            "# Análise de Características de Qualidade de Repositórios Java",
            "",
            "**Laboratório de Experimentação de Software - Lab 02**",
            "",
            f"**Data:** {self.timestamp.strftime('%d de %B de %Y')}",
            "",
            f"**Gerado em:** {self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')}",
            "",
            "---",
            ""
        ])
    
    def _add_introduction_and_hypotheses(self, analysis_results):
        """Adiciona introdução e hipóteses informais."""
        self.report_content.extend([
            "## 1. Introdução",
            "",
            "Este relatório apresenta uma análise abrangente das características de qualidade de software ",
            "em repositórios Java populares do GitHub. O objetivo é investigar como fatores do processo ",
            "de desenvolvimento se relacionam com métricas de qualidade de código obtidas através da ",
            "ferramenta CK (Chidamber & Kemerer).",
            "",
            "### 1.1 Contexto",
            "",
            "No desenvolvimento de software open-source, onde múltiplos desenvolvedores contribuem ",
            "colaborativamente, é crucial entender como características do processo de desenvolvimento ",
            "impactam na qualidade interna do código. Este estudo analisa repositórios Java populares ",
            "para identificar padrões e correlações entre métricas de processo e qualidade.",
            "",
            "### 1.2 Hipóteses Informais",
            "",
            "Antes da análise, estabelecemos as seguintes hipóteses informais:",
            ""
        ])
        
        # Adicionar hipóteses de cada RQ
        if analysis_results:
            for rq_id in ['RQ01', 'RQ02', 'RQ03', 'RQ04']:
                if rq_id in analysis_results:
                    hypothesis_data = analysis_results[rq_id]
                    self.report_content.extend([
                        f"**{rq_id}:** {hypothesis_data.get('hypothesis', 'Hipótese não definida')}",
                        ""
                    ])
        
        self.report_content.extend([
            "---",
            ""
        ])
    
    def _add_methodology(self):
        """Adiciona seção de metodologia."""
        self.report_content.extend([
            "## 2. Metodologia",
            "",
            "### 2.1 Seleção de Repositórios",
            "",
            "Foram selecionados os top-1.000 repositórios Java mais populares do GitHub, ordenados ",
            "por número de estrelas. Os critérios de seleção incluíram:",
            "",
            "- Linguagem principal: Java",
            "- Mínimo de 100 estrelas",
            "- Repositórios ativos e acessíveis",
            "",
            "### 2.2 Coleta de Dados",
            "",
            "#### 2.2.1 Métricas de Processo",
            "",
            "Coletadas através da API REST do GitHub:",
            "",
            "- **Popularidade:** Número de estrelas, forks e watchers",
            "- **Maturidade:** Idade do repositório em anos",
            "- **Atividade:** Número de releases e contribuidores",
            "- **Tamanho:** Linhas de código (LOC) e número de classes",
            "",
            "#### 2.2.2 Métricas de Qualidade",
            "",
            "Obtidas através da ferramenta CK (Chidamber & Kemerer):",
            "",
            "- **CBO (Coupling Between Objects):** Acoplamento entre objetos",
            "- **DIT (Depth of Inheritance Tree):** Profundidade da árvore de herança",
            "- **LCOM (Lack of Cohesion of Methods):** Falta de coesão entre métodos",
            "",
            "### 2.3 Análise Estatística",
            "",
            "A análise incluiu:",
            "",
            "- Estatísticas descritivas (média, mediana, desvio padrão)",
            "- Análise de correlação (Pearson e Spearman)",
            "- Testes de significância estatística (α = 0.05)",
            "- Análise de normalidade e outliers",
            "",
            "---",
            ""
        ])
    
    def _add_results_by_research_question(self, analysis_results, statistical_results, plots):
        """Adiciona resultados para cada questão de pesquisa."""
        self.report_content.extend([
            "## 3. Resultados",
            ""
        ])
        
        # RQ01: Popularidade vs Qualidade
        self._add_rq_results("RQ01", "Popularidade e Qualidade", analysis_results, statistical_results, plots)
        
        # RQ02: Maturidade vs Qualidade
        self._add_rq_results("RQ02", "Maturidade e Qualidade", analysis_results, statistical_results, plots)
        
        # RQ03: Atividade vs Qualidade
        self._add_rq_results("RQ03", "Atividade e Qualidade", analysis_results, statistical_results, plots)
        
        # RQ04: Tamanho vs Qualidade
        self._add_rq_results("RQ04", "Tamanho e Qualidade", analysis_results, statistical_results, plots)
        
        self.report_content.extend([
            "---",
            ""
        ])
    
    def _add_rq_results(self, rq_id, title, analysis_results, statistical_results, plots):
        """Adiciona resultados para uma questão de pesquisa específica."""
        self.report_content.extend([
            f"### 3.{rq_id[-1]} {rq_id}: {title}",
            ""
        ])
        
        # Questão de pesquisa
        if analysis_results and rq_id in analysis_results:
            rq_data = analysis_results[rq_id]
            question = rq_data.get('question', 'Questão não definida')
            self.report_content.extend([
                f"**Questão:** {question}",
                ""
            ])
            
            # Estatísticas descritivas
            if 'descriptive_stats' in rq_data:
                self.report_content.extend([
                    "#### Estatísticas Descritivas",
                    ""
                ])
                
                self._add_descriptive_stats_table(rq_data['descriptive_stats'])
            
            # Análise de correlação
            if 'correlations' in rq_data:
                self.report_content.extend([
                    "#### Análise de Correlação",
                    ""
                ])
                
                self._add_correlation_results(rq_data['correlations'])
        
        # Resultados dos testes estatísticos
        if statistical_results and 'hypothesis_testing' in statistical_results:
            hypothesis_results = statistical_results['hypothesis_testing']
            if rq_id in hypothesis_results:
                self.report_content.extend([
                    "#### Teste de Hipótese",
                    ""
                ])
                
                rq_hypothesis = hypothesis_results[rq_id]
                conclusion = rq_hypothesis.get('conclusion', 'Conclusão não disponível')
                confidence = rq_hypothesis.get('confidence', 0)
                
                self.report_content.extend([
                    f"**Conclusão:** {conclusion}",
                    "",
                    f"**Confiança:** {confidence:.1%}",
                    ""
                ])
        
        # Visualização
        rq_plot_key = f"rq{rq_id[-2:].lower()}_"
        matching_plots = [plot for plot_name, plot in plots.items() if rq_plot_key in plot_name]
        
        if matching_plots:
            plot_path = matching_plots[0]
            plot_filename = os.path.basename(plot_path)
            self.report_content.extend([
                "#### Visualização",
                "",
                f"![{title}](plots/{plot_filename})",
                ""
            ])
        
        self.report_content.append("")
    
    def _add_descriptive_stats_table(self, stats_data):
        """Adiciona tabela com estatísticas descritivas."""
        self.report_content.extend([
            "| Métrica | N | Média | Mediana | Desvio Padrão | Mín | Máx |",
            "|---------|---|-------|---------|---------------|-----|-----|"
        ])
        
        for metric, stats in stats_data.items():
            if 'error' not in stats:
                metric_label = self._get_metric_label(metric)
                self.report_content.append(
                    f"| {metric_label} | {stats['count']} | {stats['mean']:.2f} | "
                    f"{stats['median']:.2f} | {stats['std']:.2f} | {stats['min']:.2f} | {stats['max']:.2f} |"
                )
        
        self.report_content.append("")
    
    def _add_correlation_results(self, correlations):
        """Adiciona resultados de correlação."""
        significant_correlations = []
        
        for corr_key, corr_data in correlations.items():
            if 'error' not in corr_data:
                spearman = corr_data['spearman']
                if spearman['significant']:
                    significant_correlations.append((corr_key, spearman))
        
        if significant_correlations:
            self.report_content.extend([
                "**Correlações Significativas (Spearman, p < 0.05):**",
                ""
            ])
            
            for corr_key, spearman in significant_correlations:
                vars_pair = corr_key.replace('_vs_', ' vs ').replace('_', ' ').title()
                correlation = spearman['correlation']
                p_value = spearman['p_value']
                
                direction = "positiva" if correlation > 0 else "negativa"
                strength = self._interpret_correlation_strength(abs(correlation))
                
                self.report_content.append(
                    f"- **{vars_pair}:** r = {correlation:.3f} (p = {p_value:.3f}) - "
                    f"Correlação {direction} {strength}"
                )
            
            self.report_content.append("")
        else:
            self.report_content.extend([
                "Nenhuma correlação significativa foi encontrada.",
                ""
            ])
    
    def _add_discussion(self, analysis_results, statistical_results):
        """Adiciona seção de discussão."""
        self.report_content.extend([
            "## 4. Discussão",
            "",
            "### 4.1 Análise das Hipóteses",
            ""
        ])
        
        # Analisar cada hipótese
        if statistical_results and 'hypothesis_testing' in statistical_results:
            for rq_id, hypothesis_result in statistical_results['hypothesis_testing'].items():
                conclusion = hypothesis_result.get('conclusion', '')
                confidence = hypothesis_result.get('confidence', 0)
                
                self.report_content.extend([
                    f"**{rq_id}:** {conclusion} (Confiança: {confidence:.1%})",
                    ""
                ])
        
        self.report_content.extend([
            "### 4.2 Principais Descobertas",
            ""
        ])
        
        # Extrair principais descobertas
        key_findings = self._extract_key_findings(analysis_results, statistical_results)
        for finding in key_findings:
            self.report_content.extend([
                f"- {finding}",
                ""
            ])
        
        self.report_content.extend([
            "### 4.3 Limitações do Estudo",
            "",
            "- **Representatividade:** Análise limitada aos repositórios Java mais populares",
            "- **Métricas:** Foco em métricas CK tradicionais, não cobrindo aspectos modernos",
            "- **Causalidade:** Correlações não implicam relações causais",
            "- **Temporalidade:** Análise de momento específico, não evolutiva",
            "",
            "### 4.4 Implicações Práticas",
            "",
            "Os resultados sugerem diretrizes para desenvolvimento de software de qualidade:",
            "",
            "- Monitoramento contínuo de métricas de acoplamento e coesão",
            "- Balanceamento entre funcionalidade e qualidade estrutural",
            "- Importância da revisão de código em projetos colaborativos",
            "",
            "---",
            ""
        ])
    
    def _add_conclusions(self):
        """Adiciona seção de conclusões."""
        self.report_content.extend([
            "## 5. Conclusões",
            "",
            "Este estudo investigou as relações entre características do processo de desenvolvimento ",
            "e métricas de qualidade interna em repositórios Java populares. As análises revelaram ",
            "padrões interessantes que contribuem para o entendimento da qualidade em projetos ",
            "open-source.",
            "",
            "### 5.1 Contribuições",
            "",
            "- Análise empírica de 1.000 repositórios Java populares",
            "- Identificação de correlações entre processo e qualidade",
            "- Framework de análise replicável para outros estudos",
            "",
            "### 5.2 Trabalhos Futuros",
            "",
            "- Análise longitudinal da evolução da qualidade",
            "- Incorporação de métricas de qualidade modernas",
            "- Estudo comparativo entre diferentes linguagens",
            "- Investigação de fatores causais",
            "",
            "---",
            ""
        ])
    
    def _add_appendices(self, data_summary, plots):
        """Adiciona apêndices com informações adicionais."""
        self.report_content.extend([
            "## Apêndices",
            "",
            "### Apêndice A: Resumo dos Dados",
            ""
        ])
        
        if data_summary:
            self.report_content.extend([
                "#### Estatísticas Gerais por Repositório",
                ""
            ])
            
            # Tabela resumo
            self.report_content.extend([
                "| Métrica | Média | Mediana | Desvio Padrão |",
                "|---------|-------|---------|---------------|"
            ])
            
            for metric, stats in data_summary.items():
                if isinstance(stats, dict) and 'mean' in stats:
                    metric_label = self._get_metric_label(metric)
                    self.report_content.append(
                        f"| {metric_label} | {stats['mean']:.2f} | "
                        f"{stats['median']:.2f} | {stats['std']:.2f} |"
                    )
            
            self.report_content.append("")
        
        self.report_content.extend([
            "### Apêndice B: Visualizações",
            "",
            "As seguintes visualizações foram geradas durante a análise:",
            ""
        ])
        
        # Listar todos os gráficos
        for plot_name, plot_path in plots.items():
            plot_filename = os.path.basename(plot_path)
            plot_title = plot_name.replace('_', ' ').title()
            self.report_content.extend([
                f"- {plot_title}: `plots/{plot_filename}`",
                ""
            ])
        
        self.report_content.extend([
            "### Apêndice C: Ferramentas Utilizadas",
            "",
            "- **Python**: Linguagem de programação",
            "- **Pandas**: Manipulação de dados",
            "- **SciPy**: Análises estatísticas",
            "- **Matplotlib/Seaborn**: Visualizações",
            "- **GitHub API**: Coleta de dados dos repositórios",
            "- **CK Tool**: Análise de métricas de qualidade",
            "",
            "---",
            "",
            f"*Relatório gerado automaticamente em {self.timestamp.strftime('%d/%m/%Y às %H:%M:%S')}*"
        ])
    
    def _extract_key_findings(self, analysis_results, statistical_results):
        """Extrai as principais descobertas do estudo."""
        findings = []
        
        if statistical_results and 'statistical_summary' in statistical_results:
            summary = statistical_results['statistical_summary']
            if 'key_findings' in summary:
                findings.extend(summary['key_findings'])
        
        # Adicionar descobertas baseadas nas hipóteses
        if statistical_results and 'hypothesis_testing' in statistical_results:
            confirmed_hypotheses = []
            rejected_hypotheses = []
            
            for rq_id, result in statistical_results['hypothesis_testing'].items():
                conclusion = result.get('conclusion', '')
                if 'CONFIRMADA' in conclusion:
                    confirmed_hypotheses.append(rq_id)
                elif 'REJEITADA' in conclusion:
                    rejected_hypotheses.append(rq_id)
            
            if confirmed_hypotheses:
                findings.append(f"Hipóteses confirmadas: {', '.join(confirmed_hypotheses)}")
            
            if rejected_hypotheses:
                findings.append(f"Hipóteses rejeitadas: {', '.join(rejected_hypotheses)}")
        
        # Adicionar descoberta padrão se nenhuma foi encontrada
        if not findings:
            findings.append("Análise realizada com sucesso em repositórios Java populares")
        
        return findings
    
    def _interpret_correlation_strength(self, abs_correlation):
        """Interpreta a força da correlação."""
        if abs_correlation < 0.1:
            return "negligível"
        elif abs_correlation < 0.3:
            return "fraca"
        elif abs_correlation < 0.5:
            return "moderada"
        elif abs_correlation < 0.7:
            return "forte"
        else:
            return "muito forte"
    
    def _get_metric_label(self, metric):
        """Retorna label amigável para a métrica."""
        labels = {
            'stars': 'Estrelas',
            'forks': 'Forks',
            'watchers': 'Watchers',
            'contributors': 'Contribuidores',
            'releases': 'Releases',
            'age_years': 'Idade (anos)',
            'loc_total': 'Linhas de Código',
            'loc_comments_total': 'Linhas de Comentários',
            'classes_count': 'Número de Classes',
            'methods_count': 'Número de Métodos',
            'cbo_avg': 'CBO Médio',
            'dit_avg': 'DIT Médio',
            'lcom_avg': 'LCOM Médio'
        }
        return labels.get(metric, metric.replace('_', ' ').title())
    
    def _save_report(self, filename):
        """Salva o relatório em arquivo Markdown."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_content))
        
        print(f"Relatório salvo: {filename}")
        return filename
