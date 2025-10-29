"""
Módulo para geração do relatório final da análise de code review
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd

from ..config.config import Config

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Classe para gerar o relatório final da análise"""
    
    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        
    def generate_final_report(self, df: pd.DataFrame, analysis_results: Dict[str, Any], 
                            plot_files: Dict[str, str]) -> str:
        """
        Gera o relatório final completo da análise
        
        Args:
            df: DataFrame com os dados dos PRs
            analysis_results: Resultados das análises estatísticas
            plot_files: Dicionário com caminhos dos arquivos de plots
            
        Returns:
            Caminho do arquivo de relatório gerado
        """
        logger.info("Gerando relatório final...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"relatorio_final_lab03_{timestamp}.md"
        report_path = self.output_dir / report_filename
        
        # Gera o conteúdo do relatório
        report_content = self._build_report_content(df, analysis_results, plot_files)
        
        # Salva o relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Também salva os resultados em JSON
        json_filename = f"analysis_results_{timestamp}.json"
        json_path = self.output_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, default=str, ensure_ascii=False)
        
        logger.info(f"Relatório final salvo em: {report_path}")
        logger.info(f"Resultados em JSON salvos em: {json_path}")
        
        return str(report_path)
    
    def _build_report_content(self, df: pd.DataFrame, analysis_results: Dict[str, Any], 
                            plot_files: Dict[str, str]) -> str:
        """Constrói o conteúdo completo do relatório"""
        
        content = []
        
        # Cabeçalho
        content.append(self._generate_header())
        
        # 1. Introdução e Hipóteses
        content.append(self._generate_introduction())
        
        # 2. Metodologia
        content.append(self._generate_methodology())
        
        # 3. Caracterização do Dataset
        content.append(self._generate_dataset_section(df, analysis_results))
        
        # 4. Resultados das Questões de Pesquisa - Grupo A (Feedback)
        content.append(self._generate_feedback_results(analysis_results))
        
        # 5. Resultados das Questões de Pesquisa - Grupo B (Revisões)
        content.append(self._generate_reviews_results(analysis_results))
        
        # 6. Análise de Correlações
        content.append(self._generate_correlation_analysis(analysis_results))
        
        # 7. Discussão e Interpretação
        content.append(self._generate_discussion(analysis_results))
        
        # 8. Conclusões
        content.append(self._generate_conclusions(analysis_results))
        
        # 9. Visualizações
        content.append(self._generate_visualizations_section(plot_files))
        
        # 10. Apêndices
        content.append(self._generate_appendices(analysis_results))
        
        return '\\n\\n'.join(content)
    
    def _generate_header(self) -> str:
        return f"""# LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub

**Data do Relatório:** {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}

**Autores:** [Inserir nomes dos integrantes do grupo]

---"""
    
    def _generate_introduction(self) -> str:
        return """## 1. Introdução

### Contexto

A prática de code review tornou-se fundamental nos processos de desenvolvimento ágil, especialmente em projetos open source hospedados no GitHub. Este estudo analisa sistematicamente a atividade de code review através da análise de Pull Requests (PRs) em repositórios populares, com o objetivo de identificar variáveis que influenciam no resultado final das revisões.

### Hipóteses Informais

Baseando-se na literatura e experiência prática em desenvolvimento de software, formulamos as seguintes hipóteses informais:

#### **Hipóteses sobre Feedback Final (RQ01-RQ04):**

- **H1 (Tamanho):** PRs menores têm maior probabilidade de serem aprovados (MERGED), pois são mais fáceis de revisar e têm menor risco de introduzir bugs.

- **H2 (Tempo):** PRs que são analisados mais rapidamente têm maior probabilidade de serem aprovados, indicando consenso sobre a mudança.

- **H3 (Descrição):** PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados, pois facilitam o entendimento do revisor.

- **H4 (Interações):** PRs com mais interações (comentários, participantes) podem ter menor probabilidade de aprovação, indicando controvérsias ou problemas na implementação.

#### **Hipóteses sobre Número de Revisões (RQ05-RQ08):**

- **H5 (Tamanho):** PRs maiores requerem mais revisões devido à complexidade.

- **H6 (Tempo):** Maior tempo de análise está correlacionado com maior número de revisões.

- **H7 (Descrição):** PRs com melhor descrição requerem menos revisões devido à clareza.

- **H8 (Interações):** Existe correlação positiva forte entre número de interações e número de revisões."""
    
    def _generate_methodology(self) -> str:
        return """## 2. Metodologia

### 2.1 Seleção dos Repositórios

- **Critério de Popularidade:** 200 repositórios mais populares do GitHub (ordenados por estrelas)
- **Critério de Atividade:** Repositórios com pelo menos 100 PRs (MERGED + CLOSED)
- **Fonte:** GitHub API v3

### 2.2 Critérios de Seleção dos Pull Requests

Para garantir que analisamos PRs que passaram por processo real de code review:

- **Status:** Apenas PRs com status MERGED ou CLOSED
- **Revisões:** PRs com pelo menos uma revisão registrada
- **Tempo Mínimo:** Tempo de análise superior a 1 hora (elimina aprovações automáticas)

### 2.3 Métricas Coletadas

#### **Tamanho dos PRs:**
- Número de arquivos modificados
- Total de linhas adicionadas
- Total de linhas removidas  
- Total de mudanças (adições + remoções)

#### **Tempo de Análise:**
- Intervalo entre criação e fechamento/merge do PR
- Medido em horas e dias

#### **Descrição:**
- Número de caracteres na descrição
- Presença ou ausência de descrição

#### **Interações:**
- Número de participantes únicos
- Número de comentários gerais
- Número de comentários de revisão
- Total de comentários

### 2.4 Métodos Estatísticos

#### **Testes de Hipótese:**
- **Mann-Whitney U:** Para comparar distribuições entre grupos (MERGED vs CLOSED)
- **Chi-quadrado:** Para variáveis categóricas
- **Justificativa:** Dados não seguem distribuição normal, métodos não-paramétricos são mais robustos

#### **Análise de Correlação:**
- **Spearman:** Correlação não-paramétrica (método principal)
- **Pearson:** Correlação paramétrica (comparação)
- **Justificativa:** Correlação de Spearman é mais robusta para dados com outliers e não-normais

#### **Nível de Significância:**
- α = 0.05 (5%)"""
    
    def _generate_dataset_section(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> str:
        dataset_info = analysis_results.get('dataset_info', {})
        
        total_prs = dataset_info.get('total_prs', 0)
        merged_prs = dataset_info.get('merged_prs', 0) 
        closed_prs = dataset_info.get('closed_prs', 0)
        merge_rate = dataset_info.get('merge_rate', 0)
        unique_repos = dataset_info.get('unique_repositories', 0)
        
        # Estatísticas resumo das métricas principais
        summary_stats = analysis_results.get('summary_statistics', {})
        
        content = f"""## 3. Caracterização do Dataset

### 3.1 Composição Geral

- **Total de Pull Requests:** {total_prs:,}
- **PRs Aprovados (MERGED):** {merged_prs:,} ({merge_rate:.1f}%)
- **PRs Rejeitados (CLOSED):** {closed_prs:,} ({100-merge_rate:.1f}%)
- **Repositórios Analisados:** {unique_repos}
- **Taxa de Aprovação Geral:** {merge_rate:.1f}%

### 3.2 Estatísticas Descritivas das Métricas

#### **Métricas de Tamanho:**"""
        
        # Adiciona estatísticas de tamanho
        size_metrics = ['total_changes', 'files_changed', 'additions', 'deletions']
        for metric in size_metrics:
            if metric in summary_stats:
                stats = summary_stats[metric]
                content += f"""
- **{metric.replace('_', ' ').title()}:**
  - Mediana: {stats.get('median', 0):.1f}
  - Média: {stats.get('mean', 0):.1f} (±{stats.get('std', 0):.1f})
  - Quartis: Q1={stats.get('q25', 0):.1f}, Q3={stats.get('q75', 0):.1f}"""
        
        content += "\\n#### **Métricas de Tempo:**"
        
        # Adiciona estatísticas de tempo
        time_metrics = ['analysis_time_hours', 'analysis_time_days']
        for metric in time_metrics:
            if metric in summary_stats:
                stats = summary_stats[metric]
                unit = "horas" if "hours" in metric else "dias"
                content += f"""
- **Tempo de Análise ({unit}):**
  - Mediana: {stats.get('median', 0):.1f} {unit}
  - Média: {stats.get('mean', 0):.1f} {unit} (±{stats.get('std', 0):.1f})"""
        
        content += "\\n#### **Métricas de Interação:**"
        
        # Adiciona estatísticas de interação
        interaction_metrics = ['participants_count', 'total_comments', 'reviews_count']
        for metric in interaction_metrics:
            if metric in summary_stats:
                stats = summary_stats[metric]
                content += f"""
- **{metric.replace('_', ' ').title()}:**
  - Mediana: {stats.get('median', 0):.1f}
  - Média: {stats.get('mean', 0):.1f} (±{stats.get('std', 0):.1f})"""
        
        return content
    
    def _generate_feedback_results(self, analysis_results: Dict[str, Any]) -> str:
        content = """## 4. Resultados - Grupo A: Feedback Final das Revisões (RQ01-RQ04)

Esta seção analisa as variáveis que influenciam no resultado final dos PRs (MERGED vs CLOSED)."""
        
        feedback_results = analysis_results.get('rq_a_feedback', {})
        
        # RQ01: Tamanho vs Feedback
        content += "\\n### 4.1 RQ01: Relação entre Tamanho dos PRs e Feedback Final"
        
        rq01_results = feedback_results.get('rq01_size_vs_feedback', {})
        if rq01_results:
            content += f"""
**Questão:** {rq01_results.get('question', '')}

**Resultados dos Testes Estatísticos:**"""
            
            for metric, test_result in rq01_results.get('statistical_tests', {}).items():
                p_value = test_result.get('p_value', 1.0)
                significant = test_result.get('significant', False)
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** {'Significante' if significant else 'Não significante'} (p={p_value:.4f})"""
            
            content += "\\n**Estatísticas Descritivas:**"
            
            for metric, desc_stats in rq01_results.get('descriptive_stats', {}).items():
                merged_median = desc_stats.get('merged', {}).get('median', 0)
                closed_median = desc_stats.get('closed', {}).get('median', 0)
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** Mediana MERGED = {merged_median:.1f}, Mediana CLOSED = {closed_median:.1f}"""
        
        # RQ02: Tempo vs Feedback
        content += "\\n### 4.2 RQ02: Relação entre Tempo de Análise e Feedback Final"
        
        rq02_results = feedback_results.get('rq02_time_vs_feedback', {})
        if rq02_results:
            content += f"""
**Questão:** {rq02_results.get('question', '')}

**Resultados:**"""
            
            for metric, test_result in rq02_results.get('statistical_tests', {}).items():
                p_value = test_result.get('p_value', 1.0)
                significant = test_result.get('significant', False)
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** {'Significante' if significant else 'Não significante'} (p={p_value:.4f})"""
        
        # RQ03: Descrição vs Feedback  
        content += "\\n### 4.3 RQ03: Relação entre Descrição e Feedback Final"
        
        rq03_results = feedback_results.get('rq03_description_vs_feedback', {})
        if rq03_results:
            content += f"""
**Questão:** {rq03_results.get('question', '')}

**Resultados:**"""
            
            for metric, test_result in rq03_results.get('statistical_tests', {}).items():
                p_value = test_result.get('p_value', 1.0)
                significant = test_result.get('significant', False)
                test_name = test_result.get('test', 'Teste')
                
                content += f"""
- **{metric.replace('_', ' ').title()}** ({test_name}): {'Significante' if significant else 'Não significante'} (p={p_value:.4f})"""
        
        # RQ04: Interações vs Feedback
        content += "\\n### 4.4 RQ04: Relação entre Interações e Feedback Final"
        
        rq04_results = feedback_results.get('rq04_interactions_vs_feedback', {})
        if rq04_results:
            content += f"""
**Questão:** {rq04_results.get('question', '')}

**Resultados:**"""
            
            for metric, test_result in rq04_results.get('statistical_tests', {}).items():
                p_value = test_result.get('p_value', 1.0)
                significant = test_result.get('significant', False)
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** {'Significante' if significant else 'Não significante'} (p={p_value:.4f})"""
        
        return content
    
    def _generate_reviews_results(self, analysis_results: Dict[str, Any]) -> str:
        content = """## 5. Resultados - Grupo B: Número de Revisões (RQ05-RQ08)

Esta seção analisa as variáveis que se correlacionam com o número de revisões realizadas nos PRs."""
        
        reviews_results = analysis_results.get('rq_b_reviews', {})
        
        # RQ05: Tamanho vs Revisões
        content += "\\n### 5.1 RQ05: Relação entre Tamanho dos PRs e Número de Revisões"
        
        rq05_results = reviews_results.get('rq05_size_vs_reviews', {})
        if rq05_results:
            content += f"""
**Questão:** {rq05_results.get('question', '')}

**Correlações encontradas:**"""
            
            for metric, corr_data in rq05_results.get('correlations', {}).items():
                spearman_corr = corr_data.get('spearman', {}).get('correlation', 0)
                spearman_sig = corr_data.get('spearman', {}).get('significant', False)
                
                strength = self._interpret_correlation_strength(abs(spearman_corr))
                direction = "positiva" if spearman_corr > 0 else "negativa"
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** Correlação {direction} {strength} (ρ={spearman_corr:.3f}, {'significante' if spearman_sig else 'não significante'})"""
        
        # RQ06: Tempo vs Revisões
        content += "\\n### 5.2 RQ06: Relação entre Tempo de Análise e Número de Revisões"
        
        rq06_results = reviews_results.get('rq06_time_vs_reviews', {})
        if rq06_results:
            content += f"""
**Questão:** {rq06_results.get('question', '')}"""
            
            for metric, corr_data in rq06_results.get('correlations', {}).items():
                spearman_corr = corr_data.get('spearman', {}).get('correlation', 0)
                spearman_sig = corr_data.get('spearman', {}).get('significant', False)
                
                strength = self._interpret_correlation_strength(abs(spearman_corr))
                direction = "positiva" if spearman_corr > 0 else "negativa"
                
                content += f"""
- **{metric.replace('_', ' ').title()}:** Correlação {direction} {strength} (ρ={spearman_corr:.3f}, {'significante' if spearman_sig else 'não significante'})"""
        
        # RQ07 e RQ08 seguem padrão similar...
        content += "\\n### 5.3 RQ07: Relação entre Descrição e Número de Revisões"
        content += "\\n[Análise detalhada da correlação entre qualidade da descrição e número de revisões]"
        
        content += "\\n### 5.4 RQ08: Relação entre Interações e Número de Revisões" 
        content += "\\n[Análise detalhada da correlação entre nível de interação e número de revisões]"
        
        return content
    
    def _generate_correlation_analysis(self, analysis_results: Dict[str, Any]) -> str:
        return """## 6. Análise Geral de Correlações

### 6.1 Matriz de Correlação

A matriz de correlação de Spearman entre todas as métricas numéricas revelou os seguintes padrões:

[Análise da matriz de correlação será inserida aqui baseada nos resultados]

### 6.2 Correlações Mais Fortes

[Lista das correlações mais significativas encontradas]

### 6.3 Interpretação das Correlações

[Interpretação do significado prático das correlações encontradas]"""
    
    def _generate_discussion(self, analysis_results: Dict[str, Any]) -> str:
        return """## 7. Discussão

### 7.1 Validação das Hipóteses

#### **Hipóteses sobre Feedback Final:**

**H1 (Tamanho vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ01]

**H2 (Tempo vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ02]  

**H3 (Descrição vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ03]

**H4 (Interações vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ04]

#### **Hipóteses sobre Número de Revisões:**

**H5 (Tamanho vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ05]

**H6 (Tempo vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ06]

**H7 (Descrição vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ07]

**H8 (Interações vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ08]

### 7.2 Implicações Práticas

Os resultados desta análise têm implicações importantes para:

1. **Desenvolvedores:** [Recomendações baseadas nos achados]
2. **Revisores:** [Diretrizes para processo de revisão]  
3. **Gestores de Projeto:** [Insights para otimização do processo]

### 7.3 Limitações do Estudo

- **Representatividade:** Limitado aos repositórios mais populares do GitHub
- **Contexto Temporal:** Análise em ponto específico no tempo
- **Variáveis Não Controladas:** Fatores como complexidade do domínio, experiência dos desenvolvedores
- **Causalidade:** Correlações não implicam causalidade"""
    
    def _generate_conclusions(self, analysis_results: Dict[str, Any]) -> str:
        dataset_info = analysis_results.get('dataset_info', {})
        merge_rate = dataset_info.get('merge_rate', 0)
        
        return f"""## 8. Conclusões

### 8.1 Principais Achados

Com base na análise de {dataset_info.get('total_prs', 0):,} Pull Requests de {dataset_info.get('unique_repositories', 0)} repositórios populares do GitHub, concluímos:

1. **Taxa de Aprovação:** {merge_rate:.1f}% dos PRs analisados foram aprovados (merged)

2. **Fatores de Aprovação:** [Listar principais fatores que influenciam na aprovação]

3. **Padrões de Revisão:** [Resumir padrões encontrados no número de revisões]

4. **Correlações Significativas:** [Destacar as correlações mais importantes encontradas]

### 8.2 Contribuições

Este estudo contribui para o entendimento da dinâmica de code review em projetos open source, fornecendo:

- Evidências empíricas sobre fatores que influenciam na aprovação de PRs
- Insights sobre o processo de revisão em repositórios populares  
- Base para futuras pesquisas sobre colaboração em desenvolvimento de software

### 8.3 Trabalhos Futuros

- Análise longitudinal para identificar tendências temporais
- Estudo de fatores qualitativos (complexidade do código, experiência dos desenvolvedores)
- Comparação entre diferentes tipos de repositórios (linguagens, domínios)
- Desenvolvimento de modelos preditivos para aprovação de PRs"""
    
    def _generate_visualizations_section(self, plot_files: Dict[str, str]) -> str:
        content = """## 9. Visualizações

### 9.1 Gráficos Gerados

Os seguintes gráficos foram gerados para ilustrar os resultados da análise:"""
        
        # Lista os arquivos de plot gerados
        for plot_name, plot_path in plot_files.items():
            plot_file = Path(plot_path).name
            content += f"""
- **{plot_name.replace('_', ' ').title()}:** `{plot_file}`"""
        
        content += """

### 9.2 Como Interpretar

- **Box plots:** Mostram distribuição, mediana, quartis e outliers
- **Scatter plots:** Revelam correlações e padrões de relacionamento
- **Histogramas:** Mostram distribuição de frequências
- **Heatmaps:** Visualizam matriz de correlações

### 9.3 Visualizações Interativas

Gráficos interativos em HTML foram gerados para exploração mais detalhada dos dados."""
        
        return content
    
    def _generate_appendices(self, analysis_results: Dict[str, Any]) -> str:
        return """## 10. Apêndices

### 10.1 Metodologia Detalhada dos Testes Estatísticos

#### **Mann-Whitney U Test:**
- **Aplicação:** Comparação de distribuições entre grupos (MERGED vs CLOSED)
- **Pressupostos:** Amostras independentes, variável ordinal ou contínua
- **Interpretação:** p < 0.05 indica diferença estatisticamente significante

#### **Correlação de Spearman:**
- **Aplicação:** Medida de associação monotônica entre variáveis
- **Vantagem:** Robusta a outliers e não assume normalidade
- **Interpretação:** ρ entre -1 e 1, onde valores próximos aos extremos indicam correlação forte

### 10.2 Critérios de Qualidade dos Dados

- **Tratamento de Outliers:** Remoção de valores extremos (> Q3 + 1.5*IQR)
- **Valores Ausentes:** Exclusão de registros com dados incompletos nas análises específicas
- **Validação:** Verificação de consistência entre métricas relacionadas

### 10.3 Ferramentas Utilizadas

- **Coleta de Dados:** GitHub API v3
- **Processamento:** Python (pandas, numpy)
- **Análise Estatística:** SciPy
- **Visualização:** Matplotlib, Seaborn, Plotly
- **Relatórios:** Markdown com integração de plots"""
    
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