"""
Módulo para visualização de dados dos Pull Requests
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..config.config import Config

logger = logging.getLogger(__name__)

class DataVisualizer:
    """Classe para criar visualizações dos dados de Pull Requests"""
    
    def __init__(self):
        self.plots_dir = Config.PLOTS_DIR
        self.plots_dir.mkdir(exist_ok=True)
        
        # Configurações de estilo
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_all_visualizations(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Cria todas as visualizações necessárias para o relatório
        
        Args:
            df: DataFrame com dados dos PRs
            analysis_results: Resultados das análises estatísticas
            
        Returns:
            Dicionário com caminhos dos arquivos de plot salvos
        """
        logger.info("Criando visualizações...")
        
        plot_files = {}
        
        # 1. Visualizações descritivas do dataset
        plot_files.update(self._create_descriptive_plots(df))
        
        # 2. Visualizações das questões de pesquisa - Grupo A (Feedback)
        plot_files.update(self._create_feedback_plots(df, analysis_results))
        
        # 3. Visualizações das questões de pesquisa - Grupo B (Reviews)
        plot_files.update(self._create_reviews_plots(df, analysis_results))
        
        # 4. Matriz de correlação
        plot_files.update(self._create_correlation_plots(df, analysis_results))
        
        # 5. Visualizações interativas (Plotly)
        plot_files.update(self._create_interactive_plots(df))
        
        logger.info(f"Visualizações criadas: {len(plot_files)} arquivos salvos")
        return plot_files
    
    def _create_descriptive_plots(self, df: pd.DataFrame) -> Dict[str, str]:
        """Cria plots descritivos do dataset"""
        plot_files = {}
        
        # 1. Distribuição do status final dos PRs
        plt.figure(figsize=(10, 6))
        status_counts = df['final_status'].value_counts()
        
        plt.subplot(1, 2, 1)
        status_counts.plot(kind='bar', color=['#2ecc71', '#e74c3c'])
        plt.title('Distribuição do Status Final dos PRs')
        plt.ylabel('Quantidade de PRs')
        plt.xticks(rotation=45)
        
        plt.subplot(1, 2, 2)
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                colors=['#2ecc71', '#e74c3c'])
        plt.title('Proporção de PRs por Status')
        
        plt.tight_layout()
        plot_path = self.plots_dir / '01_status_distribution.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        plot_files['status_distribution'] = str(plot_path)
        
        # 2. Distribuições das métricas de tamanho
        if 'total_changes' in df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Total de mudanças
            axes[0,0].hist(df['total_changes'].dropna(), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            axes[0,0].set_title('Distribuição: Total de Mudanças')
            axes[0,0].set_xlabel('Total de Mudanças (log scale)')
            axes[0,0].set_ylabel('Frequência')
            axes[0,0].set_xscale('log')
            
            # Arquivos modificados
            if 'files_changed' in df.columns:
                axes[0,1].hist(df['files_changed'].dropna(), bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
                axes[0,1].set_title('Distribuição: Arquivos Modificados')
                axes[0,1].set_xlabel('Número de Arquivos')
                axes[0,1].set_ylabel('Frequência')
            
            # Tempo de análise
            if 'analysis_time_hours' in df.columns:
                axes[1,0].hist(df['analysis_time_hours'].dropna(), bins=50, alpha=0.7, color='orange', edgecolor='black')
                axes[1,0].set_title('Distribuição: Tempo de Análise')
                axes[1,0].set_xlabel('Tempo (horas, log scale)')
                axes[1,0].set_ylabel('Frequência')
                axes[1,0].set_xscale('log')
            
            # Número de revisões
            if 'reviews_count' in df.columns:
                axes[1,1].hist(df['reviews_count'].dropna(), bins=20, alpha=0.7, color='purple', edgecolor='black')
                axes[1,1].set_title('Distribuição: Número de Revisões')
                axes[1,1].set_xlabel('Número de Revisões')
                axes[1,1].set_ylabel('Frequência')
            
            plt.tight_layout()
            plot_path = self.plots_dir / '02_metrics_distributions.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['metrics_distributions'] = str(plot_path)
        
        return plot_files
    
    def _create_feedback_plots(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Cria plots para análise de feedback final (RQ01-RQ04)"""
        plot_files = {}
        
        # RQ01: Tamanho vs Feedback
        if 'total_changes' in df.columns and 'final_status' in df.columns:
            plt.figure(figsize=(15, 10))
            
            # Box plots para cada métrica de tamanho
            size_metrics = ['total_changes', 'files_changed', 'additions', 'deletions']
            available_metrics = [m for m in size_metrics if m in df.columns]
            
            for i, metric in enumerate(available_metrics, 1):
                plt.subplot(2, 2, i)
                
                # Preparar dados
                merged_data = df[df['final_status'] == 'MERGED'][metric].dropna()
                closed_data = df[df['final_status'] == 'CLOSED'][metric].dropna()
                
                data_to_plot = [merged_data, closed_data]
                labels = ['MERGED', 'CLOSED']
                
                box_plot = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
                box_plot['boxes'][0].set_facecolor('#2ecc71')
                box_plot['boxes'][1].set_facecolor('#e74c3c')
                
                plt.title(f'RQ01: {metric} por Status Final')
                plt.ylabel(metric.replace('_', ' ').title())
                plt.yscale('log' if metric in ['total_changes', 'additions', 'deletions'] else 'linear')
                
                # Adicionar informações estatísticas
                merged_median = merged_data.median() if len(merged_data) > 0 else 0
                closed_median = closed_data.median() if len(closed_data) > 0 else 0
                plt.text(0.02, 0.98, f'Mediana MERGED: {merged_median:.1f}\\nMediana CLOSED: {closed_median:.1f}', 
                        transform=plt.gca().transAxes, verticalalignment='top', fontsize=8,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            plot_path = self.plots_dir / '03_rq01_size_vs_feedback.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq01_size_feedback'] = str(plot_path)
        
        # RQ02: Tempo vs Feedback
        if 'analysis_time_hours' in df.columns and 'final_status' in df.columns:
            plt.figure(figsize=(12, 6))
            
            plt.subplot(1, 2, 1)
            # Box plot
            merged_time = df[df['final_status'] == 'MERGED']['analysis_time_hours'].dropna()
            closed_time = df[df['final_status'] == 'CLOSED']['analysis_time_hours'].dropna()
            
            data_to_plot = [merged_time, closed_time]
            labels = ['MERGED', 'CLOSED']
            
            box_plot = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
            box_plot['boxes'][0].set_facecolor('#2ecc71')
            box_plot['boxes'][1].set_facecolor('#e74c3c')
            
            plt.title('RQ02: Tempo de Análise por Status Final')
            plt.ylabel('Tempo de Análise (horas, log scale)')
            plt.yscale('log')
            
            plt.subplot(1, 2, 2)
            # Histograma sobreposto
            plt.hist(merged_time, bins=50, alpha=0.6, label='MERGED', color='#2ecc71', density=True)
            plt.hist(closed_time, bins=50, alpha=0.6, label='CLOSED', color='#e74c3c', density=True)
            plt.xlabel('Tempo de Análise (horas, log scale)')
            plt.ylabel('Densidade')
            plt.xscale('log')
            plt.legend()
            plt.title('Distribuição do Tempo por Status')
            
            plt.tight_layout()
            plot_path = self.plots_dir / '04_rq02_time_vs_feedback.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq02_time_feedback'] = str(plot_path)
        
        # RQ03: Descrição vs Feedback
        if 'description_length' in df.columns and 'final_status' in df.columns:
            plt.figure(figsize=(12, 6))
            
            plt.subplot(1, 2, 1)
            # Box plot para comprimento da descrição
            merged_desc = df[df['final_status'] == 'MERGED']['description_length'].dropna()
            closed_desc = df[df['final_status'] == 'CLOSED']['description_length'].dropna()
            
            data_to_plot = [merged_desc, closed_desc]
            labels = ['MERGED', 'CLOSED']
            
            box_plot = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
            box_plot['boxes'][0].set_facecolor('#2ecc71')
            box_plot['boxes'][1].set_facecolor('#e74c3c')
            
            plt.title('RQ03: Comprimento da Descrição por Status')
            plt.ylabel('Comprimento da Descrição (caracteres)')
            
            plt.subplot(1, 2, 2)
            # Proporção de PRs com/sem descrição por status
            if 'has_description' in df.columns:
                crosstab = pd.crosstab(df['final_status'], df['has_description'], normalize='index') * 100
                crosstab.plot(kind='bar', ax=plt.gca(), color=['#e74c3c', '#2ecc71'])
                plt.title('Proporção de PRs com Descrição por Status')
                plt.ylabel('Porcentagem (%)')
                plt.xlabel('Status Final')
                plt.legend(['Sem Descrição', 'Com Descrição'])
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            plot_path = self.plots_dir / '05_rq03_description_vs_feedback.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq03_description_feedback'] = str(plot_path)
        
        # RQ04: Interações vs Feedback
        interaction_metrics = ['participants_count', 'total_comments']
        available_metrics = [m for m in interaction_metrics if m in df.columns]
        
        if available_metrics and 'final_status' in df.columns:
            fig, axes = plt.subplots(1, len(available_metrics), figsize=(6*len(available_metrics), 6))
            if len(available_metrics) == 1:
                axes = [axes]
            
            for i, metric in enumerate(available_metrics):
                merged_data = df[df['final_status'] == 'MERGED'][metric].dropna()
                closed_data = df[df['final_status'] == 'CLOSED'][metric].dropna()
                
                data_to_plot = [merged_data, closed_data]
                labels = ['MERGED', 'CLOSED']
                
                box_plot = axes[i].boxplot(data_to_plot, labels=labels, patch_artist=True)
                box_plot['boxes'][0].set_facecolor('#2ecc71')
                box_plot['boxes'][1].set_facecolor('#e74c3c')
                
                axes[i].set_title(f'RQ04: {metric.replace("_", " ").title()} por Status')
                axes[i].set_ylabel(metric.replace('_', ' ').title())
            
            plt.tight_layout()
            plot_path = self.plots_dir / '06_rq04_interactions_vs_feedback.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq04_interactions_feedback'] = str(plot_path)
        
        return plot_files
    
    def _create_reviews_plots(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Cria plots para análise de número de revisões (RQ05-RQ08)"""
        plot_files = {}
        
        if 'reviews_count' not in df.columns:
            logger.warning("Coluna 'reviews_count' não encontrada. Pulando plots de revisões.")
            return plot_files
        
        # RQ05: Tamanho vs Número de Revisões (Scatter plots)
        size_metrics = ['total_changes', 'files_changed']
        available_metrics = [m for m in size_metrics if m in df.columns]
        
        if available_metrics:
            fig, axes = plt.subplots(1, len(available_metrics), figsize=(7*len(available_metrics), 6))
            if len(available_metrics) == 1:
                axes = [axes]
            
            for i, metric in enumerate(available_metrics):
                # Remove outliers para visualização mais clara
                clean_data = df[[metric, 'reviews_count']].dropna()
                
                # Remove outliers extremos
                q99_x = clean_data[metric].quantile(0.99)
                q99_y = clean_data['reviews_count'].quantile(0.99)
                clean_data = clean_data[(clean_data[metric] <= q99_x) & (clean_data['reviews_count'] <= q99_y)]
                
                axes[i].scatter(clean_data[metric], clean_data['reviews_count'], alpha=0.6, s=20)
                axes[i].set_xlabel(metric.replace('_', ' ').title())
                axes[i].set_ylabel('Número de Revisões')
                axes[i].set_title(f'RQ05: {metric.replace("_", " ").title()} vs Revisões')
                
                # Linha de tendência
                if len(clean_data) > 10:
                    z = np.polyfit(clean_data[metric], clean_data['reviews_count'], 1)
                    p = np.poly1d(z)
                    axes[i].plot(clean_data[metric].sort_values(), p(clean_data[metric].sort_values()), "r--", alpha=0.8)
                
                # Correlação no gráfico
                if metric in analysis_results.get('rq_b_reviews', {}).get('rq05_size_vs_reviews', {}).get('correlations', {}):
                    corr_data = analysis_results['rq_b_reviews']['rq05_size_vs_reviews']['correlations'][metric]
                    spearman_corr = corr_data['spearman']['correlation']
                    axes[i].text(0.05, 0.95, f'ρ = {spearman_corr:.3f}', transform=axes[i].transAxes, 
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            plot_path = self.plots_dir / '07_rq05_size_vs_reviews.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq05_size_reviews'] = str(plot_path)
        
        # RQ06: Tempo vs Número de Revisões
        if 'analysis_time_hours' in df.columns:
            plt.figure(figsize=(10, 6))
            
            clean_data = df[['analysis_time_hours', 'reviews_count']].dropna()
            
            # Remove outliers
            q95_time = clean_data['analysis_time_hours'].quantile(0.95)
            q95_reviews = clean_data['reviews_count'].quantile(0.95)
            clean_data = clean_data[(clean_data['analysis_time_hours'] <= q95_time) & 
                                  (clean_data['reviews_count'] <= q95_reviews)]
            
            plt.scatter(clean_data['analysis_time_hours'], clean_data['reviews_count'], alpha=0.6, s=30)
            plt.xlabel('Tempo de Análise (horas)')
            plt.ylabel('Número de Revisões')
            plt.title('RQ06: Tempo de Análise vs Número de Revisões')
            
            # Linha de tendência
            if len(clean_data) > 10:
                z = np.polyfit(clean_data['analysis_time_hours'], clean_data['reviews_count'], 1)
                p = np.poly1d(z)
                plt.plot(clean_data['analysis_time_hours'].sort_values(), 
                        p(clean_data['analysis_time_hours'].sort_values()), "r--", alpha=0.8)
            
            plt.tight_layout()
            plot_path = self.plots_dir / '08_rq06_time_vs_reviews.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['rq06_time_reviews'] = str(plot_path)
        
        return plot_files
    
    def _create_correlation_plots(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Cria visualizações da matriz de correlação"""
        plot_files = {}
        
        correlation_data = analysis_results.get('correlation_analysis', {})
        
        if 'spearman_matrix' in correlation_data:
            # Matriz de correlação de Spearman
            spearman_df = pd.DataFrame(correlation_data['spearman_matrix'])
            
            plt.figure(figsize=(12, 10))
            
            # Heatmap
            mask = np.triu(np.ones_like(spearman_df, dtype=bool))
            sns.heatmap(spearman_df, mask=mask, annot=True, cmap='RdBu_r', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .5}, fmt='.2f')
            
            plt.title('Matriz de Correlação de Spearman\\n(Triângulo Superior Removido)')
            plt.tight_layout()
            
            plot_path = self.plots_dir / '09_correlation_matrix_spearman.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            plot_files['correlation_matrix'] = str(plot_path)
        
        return plot_files
    
    def _create_interactive_plots(self, df: pd.DataFrame) -> Dict[str, str]:
        """Cria visualizações interativas com Plotly"""
        plot_files = {}
        
        try:
            # 1. Scatter plot interativo: Tamanho vs Tempo vs Reviews
            if all(col in df.columns for col in ['total_changes', 'analysis_time_hours', 'reviews_count', 'final_status']):
                
                # Remove outliers para melhor visualização
                clean_df = df[['total_changes', 'analysis_time_hours', 'reviews_count', 'final_status']].dropna()
                
                for col in ['total_changes', 'analysis_time_hours', 'reviews_count']:
                    q99 = clean_df[col].quantile(0.99)
                    clean_df = clean_df[clean_df[col] <= q99]
                
                fig = px.scatter_3d(clean_df, 
                                  x='total_changes', 
                                  y='analysis_time_hours', 
                                  z='reviews_count',
                                  color='final_status',
                                  title='Relação 3D: Tamanho vs Tempo vs Revisões',
                                  labels={
                                      'total_changes': 'Total de Mudanças',
                                      'analysis_time_hours': 'Tempo de Análise (horas)',
                                      'reviews_count': 'Número de Revisões',
                                      'final_status': 'Status Final'
                                  },
                                  color_discrete_map={'MERGED': '#2ecc71', 'CLOSED': '#e74c3c'})
                
                plot_path = self.plots_dir / '10_interactive_3d_scatter.html'
                fig.write_html(plot_path)
                plot_files['interactive_3d'] = str(plot_path)
            
            # 2. Dashboard interativo com múltiplos gráficos
            if 'final_status' in df.columns:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=['Distribuição de Status', 'Tamanho por Status', 
                                  'Tempo por Status', 'Revisões por Status'],
                    specs=[[{"type": "pie"}, {"type": "box"}],
                           [{"type": "box"}, {"type": "box"}]]
                )
                
                # Gráfico de pizza para status
                status_counts = df['final_status'].value_counts()
                fig.add_trace(go.Pie(labels=status_counts.index, 
                                   values=status_counts.values,
                                   name="Status",
                                   marker_colors=['#2ecc71', '#e74c3c']),
                            row=1, col=1)
                
                # Box plots para métricas por status
                if 'total_changes' in df.columns:
                    for status in df['final_status'].unique():
                        data = df[df['final_status'] == status]['total_changes'].dropna()
                        fig.add_trace(go.Box(y=data, name=status, 
                                           marker_color='#2ecc71' if status == 'MERGED' else '#e74c3c'),
                                    row=1, col=2)
                
                if 'analysis_time_hours' in df.columns:
                    for status in df['final_status'].unique():
                        data = df[df['final_status'] == status]['analysis_time_hours'].dropna()
                        fig.add_trace(go.Box(y=data, name=status,
                                           marker_color='#2ecc71' if status == 'MERGED' else '#e74c3c'),
                                    row=2, col=1)
                
                if 'reviews_count' in df.columns:
                    for status in df['final_status'].unique():
                        data = df[df['final_status'] == status]['reviews_count'].dropna()
                        fig.add_trace(go.Box(y=data, name=status,
                                           marker_color='#2ecc71' if status == 'MERGED' else '#e74c3c'),
                                    row=2, col=2)
                
                fig.update_layout(height=800, showlegend=False, 
                                title_text="Dashboard Interativo - Análise de Pull Requests")
                
                plot_path = self.plots_dir / '11_interactive_dashboard.html'
                fig.write_html(plot_path)
                plot_files['interactive_dashboard'] = str(plot_path)
                
        except Exception as e:
            logger.error(f"Erro ao criar plots interativos: {e}")
        
        return plot_files
    
    def create_summary_plot(self, analysis_results: Dict[str, Any]) -> str:
        """Cria um plot resumo com os principais resultados"""
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            # Plot 1: Informações do dataset
            dataset_info = analysis_results.get('dataset_info', {})
            
            axes[0,0].bar(['Total PRs', 'Merged', 'Closed'], 
                         [dataset_info.get('total_prs', 0),
                          dataset_info.get('merged_prs', 0), 
                          dataset_info.get('closed_prs', 0)],
                         color=['#3498db', '#2ecc71', '#e74c3c'])
            axes[0,0].set_title('Composição do Dataset')
            axes[0,0].set_ylabel('Quantidade de PRs')
            
            # Plot 2: Taxa de merge
            merge_rate = dataset_info.get('merge_rate', 0)
            axes[0,1].pie([merge_rate, 100-merge_rate], 
                         labels=[f'Merged ({merge_rate:.1f}%)', f'Closed ({100-merge_rate:.1f}%)'],
                         colors=['#2ecc71', '#e74c3c'],
                         autopct='%1.1f%%')
            axes[0,1].set_title('Taxa de Aprovação dos PRs')
            
            # Plot 3: Placeholder para correlações significantes
            axes[1,0].text(0.5, 0.5, 'Correlações Significantes\\n(Ver análise detalhada)', 
                          ha='center', va='center', transform=axes[1,0].transAxes,
                          fontsize=14, bbox=dict(boxstyle='round', facecolor='lightblue'))
            axes[1,0].set_title('Análise de Correlações')
            axes[1,0].set_xticks([])
            axes[1,0].set_yticks([])
            
            # Plot 4: Placeholder para testes estatísticos
            axes[1,1].text(0.5, 0.5, 'Testes Estatísticos\\n(Ver relatório completo)', 
                          ha='center', va='center', transform=axes[1,1].transAxes,
                          fontsize=14, bbox=dict(boxstyle='round', facecolor='lightgreen'))
            axes[1,1].set_title('Resultados dos Testes')
            axes[1,1].set_xticks([])
            axes[1,1].set_yticks([])
            
            plt.suptitle('LABORATÓRIO 03 - Resumo da Análise de Code Review\\nCaracterização da Atividade no GitHub', 
                        fontsize=16, y=0.98)
            plt.tight_layout()
            
            plot_path = self.plots_dir / '00_summary_analysis.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Plot resumo criado: {plot_path}")
            return str(plot_path)
            
        except Exception as e:
            logger.error(f"Erro ao criar plot resumo: {e}")
            return ""