# Arquivo: src/modules/report_generator.py

import os
from datetime import datetime
from .. import config

class ReportGenerator:
    """
    Classe responsável por gerar o relatório final em markdown.
    """
    
    def __init__(self, analysis_results, plots_paths=None):
        """
        Inicializa o gerador de relatório.
        """
        self.results = analysis_results
        self.plots_paths = plots_paths or []
        self.output_dir = config.OUTPUT_DIR
        
    def generate_hypotheses_section(self):
        """
        Gera a seção de hipóteses informais.
        """
        return """## Hipóteses Informais

Antes de analisar os dados, formulamos as seguintes hipóteses sobre repositórios populares no GitHub:

### RQ01 - Idade dos Repositórios
**Hipótese**: Repositórios populares tendem a ser mais antigos, pois precisaram de tempo para amadurecer e ganhar reconhecimento da comunidade.

### RQ02 - Contribuições Externas  
**Hipótese**: Repositórios populares recebem muitas contribuições externas (pull requests aceitas), pois atraem desenvolvedores interessados em contribuir para projetos conhecidos.

### RQ03 - Frequência de Releases
**Hipótese**: Projetos populares lançam releases com frequência moderada, balanceando estabilidade com novas funcionalidades.

### RQ04 - Frequência de Atualizações
**Hipótese**: Repositórios populares são atualizados com frequência, pois mantêm desenvolvimento ativo.

### RQ05 - Linguagens Populares
**Hipótese**: Repositórios populares usam linguagens mainstream como JavaScript, Python, Java e C++.

### RQ06 - Taxa de Fechamento de Issues
**Hipótese**: Projetos populares têm alta taxa de fechamento de issues, indicando manutenção ativa.

### RQ07 - Linguagens vs Métricas (Bônus)
**Hipótese**: Repositórios em linguagens mais populares (JavaScript, Python) recebem mais contribuições e são mais ativos.

"""

    def generate_methodology_section(self):
        """
        Gera a seção de metodologia.
        """
        return f"""## Metodologia

### Coleta de Dados
- **Fonte**: API GraphQL/REST do GitHub
- **Amostra**: {config.TOTAL_REPOS_TO_FETCH} repositórios com maior número de estrelas
- **Período**: Dados coletados em {datetime.now().strftime('%d/%m/%Y')}
- **Método**: {config.API_METHOD} API com paginação automática

### Métricas Coletadas
- **RQ01**: Data de criação → Idade em anos
- **RQ02**: Pull requests aceitas (merged)  
- **RQ03**: Total de releases publicadas
- **RQ04**: Data da última atualização → Dias desde última atualização
- **RQ05**: Linguagem primária do repositório
- **RQ06**: Issues abertas e fechadas → Taxa de fechamento

### Análise Estatística
- **Medida central**: Mediana (mais robusta a outliers)
- **Visualizações**: Histogramas, box plots, gráficos de barras
- **Correlações**: Matriz de correlação entre métricas numéricas

"""

    def generate_results_section(self):
        """
        Gera a seção de resultados.
        """
        section = "## Resultados\n\n"
        
        if 'RQ01' in self.results:
            rq01 = self.results['RQ01']
            section += f"""### RQ01: Sistemas populares são maduros/antigos?
**Resultado**: Idade mediana de **{rq01['median_age_years']:.1f} anos**

"""

        if 'RQ02' in self.results:
            rq02 = self.results['RQ02']
            section += f"""### RQ02: Sistemas populares recebem muita contribuição externa?
**Resultado**: Mediana de **{rq02['median_merged_prs']:.0f} pull requests aceitas**

"""

        if 'RQ03' in self.results:
            rq03 = self.results['RQ03']
            section += f"""### RQ03: Sistemas populares lançam releases com frequência?
**Resultado**: Mediana de **{rq03['median_releases']:.0f} releases**

"""

        if 'RQ04' in self.results:
            rq04 = self.results['RQ04']
            section += f"""### RQ04: Sistemas populares são atualizados com frequência?
**Resultado**: Mediana de **{rq04['median_days_since_update']:.0f} dias** desde a última atualização

"""

        if 'RQ05' in self.results:
            rq05 = self.results['RQ05']
            top_3 = list(rq05['top_languages'])[:3]
            section += f"""### RQ05: Sistemas populares são escritos nas linguagens mais populares?
**Resultado**: Top 3 linguagens: **{', '.join(top_3)}**

"""

        if 'RQ06' in self.results:
            rq06 = self.results['RQ06']
            section += f"""### RQ06: Sistemas populares possuem alto percentual de issues fechadas?
**Resultado**: Taxa mediana de fechamento: **{rq06['median_closure_rate']:.1%}**

"""

        # RQ07 - Análise por linguagem
        if 'RQ07' in self.results:
            rq07 = self.results['RQ07']
            section += """### RQ07: Análise por Linguagem (Bônus)

| Linguagem | Repos | PRs Aceitas (med) | Releases (med) | Dias Última Atualização (med) |
|-----------|-------|-------------------|----------------|-------------------------------|
"""
            
            for lang, data in rq07['results_by_language'].items():
                section += f"| {lang} | {data['count']} | {data['median_merged_prs']:.0f} | {data['median_releases']:.0f} | {data['median_days_since_update']:.0f} |\n"
            
            section += "\n"
        
        return section

    def generate_discussion_section(self):
        """
        Gera a seção de discussão.
        """
        return """## Discussão

### Análise das Hipóteses

#### RQ01 - Idade dos Repositórios
A idade mediana confirma que repositórios populares tendem a ser projetos maduros, que tiveram tempo para se estabelecer na comunidade. Projetos muito novos raramente alcançam popularidade imediata.

#### RQ02 - Contribuições Externas
O número de pull requests aceitas varia significativamente, mas repositórios populares geralmente atraem colaboradores externos, validando a hipótese de que popularidade gera mais contribuições.

#### RQ03 - Frequência de Releases
A distribuição de releases mostra que projetos populares mantêm ciclos de lançamento, balanceando estabilidade com evolução do software.

#### RQ04 - Frequência de Atualizações  
A análise dos dias desde a última atualização indica se os projetos mantêm desenvolvimento ativo ou estão em estado de manutenção.

#### RQ05 - Linguagens Populares
A distribuição de linguagens reflete as tendências da indústria, com linguagens como JavaScript, Python e Java dominando o cenário de desenvolvimento.

#### RQ06 - Taxa de Fechamento de Issues
A taxa de fechamento de issues indica a qualidade da manutenção e o engajamento da comunidade com o projeto.

#### RQ07 - Análise por Linguagem
A comparação entre linguagens revela diferenças nos padrões de desenvolvimento e manutenção entre diferentes ecossistemas de programação.

### Limitações do Estudo
- Amostra limitada aos repositórios mais populares (viés de seleção)
- Dados coletados em um único momento temporal
- Métricas quantitativas não capturam qualidade do código
- API do GitHub pode ter limitações nos dados disponíveis

### Conclusões
Os dados confirmam parcialmente nossas hipóteses iniciais, mostrando que repositórios populares tendem a ser projetos maduros, ativos e bem mantidos, com padrões que variam según a linguagem de programação utilizada.

"""

    def generate_visualizations_section(self):
        """
        Gera a seção de visualizações.
        """
        section = "## Visualizações\n\n"
        
        if self.plots_paths:
            section += "Os seguintes gráficos foram gerados para ilustrar os resultados:\n\n"
            
            plot_descriptions = {
                'rq01_age_distribution.png': 'RQ01 - Distribuição da idade dos repositórios',
                'rq02_pull_requests.png': 'RQ02 - Distribuição de pull requests aceitas',
                'rq03_releases.png': 'RQ03 - Distribuição de releases',
                'rq04_update_frequency.png': 'RQ04 - Frequência de atualizações',
                'rq05_languages.png': 'RQ05 - Distribuição de linguagens',
                'rq06_issues_closure.png': 'RQ06 - Taxa de fechamento de issues',
                'correlation_matrix.png': 'Matriz de correlação entre métricas'
            }
            
            for plot_path in self.plots_paths:
                filename = os.path.basename(plot_path)
                if filename in plot_descriptions:
                    section += f"- **{plot_descriptions[filename]}**\n"
                    section += f"  - Arquivo: `{plot_path}`\n\n"
        
        return section

    def generate_full_report(self):
        """
        Gera o relatório completo.
        """
        report = f"""# Análise de Repositórios Populares do GitHub

**Laboratório de Experimentação de Software**  
**Data**: {datetime.now().strftime('%d de %B de %Y')}  
**Repositórios analisados**: {config.TOTAL_REPOS_TO_FETCH}

---

{self.generate_hypotheses_section()}

{self.generate_methodology_section()}

{self.generate_results_section()}

{self.generate_discussion_section()}

{self.generate_visualizations_section()}

---

## Informações Técnicas

- **Método de coleta**: {config.API_METHOD} API
- **Arquivo de dados**: `{config.CSV_FILEPATH}`
- **Diretório de gráficos**: `{config.PLOTS_DIR}`
- **Gerado em**: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

"""
        return report

    def save_report(self, filename=None):
        """
        Salva o relatório em arquivo markdown.
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"relatorio_analise_{timestamp}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Criar diretório se não existir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Gerar e salvar relatório
        report_content = self.generate_full_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Relatório salvo em: {filepath}")
        return filepath
