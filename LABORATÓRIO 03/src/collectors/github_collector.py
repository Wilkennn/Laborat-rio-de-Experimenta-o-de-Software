"""
Módulo para coleta de dados de Pull Requests do GitHub
"""
import requests
import pandas as pd
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from ..config.config import Config

logger = logging.getLogger(__name__)

class GitHubCollector:
    """Classe para coleta de dados de Pull Requests do GitHub"""
    
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def get_pull_requests(self, repo_full_name: str, state: str = 'closed', per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Coleta Pull Requests de um repositório
        
        Args:
            repo_full_name: Nome completo do repositório (owner/repo)
            state: Estado dos PRs (closed, open, all)
            per_page: Número de PRs por página
            
        Returns:
            Lista de Pull Requests
        """
        prs = []
        page = 1
        
        logger.info(f"Coletando PRs do repositório: {repo_full_name}")
        
        while True:
            try:
                url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/pulls"
                params = {
                    'state': state,
                    'sort': 'updated',
                    'direction': 'desc',
                    'per_page': per_page,
                    'page': page
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    page_prs = response.json()
                    
                    if not page_prs:
                        break
                    
                    # Processa cada PR da página
                    for pr in page_prs:
                        pr_data = self._extract_pr_data(pr)
                        
                        # Aplica filtros básicos
                        if self._should_include_pr(pr_data):
                            # Coleta dados adicionais do PR
                            enhanced_pr = self._enhance_pr_data(repo_full_name, pr_data)
                            if enhanced_pr:
                                prs.append(enhanced_pr)
                    
                    logger.info(f"Página {page}: {len(page_prs)} PRs processados, {len(prs)} incluídos total")
                    page += 1
                    
                    # Rate limiting
                    time.sleep(Config.SLEEP_TIME)
                    
                elif response.status_code == 403:
                    logger.error("Rate limit excedido. Aguardando...")
                    time.sleep(3600)
                    
                else:
                    logger.error(f"Erro na requisição: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                logger.error(f"Erro ao coletar PRs: {str(e)}")
                break
        
        logger.info(f"Coleta concluída para {repo_full_name}: {len(prs)} PRs")
        return prs
    
    def _extract_pr_data(self, pr: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados básicos de um Pull Request"""
        return {
            'id': pr.get('id'),
            'number': pr.get('number'),
            'title': pr.get('title', ''),
            'body': pr.get('body', ''),
            'state': pr.get('state'),
            'merged': pr.get('merged', False),
            'created_at': pr.get('created_at'),
            'updated_at': pr.get('updated_at'),
            'closed_at': pr.get('closed_at'),
            'merged_at': pr.get('merged_at'),
            'user': pr.get('user', {}).get('login'),
            'assignees_count': len(pr.get('assignees', [])),
            'requested_reviewers_count': len(pr.get('requested_reviewers', [])),
            'url': pr.get('html_url'),
            'api_url': pr.get('url'),
            'diff_url': pr.get('diff_url'),
            'patch_url': pr.get('patch_url'),
        }
    
    def _should_include_pr(self, pr_data: Dict[str, Any]) -> bool:
        """
        Determina se um PR deve ser incluído na análise
        
        Critérios:
        - Estado MERGED ou CLOSED
        - Tempo de análise > 1 hora
        """
        # Verifica estado
        if pr_data['state'] not in ['closed'] and not pr_data['merged']:
            return False
        
        # Verifica tempo de análise
        created_at = datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00'))
        
        end_time = None
        if pr_data['merged_at']:
            end_time = datetime.fromisoformat(pr_data['merged_at'].replace('Z', '+00:00'))
        elif pr_data['closed_at']:
            end_time = datetime.fromisoformat(pr_data['closed_at'].replace('Z', '+00:00'))
        
        if not end_time:
            return False
        
        analysis_time = end_time - created_at
        if analysis_time < timedelta(hours=Config.MIN_REVIEW_TIME_HOURS):
            return False
        
        return True
    
    def _enhance_pr_data(self, repo_full_name: str, pr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Enriquece dados do PR com informações adicionais (revisões, comentários, arquivos)
        """
        try:
            pr_number = pr_data['number']
            
            # Coleta revisões
            reviews = self._get_pr_reviews(repo_full_name, pr_number)
            if not reviews:  # PR deve ter pelo menos uma revisão
                return None
            
            # Coleta comentários
            comments = self._get_pr_comments(repo_full_name, pr_number)
            review_comments = self._get_pr_review_comments(repo_full_name, pr_number)
            
            # Coleta informações de arquivos modificados
            files_info = self._get_pr_files(repo_full_name, pr_number)
            
            # Calcula métricas
            pr_data.update({
                # Revisões
                'reviews_count': len(reviews),
                'reviews_data': reviews,
                
                # Comentários e interações
                'comments_count': len(comments),
                'review_comments_count': len(review_comments),
                'total_comments': len(comments) + len(review_comments),
                'participants': self._get_participants(reviews, comments, review_comments, pr_data['user']),
                'participants_count': len(self._get_participants(reviews, comments, review_comments, pr_data['user'])),
                
                # Tamanho e arquivos
                'files_changed': files_info['files_count'],
                'additions': files_info['additions'],
                'deletions': files_info['deletions'],
                'total_changes': files_info['additions'] + files_info['deletions'],
                
                # Descrição
                'description_length': len(pr_data.get('body', '')),
                'has_description': bool(pr_data.get('body', '').strip()),
                
                # Tempo de análise
                'analysis_time_hours': self._calculate_analysis_time(pr_data),
                'analysis_time_days': self._calculate_analysis_time(pr_data) / 24,
                
                # Repositório
                'repo_full_name': repo_full_name,
            })
            
            return pr_data
            
        except Exception as e:
            logger.error(f"Erro ao enriquecer PR {pr_data.get('number', 'N/A')}: {str(e)}")
            return None
    
    def _get_pr_reviews(self, repo_full_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Coleta revisões de um PR"""
        try:
            url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/pulls/{pr_number}/reviews"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            logger.error(f"Erro ao coletar revisões: {str(e)}")
            return []
    
    def _get_pr_comments(self, repo_full_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Coleta comentários gerais de um PR"""
        try:
            url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/issues/{pr_number}/comments"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            logger.error(f"Erro ao coletar comentários: {str(e)}")
            return []
    
    def _get_pr_review_comments(self, repo_full_name: str, pr_number: int) -> List[Dict[str, Any]]:
        """Coleta comentários de revisão de um PR"""
        try:
            url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/pulls/{pr_number}/comments"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            logger.error(f"Erro ao coletar comentários de revisão: {str(e)}")
            return []
    
    def _get_pr_files(self, repo_full_name: str, pr_number: int) -> Dict[str, int]:
        """Coleta informações sobre arquivos modificados em um PR"""
        try:
            url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/pulls/{pr_number}/files"
            response = self.session.get(url)
            
            if response.status_code == 200:
                files = response.json()
                return {
                    'files_count': len(files),
                    'additions': sum(f.get('additions', 0) for f in files),
                    'deletions': sum(f.get('deletions', 0) for f in files)
                }
            
            return {'files_count': 0, 'additions': 0, 'deletions': 0}
            
        except Exception as e:
            logger.error(f"Erro ao coletar arquivos: {str(e)}")
            return {'files_count': 0, 'additions': 0, 'deletions': 0}
    
    def _get_participants(self, reviews: List, comments: List, review_comments: List, author: str) -> List[str]:
        """Calcula lista de participantes únicos no PR"""
        participants = set([author])
        
        for review in reviews:
            if review.get('user', {}).get('login'):
                participants.add(review['user']['login'])
        
        for comment in comments:
            if comment.get('user', {}).get('login'):
                participants.add(comment['user']['login'])
        
        for comment in review_comments:
            if comment.get('user', {}).get('login'):
                participants.add(comment['user']['login'])
        
        return list(participants)
    
    def _calculate_analysis_time(self, pr_data: Dict[str, Any]) -> float:
        """Calcula tempo de análise em horas"""
        try:
            created_at = datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00'))
            
            end_time = None
            if pr_data['merged_at']:
                end_time = datetime.fromisoformat(pr_data['merged_at'].replace('Z', '+00:00'))
            elif pr_data['closed_at']:
                end_time = datetime.fromisoformat(pr_data['closed_at'].replace('Z', '+00:00'))
            
            if end_time:
                delta = end_time - created_at
                return delta.total_seconds() / 3600
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Erro ao calcular tempo de análise: {str(e)}")
            return 0.0
    
    def collect_repository_prs(self, repo_full_name: str) -> List[Dict[str, Any]]:
        """
        Coleta todos os PRs de um repositório que atendem aos critérios
        """
        logger.info(f"=== Iniciando coleta para {repo_full_name} ===")
        
        prs = self.get_pull_requests(repo_full_name)
        
        logger.info(f"=== Coleta concluída para {repo_full_name}: {len(prs)} PRs ===")
        return prs
    
    def collect_from_repositories(self, repositories: List[Dict[str, Any]], max_repos: int = None) -> List[Dict[str, Any]]:
        """
        Coleta PRs de múltiplos repositórios
        
        Args:
            repositories: Lista de repositórios
            max_repos: Número máximo de repositórios a processar (para testes)
        """
        if max_repos:
            repositories = repositories[:max_repos]
        
        return self.collect_multiple_repositories(repositories)
    
    def collect_from_repositories(self, repositories: List[Dict[str, Any]], max_repos: int = None) -> List[Dict[str, Any]]:
        """
        Coleta PRs de múltiplos repositórios (método esperado pelo pipeline)
        """
        repos_to_process = repositories
        if max_repos:
            repos_to_process = repositories[:max_repos]
        
        return self.collect_multiple_repositories(repos_to_process)
    
    def collect_multiple_repositories(self, repositories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Coleta PRs de múltiplos repositórios
        """
        all_prs = []
        
        logger.info(f"=== INICIANDO COLETA DE {len(repositories)} REPOSITÓRIOS ===")
        
        for i, repo in enumerate(repositories):
            logger.info(f"\n--- Repositório {i+1}/{len(repositories)}: {repo['full_name']} ---")
            
            try:
                repo_prs = self.collect_repository_prs(repo['full_name'])
                all_prs.extend(repo_prs)
                
                logger.info(f"Total acumulado: {len(all_prs)} PRs")
                
                # Pausa entre repositórios para evitar rate limiting
                if i < len(repositories) - 1:
                    logger.info("Pausando entre repositórios...")
                    time.sleep(10)
                    
            except Exception as e:
                logger.error(f"Erro ao processar repositório {repo['full_name']}: {str(e)}")
                continue
        
        logger.info(f"=== COLETA CONCLUÍDA: {len(all_prs)} PRs TOTAL ===")
        return all_prs
    
    def save_prs_data(self, prs_data: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Salva dados dos PRs em arquivo CSV
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pull_requests_data_{timestamp}.csv"
        
        filepath = f"{Config.DATA_DIR}/{filename}"
        
        # Remove dados aninhados para o CSV
        clean_prs = []
        for pr in prs_data:
            clean_pr = pr.copy()
            clean_pr.pop('reviews_data', None)  # Remove dados detalhados das revisões
            clean_prs.append(clean_pr)
        
        # Converte para DataFrame e salva
        df = pd.DataFrame(clean_prs)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        # Salva também versão completa em JSON
        json_filepath = filepath.replace('.csv', '.json')
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(prs_data, f, indent=2, default=str, ensure_ascii=False)
        
        logger.info(f"Dados salvos em: {filepath}")
        logger.info(f"Dados completos salvos em: {json_filepath}")
        
        return filepath