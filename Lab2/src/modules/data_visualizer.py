"""
Módulo de Visualização de Dados - Lab 02
Responsável por gerar gráficos e visualizações para análise das questões de pesquisa.
Inclui gráficos de correlação, scatter plots e heatmaps.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime


class DataVisualizer:
    """Classe para geração de visualizações dos dados de qualidade."""
    
    def __init__(self, dataframe, output_dir):
        """
        Inicializa o visualizador.
        
        Args:
            dataframe: DataFrame com os dados dos repositórios
            output_dir: Diretório para salvar os gráficos
        """
        self.df = dataframe
        self.output_dir = output_dir
        
        # Criar diretório de plots
        self.plots_dir = os.path.join(output_dir, 'plots')
        os.makedirs(self.plots_dir, exist_ok=True)
        
        # Configurar estilo dos gráficos
        self._setup_plot_style()
        
        # Definir paleta de cores
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'neutral': '#6C757D'
        }
    
    def _setup_plot_style(self):
        """Configura o estilo dos gráficos."""
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Configurações globais
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 9
    
    def generate_all_visualizations(self, analysis_results=None):
        """Gera todas as visualizações necessárias para o laboratório."""
        print("\nGerando visualizações...")
        print("=" * 30)
        
        generated_plots = {}
        
        # 1. Matriz de correlação geral
        print("Gerando matriz de correlação...")
        correlation_plot = self.plot_correlation_matrix()
        if correlation_plot:
            generated_plots['correlation_matrix'] = correlation_plot
        
        # 2. Gráficos para cada questão de pesquisa
        rq_plots = self.plot_research_questions()
        generated_plots.update(rq_plots)
        
        # 3. Distribuições das métricas principais
        print("Gerando gráficos de distribuição...")
        distribution_plots = self.plot_metric_distributions()
        generated_plots.update(distribution_plots)
        
        # 4. Scatter plots das correlações mais importantes
        print("Gerando scatter plots...")
        scatter_plots = self.plot_correlation_scatterplots()
        generated_plots.update(scatter_plots)
        
        print(f"Visualizações salvas em: {self.plots_dir}")
        print(f"Total de gráficos gerados: {len(generated_plots)}")
        
        return generated_plots
    
    def plot_correlation_matrix(self):
        """Gera heatmap da matriz de correlação entre todas as métricas."""
        # Selecionar métricas relevantes
        metrics = [
            'stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years',
            'loc_total', 'classes_count', 'methods_count',
            'cbo_avg', 'dit_avg', 'lcom_avg'
        ]
        
        # Filtrar apenas colunas disponíveis
        available_metrics = [m for m in metrics if m in self.df.columns]
        
        if len(available_metrics) < 3:
            print("Métricas insuficientes para matriz de correlação")
            return None
        
        # Calcular correlação
        corr_matrix = self.df[available_metrics].corr()
        
        # Criar figura
        plt.figure(figsize=(14, 10))
        
        # Gerar heatmap
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Máscara para mostrar apenas metade
        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=True,
            cmap='RdBu_r',
            center=0,
            square=True,
            fmt='.2f',
            cbar_kws={'label': 'Correlação de Pearson'}
        )
        
        plt.title('Matriz de Correlação entre Métricas de Processo e Qualidade', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Métricas', fontweight='bold')
        plt.ylabel('Métricas', fontweight='bold')
        
        # Salvar
        filename = os.path.join(self.plots_dir, 'correlation_matrix.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_research_questions(self):
        """Gera gráficos específicos para cada questão de pesquisa."""
        plots = {}
        
        # RQ01: Popularidade vs Qualidade
        rq01_plot = self._plot_rq01_popularity_quality()
        if rq01_plot:
            plots['rq01_popularity_quality'] = rq01_plot
        
        # RQ02: Maturidade vs Qualidade
        rq02_plot = self._plot_rq02_maturity_quality()
        if rq02_plot:
            plots['rq02_maturity_quality'] = rq02_plot
        
        # RQ03: Atividade vs Qualidade
        rq03_plot = self._plot_rq03_activity_quality()
        if rq03_plot:
            plots['rq03_activity_quality'] = rq03_plot
        
        # RQ04: Tamanho vs Qualidade
        rq04_plot = self._plot_rq04_size_quality()
        if rq04_plot:
            plots['rq04_size_quality'] = rq04_plot
        
        return plots
    
    def _plot_rq01_popularity_quality(self):
        """RQ01: Relação entre popularidade e qualidade."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('RQ01: Popularidade vs Qualidade', fontsize=16, fontweight='bold')
        
        # Stars vs CBO
        if 'stars' in self.df.columns and 'cbo_avg' in self.df.columns:
            axes[0, 0].scatter(self.df['stars'], self.df['cbo_avg'], alpha=0.6, color=self.colors['primary'])
            axes[0, 0].set_xlabel('Estrelas')
            axes[0, 0].set_ylabel('CBO Médio')
            axes[0, 0].set_title('Estrelas vs Acoplamento (CBO)')
            self._add_trend_line(axes[0, 0], self.df['stars'], self.df['cbo_avg'])
        
        # Stars vs DIT
        if 'stars' in self.df.columns and 'dit_avg' in self.df.columns:
            axes[0, 1].scatter(self.df['stars'], self.df['dit_avg'], alpha=0.6, color=self.colors['secondary'])
            axes[0, 1].set_xlabel('Estrelas')
            axes[0, 1].set_ylabel('DIT Médio')
            axes[0, 1].set_title('Estrelas vs Profundidade de Herança (DIT)')
            self._add_trend_line(axes[0, 1], self.df['stars'], self.df['dit_avg'])
        
        # Stars vs LCOM
        if 'stars' in self.df.columns and 'lcom_avg' in self.df.columns:
            axes[1, 0].scatter(self.df['stars'], self.df['lcom_avg'], alpha=0.6, color=self.colors['accent'])
            axes[1, 0].set_xlabel('Estrelas')
            axes[1, 0].set_ylabel('LCOM Médio')
            axes[1, 0].set_title('Estrelas vs Falta de Coesão (LCOM)')
            self._add_trend_line(axes[1, 0], self.df['stars'], self.df['lcom_avg'])
        
        # Forks vs CBO
        if 'forks' in self.df.columns and 'cbo_avg' in self.df.columns:
            axes[1, 1].scatter(self.df['forks'], self.df['cbo_avg'], alpha=0.6, color=self.colors['success'])
            axes[1, 1].set_xlabel('Forks')
            axes[1, 1].set_ylabel('CBO Médio')
            axes[1, 1].set_title('Forks vs Acoplamento (CBO)')
            self._add_trend_line(axes[1, 1], self.df['forks'], self.df['cbo_avg'])
        
        plt.tight_layout()
        filename = os.path.join(self.plots_dir, 'rq01_popularity_quality.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _plot_rq02_maturity_quality(self):
        """RQ02: Relação entre maturidade e qualidade."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('RQ02: Maturidade vs Qualidade', fontsize=16, fontweight='bold')
        
        # Age vs CBO
        if 'age_years' in self.df.columns and 'cbo_avg' in self.df.columns:
            axes[0].scatter(self.df['age_years'], self.df['cbo_avg'], alpha=0.6, color=self.colors['primary'])
            axes[0].set_xlabel('Idade (anos)')
            axes[0].set_ylabel('CBO Médio')
            axes[0].set_title('Idade vs Acoplamento (CBO)')
            self._add_trend_line(axes[0], self.df['age_years'], self.df['cbo_avg'])
        
        # Age vs DIT
        if 'age_years' in self.df.columns and 'dit_avg' in self.df.columns:
            axes[1].scatter(self.df['age_years'], self.df['dit_avg'], alpha=0.6, color=self.colors['secondary'])
            axes[1].set_xlabel('Idade (anos)')
            axes[1].set_ylabel('DIT Médio')
            axes[1].set_title('Idade vs Profundidade de Herança (DIT)')
            self._add_trend_line(axes[1], self.df['age_years'], self.df['dit_avg'])
        
        # Age vs LCOM
        if 'age_years' in self.df.columns and 'lcom_avg' in self.df.columns:
            axes[2].scatter(self.df['age_years'], self.df['lcom_avg'], alpha=0.6, color=self.colors['accent'])
            axes[2].set_xlabel('Idade (anos)')
            axes[2].set_ylabel('LCOM Médio')
            axes[2].set_title('Idade vs Falta de Coesão (LCOM)')
            self._add_trend_line(axes[2], self.df['age_years'], self.df['lcom_avg'])
        
        plt.tight_layout()
        filename = os.path.join(self.plots_dir, 'rq02_maturity_quality.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _plot_rq03_activity_quality(self):
        """RQ03: Relação entre atividade e qualidade."""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('RQ03: Atividade vs Qualidade', fontsize=16, fontweight='bold')
        
        # Releases vs Quality metrics
        if 'releases' in self.df.columns:
            if 'cbo_avg' in self.df.columns:
                axes[0, 0].scatter(self.df['releases'], self.df['cbo_avg'], alpha=0.6, color=self.colors['primary'])
                axes[0, 0].set_xlabel('Número de Releases')
                axes[0, 0].set_ylabel('CBO Médio')
                axes[0, 0].set_title('Releases vs Acoplamento (CBO)')
                self._add_trend_line(axes[0, 0], self.df['releases'], self.df['cbo_avg'])
            
            if 'dit_avg' in self.df.columns:
                axes[0, 1].scatter(self.df['releases'], self.df['dit_avg'], alpha=0.6, color=self.colors['secondary'])
                axes[0, 1].set_xlabel('Número de Releases')
                axes[0, 1].set_ylabel('DIT Médio')
                axes[0, 1].set_title('Releases vs Profundidade de Herança (DIT)')
                self._add_trend_line(axes[0, 1], self.df['releases'], self.df['dit_avg'])
            
            if 'lcom_avg' in self.df.columns:
                axes[0, 2].scatter(self.df['releases'], self.df['lcom_avg'], alpha=0.6, color=self.colors['accent'])
                axes[0, 2].set_xlabel('Número de Releases')
                axes[0, 2].set_ylabel('LCOM Médio')
                axes[0, 2].set_title('Releases vs Falta de Coesão (LCOM)')
                self._add_trend_line(axes[0, 2], self.df['releases'], self.df['lcom_avg'])
        
        # Contributors vs Quality metrics
        if 'contributors' in self.df.columns:
            if 'cbo_avg' in self.df.columns:
                axes[1, 0].scatter(self.df['contributors'], self.df['cbo_avg'], alpha=0.6, color=self.colors['primary'])
                axes[1, 0].set_xlabel('Número de Contribuidores')
                axes[1, 0].set_ylabel('CBO Médio')
                axes[1, 0].set_title('Contribuidores vs Acoplamento (CBO)')
                self._add_trend_line(axes[1, 0], self.df['contributors'], self.df['cbo_avg'])
            
            if 'dit_avg' in self.df.columns:
                axes[1, 1].scatter(self.df['contributors'], self.df['dit_avg'], alpha=0.6, color=self.colors['secondary'])
                axes[1, 1].set_xlabel('Número de Contribuidores')
                axes[1, 1].set_ylabel('DIT Médio')
                axes[1, 1].set_title('Contribuidores vs Profundidade de Herança (DIT)')
                self._add_trend_line(axes[1, 1], self.df['contributors'], self.df['dit_avg'])
            
            if 'lcom_avg' in self.df.columns:
                axes[1, 2].scatter(self.df['contributors'], self.df['lcom_avg'], alpha=0.6, color=self.colors['accent'])
                axes[1, 2].set_xlabel('Número de Contribuidores')
                axes[1, 2].set_ylabel('LCOM Médio')
                axes[1, 2].set_title('Contribuidores vs Falta de Coesão (LCOM)')
                self._add_trend_line(axes[1, 2], self.df['contributors'], self.df['lcom_avg'])
        
        plt.tight_layout()
        filename = os.path.join(self.plots_dir, 'rq03_activity_quality.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def _plot_rq04_size_quality(self):
        """RQ04: Relação entre tamanho e qualidade."""
        fig, axes = plt.subplots(3, 3, figsize=(18, 18))
        fig.suptitle('RQ04: Tamanho vs Qualidade', fontsize=16, fontweight='bold')
        
        size_metrics = ['loc_total', 'classes_count', 'methods_count']
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg']
        
        for i, size_metric in enumerate(size_metrics):
            for j, quality_metric in enumerate(quality_metrics):
                if size_metric in self.df.columns and quality_metric in self.df.columns:
                    axes[i, j].scatter(self.df[size_metric], self.df[quality_metric], 
                                     alpha=0.6, color=self.colors['primary'])
                    axes[i, j].set_xlabel(self._get_metric_label(size_metric))
                    axes[i, j].set_ylabel(self._get_metric_label(quality_metric))
                    axes[i, j].set_title(f'{self._get_metric_label(size_metric)} vs {self._get_metric_label(quality_metric)}')
                    self._add_trend_line(axes[i, j], self.df[size_metric], self.df[quality_metric])
        
        plt.tight_layout()
        filename = os.path.join(self.plots_dir, 'rq04_size_quality.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def plot_metric_distributions(self):
        """Gera gráficos de distribuição das métricas principais."""
        plots = {}
        
        # Métricas de processo
        process_metrics = ['stars', 'forks', 'age_years', 'releases', 'contributors']
        available_process = [m for m in process_metrics if m in self.df.columns]
        
        if available_process:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Distribuição das Métricas de Processo', fontsize=16, fontweight='bold')
            
            for i, metric in enumerate(available_process[:6]):
                row, col = i // 3, i % 3
                if i < 6:
                    data = self.df[metric].dropna()
                    axes[row, col].hist(data, bins=30, alpha=0.7, color=self.colors['primary'])
                    axes[row, col].set_xlabel(self._get_metric_label(metric))
                    axes[row, col].set_ylabel('Frequência')
                    axes[row, col].set_title(f'Distribuição: {self._get_metric_label(metric)}')
                    
                    # Adicionar estatísticas
                    mean_val = data.mean()
                    median_val = data.median()
                    axes[row, col].axvline(mean_val, color='red', linestyle='--', label=f'Média: {mean_val:.1f}')
                    axes[row, col].axvline(median_val, color='orange', linestyle='--', label=f'Mediana: {median_val:.1f}')
                    axes[row, col].legend()
            
            # Remover subplots vazios
            for i in range(len(available_process), 6):
                row, col = i // 3, i % 3
                fig.delaxes(axes[row, col])
            
            plt.tight_layout()
            filename = os.path.join(self.plots_dir, 'metric_distributions_process.png')
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
            plots['distributions_process'] = filename
        
        # Métricas de qualidade
        quality_metrics = ['cbo_avg', 'dit_avg', 'lcom_avg', 'loc_total', 'classes_count']
        available_quality = [m for m in quality_metrics if m in self.df.columns]
        
        if available_quality:
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Distribuição das Métricas de Qualidade', fontsize=16, fontweight='bold')
            
            for i, metric in enumerate(available_quality[:6]):
                row, col = i // 3, i % 3
                if i < 6:
                    data = self.df[metric].dropna()
                    axes[row, col].hist(data, bins=30, alpha=0.7, color=self.colors['secondary'])
                    axes[row, col].set_xlabel(self._get_metric_label(metric))
                    axes[row, col].set_ylabel('Frequência')
                    axes[row, col].set_title(f'Distribuição: {self._get_metric_label(metric)}')
                    
                    # Adicionar estatísticas
                    mean_val = data.mean()
                    median_val = data.median()
                    axes[row, col].axvline(mean_val, color='red', linestyle='--', label=f'Média: {mean_val:.1f}')
                    axes[row, col].axvline(median_val, color='orange', linestyle='--', label=f'Mediana: {median_val:.1f}')
                    axes[row, col].legend()
            
            # Remover subplots vazios
            for i in range(len(available_quality), 6):
                row, col = i // 3, i % 3
                fig.delaxes(axes[row, col])
            
            plt.tight_layout()
            filename = os.path.join(self.plots_dir, 'metric_distributions_quality.png')
            plt.savefig(filename, bbox_inches='tight')
            plt.close()
            plots['distributions_quality'] = filename
        
        return plots
    
    def plot_correlation_scatterplots(self):
        """Gera scatter plots das correlações mais importantes."""
        plots = {}
        
        # Correlações importantes baseadas nas questões de pesquisa
        important_correlations = [
            ('stars', 'cbo_avg', 'Popularidade vs Acoplamento'),
            ('age_years', 'dit_avg', 'Maturidade vs Profundidade de Herança'),
            ('releases', 'lcom_avg', 'Atividade vs Coesão'),
            ('loc_total', 'cbo_avg', 'Tamanho vs Acoplamento')
        ]
        
        for x_var, y_var, title in important_correlations:
            if x_var in self.df.columns and y_var in self.df.columns:
                plt.figure(figsize=(10, 8))
                
                # Scatter plot
                plt.scatter(self.df[x_var], self.df[y_var], alpha=0.6, color=self.colors['primary'])
                
                # Linha de tendência
                self._add_trend_line(plt.gca(), self.df[x_var], self.df[y_var])
                
                # Calcular correlação
                correlation = self.df[x_var].corr(self.df[y_var])
                
                plt.xlabel(self._get_metric_label(x_var))
                plt.ylabel(self._get_metric_label(y_var))
                plt.title(f'{title}\nCorrelação: {correlation:.3f}', fontweight='bold')
                plt.grid(True, alpha=0.3)
                
                # Salvar
                safe_title = title.replace(' ', '_').replace('vs', '').replace(',', '').lower()
                filename = os.path.join(self.plots_dir, f'scatter_{safe_title}.png')
                plt.savefig(filename, bbox_inches='tight')
                plt.close()
                
                plots[f'scatter_{safe_title}'] = filename
        
        return plots
    
    def _add_trend_line(self, ax, x, y):
        """Adiciona linha de tendência ao gráfico."""
        # Remover valores NaN
        mask = ~(pd.isna(x) | pd.isna(y))
        x_clean = x[mask]
        y_clean = y[mask]
        
        if len(x_clean) > 1:
            # Calcular linha de tendência
            z = np.polyfit(x_clean, y_clean, 1)
            p = np.poly1d(z)
            ax.plot(x_clean, p(x_clean), "r--", alpha=0.8, linewidth=2)
    
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
            'cbo_max': 'CBO Máximo',
            'dit_avg': 'DIT Médio',
            'dit_max': 'DIT Máximo',
            'lcom_avg': 'LCOM Médio',
            'lcom_max': 'LCOM Máximo',
            'wmc_avg': 'WMC Médio',
            'noc_avg': 'NOC Médio',
            'cc_avg': 'Complexidade Ciclomática Média'
        }
        return labels.get(metric, metric.replace('_', ' ').title())
    
    def generate_summary_plot(self):
        """Gera um gráfico resumo com as principais descobertas."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Resumo: Qualidade de Software em Repositórios Java', fontsize=16, fontweight='bold')
        
        # 1. Top repositórios por popularidade
        if 'stars' in self.df.columns and 'name' in self.df.columns:
            top_repos = self.df.nlargest(10, 'stars')
            ax1.barh(range(len(top_repos)), top_repos['stars'], color=self.colors['primary'])
            ax1.set_yticks(range(len(top_repos)))
            ax1.set_yticklabels([name.split('/')[-1][:15] for name in top_repos['name']], fontsize=8)
            ax1.set_xlabel('Estrelas')
            ax1.set_title('Top 10 Repositórios Mais Populares')
        
        # 2. Distribuição de qualidade geral
        if 'cbo_avg' in self.df.columns:
            cbo_data = self.df['cbo_avg'].dropna()
            ax2.hist(cbo_data, bins=20, alpha=0.7, color=self.colors['secondary'])
            ax2.set_xlabel('CBO Médio')
            ax2.set_ylabel('Frequência')
            ax2.set_title('Distribuição do Acoplamento (CBO)')
            ax2.axvline(cbo_data.mean(), color='red', linestyle='--', label=f'Média: {cbo_data.mean():.2f}')
            ax2.legend()
        
        # 3. Relação tamanho vs qualidade
        if 'loc_total' in self.df.columns and 'cbo_avg' in self.df.columns:
            ax3.scatter(self.df['loc_total'], self.df['cbo_avg'], alpha=0.6, color=self.colors['accent'])
            ax3.set_xlabel('Linhas de Código')
            ax3.set_ylabel('CBO Médio')
            ax3.set_title('Tamanho vs Acoplamento')
            self._add_trend_line(ax3, self.df['loc_total'], self.df['cbo_avg'])
        
        # 4. Maturidade vs qualidade
        if 'age_years' in self.df.columns and 'lcom_avg' in self.df.columns:
            ax4.scatter(self.df['age_years'], self.df['lcom_avg'], alpha=0.6, color=self.colors['success'])
            ax4.set_xlabel('Idade (anos)')
            ax4.set_ylabel('LCOM Médio')
            ax4.set_title('Maturidade vs Coesão')
            self._add_trend_line(ax4, self.df['age_years'], self.df['lcom_avg'])
        
        plt.tight_layout()
        filename = os.path.join(self.plots_dir, 'summary_analysis.png')
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        
        return filename
