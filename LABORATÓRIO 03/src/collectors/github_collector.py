"""
Módulo para coleta de dados de Pull Requests do GitHub
"""
import requests
import pandas as pd
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

# Supondo que a classe Config esteja em src/config/config.py
from ..config.config import Config

logger = logging.getLogger(__name__)

class GitHubCollector:
    """
    Classe para orquestrar a coleta de dados de Pull Requests do GitHub,
    focando nos PRs mais recentes que atendem a critérios específicos.
    """
    
    def __init__(self, token: str = None):
        """Inicializa o coletor com o token do GitHub e uma sessão HTTP."""
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def get_pull_requests(self, repo_full_name: str, state: str = 'closed', per_page: int = 100, limit: int = 200) -> List[Dict[str, Any]]:
        """
        Coleta Pull Requests de um repositório até atingir um limite de PRs válidos.
        Busca os PRs ordenados pelos mais recentemente atualizados.
        """
        prs = []
        page = 1
        
        logger.info(f"Coletando até {limit} PRs recentes do repositório: {repo_full_name}")
        
        while len(prs) < limit:
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
                        logger.info("Não há mais PRs para coletar neste repositório.")
                        break
                    
                    processed_on_page = 0
                    for pr in page_prs:
                        pr_data = self._extract_pr_data(pr)
                        
                        if self._should_include_pr(pr_data):
                            enhanced_pr = self._enhance_pr_data(repo_full_name, pr_data)
                            if enhanced_pr:
                                prs.append(enhanced_pr)
                                processed_on_page += 1
                                if len(prs) >= limit:
                                    break
                    
                    logger.info(f"Página {page}: {len(page_prs)} PRs recebidos, {processed_on_page} incluídos. Total: {len(prs)}/{limit}")
                    page += 1
                    time.sleep(Config.SLEEP_TIME)
                    
                elif response.status_code == 403:
                    logger.warning("Rate limit do GitHub atingido. Aguardando 1 hora para continuar...")
                    time.sleep(3600)
                else:
                    logger.error(f"Erro na requisição à API do GitHub: {response.status_code} - {response.text}")
                    break
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de conexão ao coletar PRs: {e}")
                time.sleep(30) # Espera 30s antes de tentar novamente
            except Exception as e:
                logger.error(f"Erro inesperado ao coletar PRs: {e}", exc_info=True)
                break
        
        logger.info(f"Coleta finalizada para {repo_full_name}: {len(prs)} PRs coletados.")
        return prs[:limit]

    def collect_repository_prs(self, repo_full_name: str) -> List[Dict[str, Any]]:
        """Coleta os PRs mais recentes de um repositório que atendem aos critérios."""
        logger.info(f"=== Iniciando coleta para {repo_full_name} ===")
        prs = self.get_pull_requests(
            repo_full_name,
            limit=Config.PRS_PER_REPO_LIMIT
        )
        logger.info(f"=== Coleta concluída para {repo_full_name}: {len(prs)} PRs válidos encontrados ===")
        return prs

    def collect_multiple_repositories(self, repositories: List[Dict[str, Any]], max_repos: Optional[int] = None) -> List[Dict[str, Any]]:
        """Coleta PRs de múltiplos repositórios."""
        all_prs = []
        
        repos_to_process = repositories
        if max_repos and max_repos < len(repositories):
            repos_to_process = repositories[:max_repos]
            logger.info(f"Limitando a coleta a {max_repos} repositórios.")

        logger.info(f"=== INICIANDO COLETA DE {len(repos_to_process)} REPOSITÓRIOS ===")
        
        for i, repo in enumerate(repos_to_process):
            repo_name = repo['full_name']
            logger.info(f"\n--- Processando Repositório {i+1}/{len(repos_to_process)}: {repo_name} ---")
            try:
                repo_prs = self.collect_repository_prs(repo_name)
                all_prs.extend(repo_prs)
                logger.info(f"Total acumulado de PRs: {len(all_prs)}")
                
                if i < len(repos_to_process) - 1:
                    logger.info("Pausando por 10 segundos entre repositórios...")
                    time.sleep(10)
            except Exception as e:
                logger.error(f"Erro fatal ao processar o repositório {repo_name}: {e}", exc_info=True)
                continue
        
        logger.info(f"=== COLETA GERAL CONCLUÍDA: {len(all_prs)} PRs coletados no total ===")
        return all_prs

    def save_prs_data(self, prs_data: List[Dict[str, Any]], filename: str = None) -> str:
        """Salva os dados dos PRs em arquivos CSV (simplificado) e JSON (completo)."""
        if not prs_data:
            logger.warning("Nenhum dado de PR para salvar.")
            return ""

        if not filename:
            filename = f"pull_requests_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = Path(Config.DATA_DIR) / filename
        
        # Prepara dados para CSV, removendo estruturas aninhadas complexas
        clean_prs = []
        for pr in prs_data:
            clean_pr = pr.copy()
            clean_pr.pop('reviews_data', None)
            clean_pr.pop('participants', None) 
            clean_prs.append(clean_pr)
        
        df = pd.DataFrame(clean_prs)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Dados simplificados salvos em: {filepath}")
        
        # Salva a versão completa com todos os dados em JSON
        json_filepath = filepath.with_suffix('.json')
        try:
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(prs_data, f, indent=2, default=str, ensure_ascii=False)
            logger.info(f"Dados completos salvos em: {json_filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo JSON: {e}")
        
        return str(filepath)

    # --- Métodos Auxiliares para Extração e Enriquecimento de Dados ---

    def _extract_pr_data(self, pr: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai os dados brutos mais importantes de um PR da API."""
        return {
            'id': pr.get('id'),
            'number': pr.get('number'),
            'title': pr.get('title', ''),
            'body': pr.get('body') or '',
            'state': pr.get('state'),
            'merged': pr.get('merged_at') is not None,
            'created_at': pr.get('created_at'),
            'updated_at': pr.get('updated_at'),
            'closed_at': pr.get('closed_at'),
            'merged_at': pr.get('merged_at'),
            'user': pr.get('user', {}).get('login'),
            'url': pr.get('html_url'),
        }
    
    def _should_include_pr(self, pr_data: Dict[str, Any]) -> bool:
        """Determina se um PR atende aos critérios mínimos para ser incluído na análise."""
        if pr_data['state'] != 'closed':
            return False
        
        if not pr_data['created_at'] or not pr_data['closed_at']:
            return False
            
        created_at = datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00'))
        closed_at = datetime.fromisoformat(pr_data['closed_at'].replace('Z', '+00:00'))
        
        analysis_time = closed_at - created_at
        if analysis_time < timedelta(hours=Config.MIN_REVIEW_TIME_HOURS):
            return False
        
        return True

    def _enhance_pr_data(self, repo_full_name: str, pr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Busca dados adicionais na API para enriquecer as informações de um único PR."""
        try:
            pr_number = pr_data['number']
            
            reviews = self._get_pr_endpoint(repo_full_name, pr_number, "reviews")
            comments = self._get_pr_endpoint(repo_full_name, pr_number, "comments", is_issue=True)
            review_comments = self._get_pr_endpoint(repo_full_name, pr_number, "comments")
            files_info = self._get_pr_files_info(repo_full_name, pr_number)

            participants = self._get_participants(reviews, comments, review_comments, pr_data['user'])
            analysis_time_hours = self._calculate_analysis_time(pr_data)

            pr_data.update({
                'repo_full_name': repo_full_name,
                'reviews_count': len(reviews),
                'comments_count': len(comments),
                'review_comments_count': len(review_comments),
                'participants_count': len(participants),
                'files_changed': files_info['files_count'],
                'additions': files_info['additions'],
                'deletions': files_info['deletions'],
                'total_changes': files_info['additions'] + files_info['deletions'],
                'description_length': len(pr_data.get('body', '')),
                'analysis_time_hours': analysis_time_hours,
                'analysis_time_days': analysis_time_hours / 24 if analysis_time_hours is not None else 0,
                # Dados completos para salvar no JSON
                'reviews_data': reviews, 
                'participants': participants,
            })
            return pr_data
        except Exception as e:
            logger.error(f"Erro ao enriquecer PR #{pr_data.get('number')}: {e}", exc_info=True)
            return None
    
    def _get_pr_endpoint(self, repo_full_name: str, pr_number: int, endpoint: str, is_issue: bool = False) -> List:
        """Função genérica para buscar dados de um endpoint de PR/Issue."""
        base_path = "issues" if is_issue else "pulls"
        try:
            url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/{base_path}/{pr_number}/{endpoint}"
            response = self.session.get(url, params={'per_page': 100})
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar endpoint '{endpoint}' para o PR #{pr_number}: {e}")
        return []

    def _get_pr_files_info(self, repo_full_name: str, pr_number: int) -> Dict[str, int]:
        """Coleta e resume informações sobre arquivos modificados em um PR."""
        files = self._get_pr_endpoint(repo_full_name, pr_number, "files")
        return {
            'files_count': len(files),
            'additions': sum(f.get('additions', 0) for f in files),
            'deletions': sum(f.get('deletions', 0) for f in files)
        }
    
    def _get_participants(self, reviews: List, comments: List, review_comments: List, author: Optional[str]) -> List[str]:
        """Calcula a lista de participantes únicos em um PR."""
        participants = {author} if author else set()
        for item_list in [reviews, comments, review_comments]:
            for item in item_list:
                if (user := item.get('user')) and (login := user.get('login')):
                    participants.add(login)
        return list(participants)
    
    def _calculate_analysis_time(self, pr_data: Dict[str, Any]) -> Optional[float]:
        """Calcula o tempo de análise de um PR em horas."""
        try:
            created_at = datetime.fromisoformat(pr_data['created_at'].replace('Z', '+00:00'))
            closed_at = datetime.fromisoformat(pr_data['closed_at'].replace('Z', '+00:00'))
            delta = closed_at - created_at
            return delta.total_seconds() / 3600
        except (TypeError, ValueError) as e:
            logger.warning(f"Não foi possível calcular o tempo de análise para o PR #{pr_data.get('number')}: {e}")
            return None
        