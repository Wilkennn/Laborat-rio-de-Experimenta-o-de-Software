"""
Módulo para cálculo de métricas dos Pull Requests
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Tuple
from datetime import datetime

from ..config.config import Config

logger = logging.getLogger(__name__)

class MetricsCalculator:
    """Classe para calcular métricas dos Pull Requests coletados"""
    
    def __init__(self):
        self.metrics = Config.METRICS
    
    def calculate_all_metrics(self, prs_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Calcula todas as métricas definidas para os PRs
        
        Args:
            prs_data: Lista de dados dos PRs
            
        Returns:
            DataFrame com todas as métricas calculadas
        """
        logger.info("Calculando métricas dos PRs...")
        
        if not prs_data:
            logger.warning("Nenhum dado de PR fornecido")
            return pd.DataFrame()
        
        df = pd.DataFrame(prs_data)
        
        # Calcula métricas de tamanho
        df = self._calculate_size_metrics(df)
        
        # Calcula métricas de tempo
        df = self._calculate_time_metrics(df)
        
        # Calcula métricas de descrição
        df = self._calculate_description_metrics(df)
        
        # Calcula métricas de interação
        df = self._calculate_interaction_metrics(df)
        
        # Calcula métricas derivadas
        df = self._calculate_derived_metrics(df)
        
        logger.info(f"Métricas calculadas para {len(df)} PRs")
        return df
    
    def _calculate_size_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas relacionadas ao tamanho dos PRs"""
        logger.info("Calculando métricas de tamanho...")
        
        # Garante que as colunas existam
        size_columns = ['files_changed', 'additions', 'deletions', 'total_changes']
        for col in size_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Converte para numérico
        for col in size_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calcula métricas derivadas de tamanho
        df['size_category'] = df['total_changes'].apply(self._categorize_size)
        df['files_per_change'] = df.apply(
            lambda row: row['files_changed'] / max(row['total_changes'], 1), axis=1
        )
        
        return df
    
    def _calculate_time_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas relacionadas ao tempo de análise"""
        logger.info("Calculando métricas de tempo...")
        
        # Garante que as colunas existam
        time_columns = ['analysis_time_hours', 'analysis_time_days']
        for col in time_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Converte para numérico
        for col in time_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calcula métricas derivadas de tempo
        df['time_category'] = df['analysis_time_hours'].apply(self._categorize_time)
        df['is_quick_review'] = df['analysis_time_hours'] < 24
        df['is_long_review'] = df['analysis_time_hours'] > 168  # 1 semana
        
        return df
    
    def _calculate_description_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas relacionadas à descrição dos PRs"""
        logger.info("Calculando métricas de descrição...")
        
        # Garante que as colunas existam
        if 'description_length' not in df.columns:
            df['description_length'] = 0
        if 'has_description' not in df.columns:
            df['has_description'] = False
        
        # Converte para numérico
        df['description_length'] = pd.to_numeric(df['description_length'], errors='coerce').fillna(0)
        
        # Calcula métricas derivadas de descrição
        df['description_category'] = df['description_length'].apply(self._categorize_description)
        df['description_quality'] = df.apply(self._assess_description_quality, axis=1)
        
        return df
    
    def _calculate_interaction_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas relacionadas às interações nos PRs"""
        logger.info("Calculando métricas de interação...")
        
        # Garante que as colunas existam
        interaction_columns = ['participants_count', 'comments_count', 'review_comments_count', 'reviews_count']
        for col in interaction_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Converte para numérico
        for col in interaction_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calcula total de comentários se não existir
        if 'total_comments' not in df.columns:
            df['total_comments'] = df['comments_count'] + df['review_comments_count']
        
        # Calcula métricas derivadas de interação
        df['interaction_intensity'] = df.apply(self._calculate_interaction_intensity, axis=1)
        df['avg_comments_per_participant'] = df.apply(
            lambda row: row['total_comments'] / max(row['participants_count'], 1), axis=1
        )
        df['has_multiple_reviewers'] = df['participants_count'] > 2  # Autor + pelo menos 2 revisores
        
        return df
    
    def _calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas derivadas e compostas"""
        logger.info("Calculando métricas derivadas...")
        
        # Métricas de complexidade
        df['complexity_score'] = (
            df['total_changes'].fillna(0) * 0.3 +
            df['files_changed'].fillna(0) * 0.2 +
            df['analysis_time_hours'].fillna(0) * 0.3 +
            df['reviews_count'].fillna(0) * 0.2
        )
        
        # Status final
        df['final_status'] = df.apply(self._determine_final_status, axis=1)
        
        # Categorias de PR baseadas em características
        df['pr_type'] = df.apply(self._classify_pr_type, axis=1)
        
        return df
    
    def _categorize_size(self, total_changes: int) -> str:
        """Categoriza PRs por tamanho"""
        if total_changes <= 10:
            return 'XS'
        elif total_changes <= 50:
            return 'S'
        elif total_changes <= 200:
            return 'M'
        elif total_changes <= 500:
            return 'L'
        else:
            return 'XL'
    
    def _categorize_time(self, hours: float) -> str:
        """Categoriza PRs por tempo de análise"""
        if hours <= 4:
            return 'Muito Rápido'
        elif hours <= 24:
            return 'Rápido'
        elif hours <= 72:
            return 'Médio'
        elif hours <= 168:
            return 'Lento'
        else:
            return 'Muito Lento'
    
    def _categorize_description(self, length: int) -> str:
        """Categoriza PRs por tamanho da descrição"""
        if length == 0:
            return 'Sem Descrição'
        elif length <= 50:
            return 'Muito Curta'
        elif length <= 200:
            return 'Curta'
        elif length <= 500:
            return 'Média'
        else:
            return 'Longa'
    
    def _assess_description_quality(self, row) -> str:
        """Avalia qualidade da descrição baseada em heurísticas simples"""
        length = row['description_length']
        has_desc = row['has_description']
        
        if not has_desc or length == 0:
            return 'Sem Descrição'
        elif length < 20:
            return 'Inadequada'
        elif length < 100:
            return 'Básica'
        elif length < 300:
            return 'Boa'
        else:
            return 'Detalhada'
    
    def _calculate_interaction_intensity(self, row) -> str:
        """Calcula intensidade de interação"""
        participants = row['participants_count']
        comments = row['total_comments']
        reviews = row['reviews_count']
        
        intensity_score = participants * 2 + comments * 0.5 + reviews * 1.5
        
        if intensity_score <= 3:
            return 'Baixa'
        elif intensity_score <= 8:
            return 'Média'
        elif intensity_score <= 15:
            return 'Alta'
        else:
            return 'Muito Alta'
    
    def _determine_final_status(self, row) -> str:
        """Determina status final do PR"""
        if row.get('merged', False):
            return 'MERGED'
        elif row.get('state') == 'closed':
            return 'CLOSED'
        else:
            return 'UNKNOWN'
    
    def _classify_pr_type(self, row) -> str:
        """Classifica tipo de PR baseado em características"""
        size_cat = row.get('size_category', 'M')
        time_cat = row.get('time_category', 'Médio')
        interaction = row.get('interaction_intensity', 'Média')
        
        if size_cat in ['XS', 'S'] and time_cat in ['Muito Rápido', 'Rápido']:
            return 'Hotfix/Pequeno'
        elif size_cat in ['XL'] or interaction in ['Alta', 'Muito Alta']:
            return 'Feature/Complexo'
        elif time_cat in ['Lento', 'Muito Lento']:
            return 'Controverso/Difícil'
        else:
            return 'Padrão'
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera estatísticas resumo do dataset
        """
        if df.empty:
            return {}
        
        summary = {
            'total_prs': len(df),
            'merged_prs': len(df[df['final_status'] == 'MERGED']),
            'closed_prs': len(df[df['final_status'] == 'CLOSED']),
            'merge_rate': len(df[df['final_status'] == 'MERGED']) / len(df) * 100,
            
            'size_metrics': {
                'avg_files_changed': df['files_changed'].mean(),
                'avg_total_changes': df['total_changes'].mean(),
                'median_total_changes': df['total_changes'].median(),
            },
            
            'time_metrics': {
                'avg_analysis_time_hours': df['analysis_time_hours'].mean(),
                'median_analysis_time_hours': df['analysis_time_hours'].median(),
                'avg_analysis_time_days': df['analysis_time_days'].mean(),
            },
            
            'interaction_metrics': {
                'avg_participants': df['participants_count'].mean(),
                'avg_total_comments': df['total_comments'].mean(),
                'avg_reviews': df['reviews_count'].mean(),
            },
            
            'description_metrics': {
                'avg_description_length': df['description_length'].mean(),
                'prs_with_description': df['has_description'].sum(),
                'description_rate': df['has_description'].mean() * 100,
            },
            
            'categories': {
                'size_distribution': df['size_category'].value_counts().to_dict(),
                'time_distribution': df['time_category'].value_counts().to_dict(),
                'pr_type_distribution': df['pr_type'].value_counts().to_dict(),
            }
        }
        
        return summary
    
    def save_metrics(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Salva DataFrame com métricas em arquivo CSV
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prs_with_metrics_{timestamp}.csv"
        
        filepath = f"{Config.DATA_DIR}/{filename}"
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Métricas salvas em: {filepath}")
        return filepath