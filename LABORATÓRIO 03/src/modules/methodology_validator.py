"""
Validador de Metodologia - Garante conformidade com LAB03 
Verifica se estamos seguindo exatamente a metodologia especificada
"""
import pandas as pd
import logging
from typing import Dict, List, Any, Tuple
from ..config.config import Config

logger = logging.getLogger(__name__)

class MethodologyValidator:
    """Valida se a coleta e análise seguem a metodologia do LAB03"""
    
    def validate_repository_selection(self, repositories: List[Dict]) -> Tuple[bool, str]:
        """
        Valida critérios de seleção dos repositórios:
        - Repositórios populares (top 200)
        - Pelo menos 100 PRs (MERGED + CLOSED)
        """
        logger.info("🔍 Validando critérios de seleção de repositórios...")
        
        if not repositories:
            return False, "Nenhum repositório selecionado"
        
        # Verifica se são populares (ordenados por stars)
        stars = [repo.get('stars', 0) for repo in repositories]
        if not all(stars[i] >= stars[i+1] for i in range(len(stars)-1)):
            logger.warning("⚠️ Repositórios podem não estar ordenados por popularidade")
        
        # Verifica critério de PRs mínimos
        invalid_repos = []
        for repo in repositories:
            pr_count = repo.get('pr_count', 0)
            if pr_count < Config.MIN_PRS_PER_REPO:
                invalid_repos.append(f"{repo.get('full_name', 'unknown')} ({pr_count} PRs)")
        
        if invalid_repos:
            message = f"❌ {len(invalid_repos)} repositórios não atendem ao critério de {Config.MIN_PRS_PER_REPO}+ PRs: {', '.join(invalid_repos[:5])}"
            return False, message
        
        logger.info(f"✅ {len(repositories)} repositórios validados com critério de {Config.MIN_PRS_PER_REPO}+ PRs")
        return True, f"Repositórios válidos: {len(repositories)}"
    
    def validate_pr_selection(self, prs: List[Dict]) -> Tuple[bool, str]:
        """
        Valida critérios de seleção dos PRs:
        - Status MERGED ou CLOSED
        - Pelo menos uma revisão
        - Tempo > 1 hora (elimina automação)
        """
        logger.info("🔍 Validando critérios de seleção de PRs...")
        
        if not prs:
            return False, "Nenhum PR coletado"
        
        # Estatísticas de validação
        total_prs = len(prs)
        merged_closed = 0
        with_reviews = 0
        time_valid = 0
        fully_valid = 0
        
        invalid_reasons = {
            'status': 0,
            'reviews': 0, 
            'time': 0
        }
        
        for pr in prs:
            # Critério 1: Status MERGED ou CLOSED
            state = pr.get('state', '').lower()
            merged = pr.get('merged', False)
            status_valid = state == 'closed' or merged
            
            if status_valid:
                merged_closed += 1
            else:
                invalid_reasons['status'] += 1
            
            # Critério 2: Pelo menos uma revisão
            reviews = pr.get('reviews_count', 0)
            reviews_valid = reviews >= 1
            
            if reviews_valid:
                with_reviews += 1
            else:
                invalid_reasons['reviews'] += 1
            
            # Critério 3: Tempo > 1 hora
            time_hours = pr.get('analysis_time_hours', 0)
            time_valid_check = time_hours > Config.MIN_REVIEW_TIME_HOURS
            
            if time_valid_check:
                time_valid += 1
            else:
                invalid_reasons['time'] += 1
            
            # Válido se atende todos os critérios
            if status_valid and reviews_valid and time_valid_check:
                fully_valid += 1
        
        # Log de estatísticas
        logger.info(f"📊 Estatísticas de validação dos PRs:")
        logger.info(f"   Total coletado: {total_prs}")
        logger.info(f"   ✅ Status MERGED/CLOSED: {merged_closed} ({merged_closed/total_prs*100:.1f}%)")
        logger.info(f"   ✅ Com revisões (≥1): {with_reviews} ({with_reviews/total_prs*100:.1f}%)")
        logger.info(f"   ✅ Tempo válido (>1h): {time_valid} ({time_valid/total_prs*100:.1f}%)")
        logger.info(f"   ✅ TOTALMENTE VÁLIDOS: {fully_valid} ({fully_valid/total_prs*100:.1f}%)")
        
        if invalid_reasons['status'] > 0:
            logger.warning(f"   ❌ Status inválido: {invalid_reasons['status']}")
        if invalid_reasons['reviews'] > 0:
            logger.warning(f"   ❌ Sem revisões: {invalid_reasons['reviews']}")
        if invalid_reasons['time'] > 0:
            logger.warning(f"   ❌ Tempo insuficiente: {invalid_reasons['time']}")
        
        # Considera válido se pelo menos 50% atendem todos os critérios
        success_rate = fully_valid / total_prs
        if success_rate >= 0.5:
            return True, f"✅ {fully_valid}/{total_prs} PRs válidos ({success_rate*100:.1f}%)"
        else:
            return False, f"❌ Apenas {fully_valid}/{total_prs} PRs válidos ({success_rate*100:.1f}%) - insuficiente"
    
    def validate_metrics_completeness(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Valida se todas as métricas especificadas foram coletadas:
        - Tamanho: arquivos, linhas adicionadas/removidas
        - Tempo: intervalo criação-fechamento/merge
        - Descrição: caracteres da descrição
        - Interações: participantes, comentários
        """
        logger.info("🔍 Validando completude das métricas...")
        
        if df.empty:
            return False, "DataFrame vazio"
        
        # Métricas obrigatórias conforme especificação
        required_metrics = {
            'Tamanho': ['files_changed', 'additions', 'deletions', 'total_changes'],
            'Tempo': ['analysis_time_hours', 'analysis_time_days'], 
            'Descrição': ['description_length', 'has_description'],
            'Interações': ['participants_count', 'comments_count']
        }
        
        missing_metrics = []
        available_metrics = []
        
        for category, metrics in required_metrics.items():
            category_missing = []
            category_available = []
            
            for metric in metrics:
                if metric in df.columns:
                    category_available.append(metric)
                else:
                    category_missing.append(metric)
                    missing_metrics.append(f"{category}:{metric}")
            
            logger.info(f"   {category}: {len(category_available)}/{len(metrics)} disponíveis")
            if category_missing:
                logger.warning(f"     ❌ Ausentes: {category_missing}")
            else:
                logger.info(f"     ✅ Completas: {category_available}")
        
        if missing_metrics:
            return False, f"❌ Métricas ausentes: {missing_metrics}"
        
        # Verifica se há dados válidos (não nulos)
        null_counts = {}
        for category, metrics in required_metrics.items():
            for metric in metrics:
                if metric in df.columns:
                    null_count = df[metric].isnull().sum()
                    if null_count > 0:
                        null_counts[metric] = null_count
        
        if null_counts:
            logger.warning(f"⚠️ Métricas com valores nulos: {null_counts}")
        
        return True, f"✅ Todas as {sum(len(m) for m in required_metrics.values())} métricas coletadas"
    
    def validate_research_questions(self, analysis_results: Dict) -> Tuple[bool, str]:
        """
        Valida se todas as 8 questões de pesquisa foram respondidas:
        RQ01-RQ04: Feedback Final (MERGED vs CLOSED)
        RQ05-RQ08: Número de Revisões
        """
        logger.info("🔍 Validando questões de pesquisa...")
        
        # Questões obrigatórias
        required_rqs = {
            'Grupo A - Feedback Final': ['rq01_size_vs_feedback', 'rq02_time_vs_feedback', 
                                       'rq03_description_vs_feedback', 'rq04_interactions_vs_feedback'],
            'Grupo B - Número de Revisões': ['rq05_size_vs_reviews', 'rq06_time_vs_reviews',
                                           'rq07_description_vs_reviews', 'rq08_interactions_vs_reviews']
        }
        
        missing_rqs = []
        completed_rqs = []
        
        for group, rqs in required_rqs.items():
            group_missing = []
            group_completed = []
            
            # Verifica no grupo A (feedback)
            if group.startswith('Grupo A'):
                group_data = analysis_results.get('rq_a_feedback', {})
            else:
                group_data = analysis_results.get('rq_b_reviews', {})
            
            for rq in rqs:
                if rq in group_data and group_data[rq]:
                    group_completed.append(rq)
                    completed_rqs.append(rq)
                else:
                    group_missing.append(rq)
                    missing_rqs.append(f"{group}:{rq}")
            
            logger.info(f"   {group}: {len(group_completed)}/{len(rqs)} completas")
            if group_missing:
                logger.warning(f"     ❌ Ausentes: {group_missing}")
            else:
                logger.info(f"     ✅ Completas: {group_completed}")
        
        if missing_rqs:
            return False, f"❌ RQs ausentes: {missing_rqs}"
        
        return True, f"✅ Todas as 8 questões de pesquisa respondidas"
    
    def generate_compliance_report(self, repositories: List[Dict], prs: List[Dict], 
                                 df: pd.DataFrame, analysis_results: Dict) -> str:
        """Gera relatório de conformidade com a metodologia"""
        
        report = []
        report.append("=" * 60)
        report.append("📋 RELATÓRIO DE CONFORMIDADE COM METODOLOGIA LAB03")
        report.append("=" * 60)
        
        # Validação de repositórios
        repo_valid, repo_msg = self.validate_repository_selection(repositories)
        report.append(f"\n🏛️  CRITÉRIOS DE REPOSITÓRIOS:")
        report.append(f"   Status: {'✅ CONFORME' if repo_valid else '❌ NÃO CONFORME'}")
        report.append(f"   Detalhes: {repo_msg}")
        
        # Validação de PRs
        pr_valid, pr_msg = self.validate_pr_selection(prs)
        report.append(f"\n📝 CRITÉRIOS DE PRS:")
        report.append(f"   Status: {'✅ CONFORME' if pr_valid else '❌ NÃO CONFORME'}")
        report.append(f"   Detalhes: {pr_msg}")
        
        # Validação de métricas
        metrics_valid, metrics_msg = self.validate_metrics_completeness(df)
        report.append(f"\n📊 MÉTRICAS OBRIGATÓRIAS:")
        report.append(f"   Status: {'✅ CONFORME' if metrics_valid else '❌ NÃO CONFORME'}")
        report.append(f"   Detalhes: {metrics_msg}")
        
        # Validação de RQs
        rq_valid, rq_msg = self.validate_research_questions(analysis_results)
        report.append(f"\n🔬 QUESTÕES DE PESQUISA:")
        report.append(f"   Status: {'✅ CONFORME' if rq_valid else '❌ NÃO CONFORME'}")
        report.append(f"   Detalhes: {rq_msg}")
        
        # Status geral
        overall_valid = all([repo_valid, pr_valid, metrics_valid, rq_valid])
        report.append(f"\n🎯 STATUS GERAL:")
        report.append(f"   {'✅ METODOLOGIA TOTALMENTE CONFORME' if overall_valid else '❌ METODOLOGIA NÃO CONFORME'}")
        
        report.append("=" * 60)
        
        return "\n".join(report)