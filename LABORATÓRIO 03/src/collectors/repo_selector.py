"""
Módulo para seleção de repositórios populares no GitHub
"""
import requests
import pandas as pd
import time
import logging
from typing import List, Dict, Any
from datetime import datetime

from ..config.config import Config

logger = logging.getLogger(__name__)

class RepositorySelector:
    """Classe para seleção de repositórios populares no GitHub"""
    
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({'Authorization': f'token {self.token}'})
        
    def get_top_repositories(self, count: int = 200) -> List[Dict[str, Any]]:
        """
        Obtém os repositórios mais populares do GitHub
        
        Args:
            count: Número de repositórios a buscar
            
        Returns:
            Lista de dicionários com dados dos repositórios
        """
        repositories = []
        page = 1
        per_page = 100  # Máximo permitido pela API
        
        logger.info(f"Iniciando coleta dos {count} repositórios mais populares...")
        
        while len(repositories) < count:
            try:
                # Busca repositórios ordenados por estrelas
                url = f"{Config.GITHUB_API_BASE_URL}/search/repositories"
                params = {
                    'q': 'stars:>1',  # Filtro básico para ter alguns resultados
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': min(per_page, count - len(repositories)),
                    'page': page
                }
                
                logger.info(f"Fazendo requisição para página {page}...")
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    page_repos = data.get('items', [])
                    
                    if not page_repos:
                        logger.warning("Nenhum repositório encontrado na página atual")
                        break
                    
                    # Processa cada repositório da página
                    for repo in page_repos:
                        repo_data = self._extract_repo_data(repo)
                        repositories.append(repo_data)
                        
                        if len(repositories) >= count:
                            break
                    
                    logger.info(f"Coletados {len(repositories)} repositórios até agora...")
                    page += 1
                    
                    # Rate limiting
                    time.sleep(Config.SLEEP_TIME)
                    
                elif response.status_code == 403:
                    logger.error("Rate limit excedido. Aguardando...")
                    time.sleep(3600)  # Espera 1 hora
                    
                else:
                    logger.error(f"Erro na requisição: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                logger.error(f"Erro ao buscar repositórios: {str(e)}")
                break
        
        logger.info(f"Coleta concluída. Total de repositórios: {len(repositories)}")
        return repositories[:count]
    
    def _extract_repo_data(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados relevantes de um repositório"""
        return {
            'id': repo.get('id'),
            'name': repo.get('name'),
            'full_name': repo.get('full_name'),
            'owner': repo.get('owner', {}).get('login'),
            'description': repo.get('description', ''),
            'language': repo.get('language'),
            'stars': repo.get('stargazers_count', 0),
            'forks': repo.get('forks_count', 0),
            'watchers': repo.get('watchers_count', 0),
            'size': repo.get('size', 0),
            'created_at': repo.get('created_at'),
            'updated_at': repo.get('updated_at'),
            'url': repo.get('html_url'),
            'api_url': repo.get('url'),
            'has_issues': repo.get('has_issues', False),
            'has_projects': repo.get('has_projects', False),
            'has_wiki': repo.get('has_wiki', False),
            'archived': repo.get('archived', False),
            'disabled': repo.get('disabled', False)
        }
    
    def check_pr_count(self, repo_full_name: str) -> int:
        """
        Verifica quantos PRs um repositório possui (MERGED + CLOSED)
        
        Args:
            repo_full_name: Nome completo do repositório (owner/repo)
            
        Returns:
            Número total de PRs merged + closed
        """
        try:
            # Conta PRs merged
            merged_url = f"{Config.GITHUB_API_BASE_URL}/repos/{repo_full_name}/pulls"
            merged_params = {'state': 'closed', 'per_page': 1}
            merged_response = self.session.get(merged_url, params=merged_params)
            
            if merged_response.status_code != 200:
                logger.warning(f"Erro ao verificar PRs para {repo_full_name}: {merged_response.status_code}")
                return 0
            
            # Pega o total de PRs do header Link (se disponível)
            link_header = merged_response.headers.get('Link', '')
            if 'rel="last"' in link_header:
                # Extrai o número da última página para estimar total
                import re
                last_page_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                if last_page_match:
                    last_page = int(last_page_match.group(1))
                    # Estimativa baseada na última página (assumindo per_page=30 padrão)
                    estimated_total = last_page * 30
                    return estimated_total
            
            # Fallback: usar busca para contar
            search_url = f"{Config.GITHUB_API_BASE_URL}/search/issues"
            search_params = {
                'q': f'repo:{repo_full_name} is:pr is:closed',
                'per_page': 1
            }
            search_response = self.session.get(search_url, params=search_params)
            
            if search_response.status_code == 200:
                data = search_response.json()
                return data.get('total_count', 0)
            
            return 0
            
        except Exception as e:
            logger.error(f"Erro ao contar PRs para {repo_full_name}: {str(e)}")
            return 0
    
    def filter_repositories_by_prs(self, repositories: List[Dict[str, Any]], min_prs: int = 100) -> List[Dict[str, Any]]:
        """
        Filtra repositórios que tenham pelo menos o número mínimo de PRs
        
        Args:
            repositories: Lista de repositórios
            min_prs: Número mínimo de PRs
            
        Returns:
            Lista filtrada de repositórios
        """
        filtered_repos = []
        
        logger.info(f"Filtrando repositórios com pelo menos {min_prs} PRs...")
        
        for i, repo in enumerate(repositories):
            logger.info(f"Verificando repo {i+1}/{len(repositories)}: {repo['full_name']}")
            
            pr_count = self.check_pr_count(repo['full_name'])
            repo['pr_count'] = pr_count
            
            if pr_count >= min_prs:
                filtered_repos.append(repo)
                logger.info(f"✓ {repo['full_name']}: {pr_count} PRs - INCLUÍDO")
            else:
                logger.info(f"✗ {repo['full_name']}: {pr_count} PRs - EXCLUÍDO")
            
            # Rate limiting
            time.sleep(Config.SLEEP_TIME)
        
        logger.info(f"Filtro concluído. Repositórios selecionados: {len(filtered_repos)}/{len(repositories)}")
        return filtered_repos
    
    def save_repositories(self, repositories: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Salva lista de repositórios em arquivo CSV
        
        Args:
            repositories: Lista de repositórios
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"selected_repositories_{timestamp}.csv"
        
        filepath = f"{Config.DATA_DIR}/{filename}"
        
        # Converte para DataFrame e salva
        df = pd.DataFrame(repositories)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Repositórios salvos em: {filepath}")
        return filepath
    
    def select_repositories(self, count: int = 200, min_prs: int = 100, save: bool = True) -> List[Dict[str, Any]]:
        """
        Processo completo de seleção de repositórios
        
        Args:
            count: Número inicial de repositórios a buscar
            min_prs: Número mínimo de PRs por repositório
            save: Se deve salvar o resultado em arquivo
            
        Returns:
            Lista de repositórios selecionados
        """
        logger.info("=== INICIANDO SELEÇÃO DE REPOSITÓRIOS ===")
        
        # 1. Buscar repositórios mais populares
        top_repos = self.get_top_repositories(count)
        
        if not top_repos:
            logger.error("Nenhum repositório encontrado!")
            return []
        
        # 2. Filtrar por número de PRs
        selected_repos = self.filter_repositories_by_prs(top_repos, min_prs)
        
        if not selected_repos:
            logger.error("Nenhum repositório atende aos critérios!")
            return []
        
        # 3. Salvar resultado se solicitado
        if save:
            self.save_repositories(selected_repos, "selected_repositories.csv")
        
        logger.info("=== SELEÇÃO DE REPOSITÓRIOS CONCLUÍDA ===")
        logger.info(f"Total selecionado: {len(selected_repos)} repositórios")
        
        return selected_repos