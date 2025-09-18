import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
from .. import config

class DataVisualizer:
    
    def __init__(self, csv_filepath=None):
        self.csv_filepath = csv_filepath or config.CSV_FILEPATH
        self.dataframe = None
        self.plots_dir = config.PLOTS_DIR
        
        plt.style.use('default')
        sns.set_palette("husl")
        
    def load_data(self):
        """
        Carrega os dados do arquivo CSV.
        """
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {self.csv_filepath}")
        
        self.dataframe = pd.read_csv(self.csv_filepath)
        
        # Preprocessar datas
        self.dataframe['created_at'] = pd.to_datetime(self.dataframe['created_at']).dt.tz_localize(None)
        self.dataframe['updated_at'] = pd.to_datetime(self.dataframe['updated_at']).dt.tz_localize(None)
        
        # Calcular métricas derivadas
        current_date = datetime.now()
        self.dataframe['age_years'] = (current_date - self.dataframe['created_at']).dt.days / 365.25
        self.dataframe['days_since_update'] = (current_date - self.dataframe['updated_at']).dt.days
        self.dataframe['total_issues'] = self.dataframe['open_issues'] + self.dataframe['closed_issues']
        self.dataframe['issues_closure_rate'] = np.where(
            self.dataframe['total_issues'] > 0,
            self.dataframe['closed_issues'] / self.dataframe['total_issues'],
            0
        )
        
        print(f"Dados carregados: {len(self.dataframe)} repositórios")
        return self.dataframe
    
    def create_age_distribution_plot(self):
        """
        RQ01: Cria gráfico da distribuição de idades dos repositórios.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.hist(self.dataframe['age_years'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('Idade (anos)')
        plt.ylabel('Frequência')
        plt.title('RQ01: Distribuição da Idade dos Repositórios')
        plt.axvline(self.dataframe['age_years'].median(), color='red', linestyle='--', 
                   label=f'Mediana: {self.dataframe["age_years"].median():.1f} anos')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.boxplot(self.dataframe['age_years'], vert=True)
        plt.ylabel('Idade (anos)')
        plt.title('Box Plot - Idade dos Repositórios')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        os.makedirs(self.plots_dir, exist_ok=True)
        filepath = os.path.join(self.plots_dir, 'rq01_age_distribution.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_pull_requests_plot(self):
        """
        RQ02: Cria gráfico da distribuição de pull requests aceitas.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Distribuição log
        plt.subplot(1, 2, 1)
        # Filtrar valores > 0 para escala log
        pr_data = self.dataframe[self.dataframe['merged_pull_requests'] > 0]['merged_pull_requests']
        plt.hist(pr_data, bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.xlabel('Pull Requests Aceitas (escala log)')
        plt.ylabel('Frequência')
        plt.title('RQ02: Distribuição de PRs Aceitas')
        plt.yscale('log')
        plt.axvline(self.dataframe['merged_pull_requests'].median(), color='red', linestyle='--',
                   label=f'Mediana: {self.dataframe["merged_pull_requests"].median():.0f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Top 20 repositórios
        plt.subplot(1, 2, 2)
        top_20 = self.dataframe.nlargest(20, 'merged_pull_requests')[['name', 'merged_pull_requests']]
        plt.barh(range(len(top_20)), top_20['merged_pull_requests'], color='lightcoral')
        plt.yticks(range(len(top_20)), [name.split('/')[-1] for name in top_20['name']], fontsize=8)
        plt.xlabel('Pull Requests Aceitas')
        plt.title('Top 20 - PRs Aceitas')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'rq02_pull_requests.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_releases_plot(self):
        """
        RQ03: Cria gráfico da distribuição de releases.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Histograma
        plt.subplot(1, 2, 1)
        plt.hist(self.dataframe['releases'], bins=30, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Número de Releases')
        plt.ylabel('Frequência')
        plt.title('RQ03: Distribuição de Releases')
        plt.axvline(self.dataframe['releases'].median(), color='red', linestyle='--',
                   label=f'Mediana: {self.dataframe["releases"].median():.0f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Releases vs Stars (scatter)
        plt.subplot(1, 2, 2)
        plt.scatter(self.dataframe['stars'], self.dataframe['releases'], alpha=0.6, color='purple')
        plt.xlabel('Estrelas (escala log)')
        plt.ylabel('Releases')
        plt.title('Releases vs Popularidade')
        plt.xscale('log')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'rq03_releases.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_update_frequency_plot(self):
        """
        RQ04: Cria gráfico da frequência de atualizações.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: Histograma
        plt.subplot(1, 2, 1)
        plt.hist(self.dataframe['days_since_update'], bins=30, alpha=0.7, color='lightblue', edgecolor='black')
        plt.xlabel('Dias desde última atualização')
        plt.ylabel('Frequência')
        plt.title('RQ04: Tempo desde Última Atualização')
        plt.axvline(self.dataframe['days_since_update'].median(), color='red', linestyle='--',
                   label=f'Mediana: {self.dataframe["days_since_update"].median():.0f} dias')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Categorias de atualização
        plt.subplot(1, 2, 2)
        categories = []
        for days in self.dataframe['days_since_update']:
            if days <= 30:
                categories.append('Último mês')
            elif days <= 90:
                categories.append('Últimos 3 meses')
            elif days <= 365:
                categories.append('Último ano')
            else:
                categories.append('Mais de 1 ano')
        
        cat_counts = pd.Series(categories).value_counts()
        plt.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Categorias de Atualização')
        
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'rq04_update_frequency.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_languages_plot(self):
        """
        RQ05: Cria gráfico da distribuição de linguagens.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(15, 8))
        
        # Subplot 1: Top 15 linguagens
        plt.subplot(2, 2, 1)
        lang_counts = self.dataframe['language'].value_counts().head(15)
        plt.barh(range(len(lang_counts)), lang_counts.values, color='lightcoral')
        plt.yticks(range(len(lang_counts)), lang_counts.index)
        plt.xlabel('Número de Repositórios')
        plt.title('RQ05: Top 15 Linguagens')
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Pie chart das top 10
        plt.subplot(2, 2, 2)
        top_10_langs = self.dataframe['language'].value_counts().head(10)
        others_count = len(self.dataframe) - top_10_langs.sum()
        
        if others_count > 0:
            labels = list(top_10_langs.index) + ['Outras']
            sizes = list(top_10_langs.values) + [others_count]
        else:
            labels = top_10_langs.index
            sizes = top_10_langs.values
            
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Distribuição de Linguagens (Top 10)')
        
        # Subplot 3: Linguagens vs Stars
        plt.subplot(2, 2, 3)
        top_5_langs = self.dataframe['language'].value_counts().head(5).index
        lang_data = []
        lang_labels = []
        
        for lang in top_5_langs:
            lang_repos = self.dataframe[self.dataframe['language'] == lang]['stars']
            if len(lang_repos) > 0:
                lang_data.append(lang_repos)
                lang_labels.append(lang)
        
        if lang_data:
            plt.boxplot(lang_data, labels=lang_labels)
            plt.ylabel('Estrelas (escala log)')
            plt.title('Popularidade por Linguagem (Top 5)')
            plt.yscale('log')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
        
        # Subplot 4: Tabela resumo
        plt.subplot(2, 2, 4)
        plt.axis('off')
        
        # Criar tabela com estatísticas
        stats_data = []
        for lang in lang_counts.head(10).index:
            lang_df = self.dataframe[self.dataframe['language'] == lang]
            stats_data.append([
                lang,
                len(lang_df),
                f"{lang_df['stars'].median():.0f}",
                f"{lang_df['age_years'].median():.1f}"
            ])
        
        table = plt.table(cellText=stats_data,
                         colLabels=['Linguagem', 'Repos', 'Stars (med)', 'Idade (anos)'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
        plt.title('Estatísticas por Linguagem', y=0.95)
        
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'rq05_languages.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_issues_closure_plot(self):
        """
        RQ06: Cria gráfico da taxa de fechamento de issues.
        """
        if self.dataframe is None:
            self.load_data()
        
        plt.figure(figsize=(12, 6))
        
        # Filtrar repositórios com issues
        repos_with_issues = self.dataframe[self.dataframe['total_issues'] > 0]
        
        # Subplot 1: Distribuição da taxa de fechamento
        plt.subplot(1, 2, 1)
        plt.hist(repos_with_issues['issues_closure_rate'], bins=30, alpha=0.7, 
                color='gold', edgecolor='black')
        plt.xlabel('Taxa de Fechamento de Issues')
        plt.ylabel('Frequência')
        plt.title('RQ06: Taxa de Fechamento de Issues')
        plt.axvline(repos_with_issues['issues_closure_rate'].median(), color='red', linestyle='--',
                   label=f'Mediana: {repos_with_issues["issues_closure_rate"].median():.2%}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: Taxa vs Total de Issues
        plt.subplot(1, 2, 2)
        plt.scatter(repos_with_issues['total_issues'], repos_with_issues['issues_closure_rate'], 
                   alpha=0.6, color='darkgreen')
        plt.xlabel('Total de Issues (escala log)')
        plt.ylabel('Taxa de Fechamento')
        plt.title('Taxa de Fechamento vs Total de Issues')
        plt.xscale('log')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'rq06_issues_closure.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_correlation_matrix(self):
        """
        Cria matriz de correlação entre as métricas.
        """
        if self.dataframe is None:
            self.load_data()
        
        # Selecionar colunas numéricas relevantes
        numeric_cols = ['stars', 'forks', 'merged_pull_requests', 'releases', 
                       'age_years', 'days_since_update', 'issues_closure_rate', 'total_issues']
        
        correlation_data = self.dataframe[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(correlation_data, dtype=bool))
        sns.heatmap(correlation_data, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('Matriz de Correlação entre Métricas')
        plt.tight_layout()
        
        # Salvar
        filepath = os.path.join(self.plots_dir, 'correlation_matrix.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_all_plots(self):
        """
        Gera todos os gráficos e retorna lista dos caminhos dos arquivos.
        """
        print("=== GERANDO VISUALIZAÇÕES ===")
        
        plots = []
        
        print("Criando gráfico RQ01 (Idade dos repositórios)...")
        plots.append(self.create_age_distribution_plot())
        
        print("Criando gráfico RQ02 (Pull requests aceitas)...")
        plots.append(self.create_pull_requests_plot())
        
        print("Criando gráfico RQ03 (Releases)...")
        plots.append(self.create_releases_plot())
        
        print("Criando gráfico RQ04 (Frequência de atualização)...")
        plots.append(self.create_update_frequency_plot())
        
        print("Criando gráfico RQ05 (Linguagens)...")
        plots.append(self.create_languages_plot())
        
        print("Criando gráfico RQ06 (Taxa de fechamento de issues)...")
        plots.append(self.create_issues_closure_plot())
        
        print("Criando matriz de correlação...")
        plots.append(self.create_correlation_matrix())
        
        print(f"{len(plots)} gráficos criados em: {self.plots_dir}")
        return plots
