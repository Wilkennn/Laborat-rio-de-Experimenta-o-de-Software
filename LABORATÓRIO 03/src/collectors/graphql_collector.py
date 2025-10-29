"""
Coletor GraphQL otimizado para GitHub - Baseado no LAB01
Gerencia eficientemente as requisições usando GraphQL para coletar dados de PRs
"""
import requests
import json
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd

from ..config.config import Config

logger = logging.getLogger(__name__)

class GraphQLGitHubCollector:
    """Coletor otimizado usando GraphQL do GitHub"""
    
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        self.api_url = "https://api.github.com/graphql"
        
        if self.token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.v4+json'
            })
        
        # Rate limiting - GraphQL é mais eficiente
        self.requests_made = 0
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
    
    def search_popular_repositories(self, count: int = None) -> List[Dict[str, Any]]:
        """
        Busca repositórios populares usando GraphQL - otimizado com Config
        """
        if count is None:
            count = Config.TOP_REPOS_COUNT
            
        # Usa paginação menor para evitar rate limits
        per_page = min(Config.REPOS_PER_PAGE, count)
        
        logger.info(f"Buscando {count} repositórios mais populares via GraphQL (páginas de {per_page})...")
        
        repositories = []
        
        # Query GraphQL otimizada para buscar repositórios
        query = """
        query SearchRepositories($cursor: String, $count: Int!) {
          search(query: "stars:>1000 sort:stars", type: REPOSITORY, first: $count, after: $cursor) {
            repositoryCount
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              ... on Repository {
                id
                name
                nameWithOwner
                description
                stargazerCount
                forkCount
                watchers {
                  totalCount
                }
                primaryLanguage {
                  name
                }
                createdAt
                updatedAt
                url
                isArchived
                isDisabled
                hasIssuesEnabled
                pullRequests(states: [MERGED, CLOSED]) {
                  totalCount
                }
              }
            }
          }
          rateLimit {
            remaining
            resetAt
          }
        }
        """
        
        cursor = None
        per_request = min(per_page, count)  # Usa configuração otimizada
        
        while len(repositories) < count:
            variables = {
                "cursor": cursor,
                "count": min(per_request, count - len(repositories))
            }
            
            try:
                response = self._execute_query(query, variables)
                
                if not response or 'data' not in response:
                    logger.error("Resposta GraphQL inválida")
                    break
                
                search_data = response['data']['search']
                
                # Processa repositórios da página
                for repo in search_data['nodes']:
                    if repo:  # Alguns nodes podem ser null
                        repo_data = self._process_repository_data(repo)
                        if repo_data:
                            repositories.append(repo_data)
                
                # Atualiza rate limit
                if 'rateLimit' in response['data']:
                    self._update_rate_limit(response['data']['rateLimit'])
                
                # Verifica se há próxima página
                page_info = search_data['pageInfo']
                if not page_info['hasNextPage']:
                    break
                
                cursor = page_info['endCursor']
                
                logger.info(f"Coletados {len(repositories)} repositórios até agora...")
                
                # Rate limiting
                self._handle_rate_limiting()
                
            except Exception as e:
                logger.error(f"Erro na busca de repositórios: {e}")
                break
        
        logger.info(f"Busca concluída: {len(repositories)} repositórios encontrados")
        return repositories
    
    def collect_pull_requests_batch(self, repo_owner: str, repo_name: str, 
                                  max_prs: int = None) -> List[Dict[str, Any]]:
        """
        Coleta PRs de um repositório usando GraphQL - otimizado com Config
        """
        if max_prs is None:
            max_prs = Config.MAX_PRS_PER_REPO
            
        logger.info(f"Coletando até {max_prs} PRs de {repo_owner}/{repo_name} via GraphQL...")
        
        # Query GraphQL para coletar PRs com todos os dados necessários
        query = """
        query GetPullRequests($owner: String!, $name: String!, $cursor: String, $count: Int!) {
          repository(owner: $owner, name: $name) {
            pullRequests(
              states: [MERGED, CLOSED], 
              first: $count, 
              after: $cursor,
              orderBy: {field: UPDATED_AT, direction: DESC}
            ) {
              totalCount
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                id
                number
                title
                body
                state
                merged
                createdAt
                updatedAt
                closedAt
                mergedAt
                author {
                  login
                }
                participants(first: 5) {
                  totalCount
                  nodes {
                    login
                  }
                }
                comments {
                  totalCount
                }
                reviews(first: 10) {
                  totalCount
                  nodes {
                    state
                    createdAt
                  }
                }
                reviewRequests {
                  totalCount
                }
                files(first: 20) {
                  totalCount
                  nodes {
                    additions
                    deletions
                  }
                }
                additions
                deletions
                changedFiles
                url
              }
            }
          }
          rateLimit {
            remaining
            resetAt
          }
        }
        """
        
        pull_requests = []
        cursor = None
        per_request = min(Config.PRS_PER_PAGE, max_prs)  # Usa configuração otimizada
        
        while len(pull_requests) < max_prs:
            variables = {
                "owner": repo_owner,
                "name": repo_name,
                "cursor": cursor,
                "count": min(per_request, max_prs - len(pull_requests))
            }
            
            try:
                response = self._execute_query(query, variables)
                
                if not response or 'data' not in response or not response['data']['repository']:
                    logger.warning(f"Repositório {repo_owner}/{repo_name} não encontrado")
                    break
                
                pr_data = response['data']['repository']['pullRequests']
                
                # Processa PRs da página
                for pr in pr_data['nodes']:
                    if pr:
                        processed_pr = self._process_pull_request_data(pr, repo_owner, repo_name)
                        if processed_pr:
                            pull_requests.append(processed_pr)
                
                # Atualiza rate limit
                if 'rateLimit' in response['data']:
                    self._update_rate_limit(response['data']['rateLimit'])
                
                # Verifica se há próxima página
                page_info = pr_data['pageInfo']
                if not page_info['hasNextPage']:
                    break
                
                cursor = page_info['endCursor']
                
                logger.info(f"Coletados {len(pull_requests)} PRs de {repo_owner}/{repo_name}")
                
                # Rate limiting
                self._handle_rate_limiting()
                
            except Exception as e:
                logger.error(f"Erro ao coletar PRs de {repo_owner}/{repo_name}: {e}")
                break
        
        # Filtra PRs que atendem aos critérios
        filtered_prs = []
        for pr in pull_requests:
            if self._should_include_pr(pr):
                filtered_prs.append(pr)
        
        logger.info(f"PRs coletados de {repo_owner}/{repo_name}: {len(pull_requests)} total, {len(filtered_prs)} válidos")
        return filtered_prs
    
    def _process_repository_data(self, repo: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Processa dados de repositório do GraphQL"""
        try:
            pr_count = repo.get('pullRequests', {}).get('totalCount', 0)
            
            # Filtra repositórios com poucos PRs
            if pr_count < Config.MIN_PRS_PER_REPO:
                return None
            
            return {
                'id': repo.get('id'),
                'name': repo.get('name'),
                'full_name': repo.get('nameWithOwner'),
                'owner': repo.get('nameWithOwner', '').split('/')[0] if repo.get('nameWithOwner') else '',
                'description': repo.get('description', ''),
                'language': repo.get('primaryLanguage', {}).get('name') if repo.get('primaryLanguage') else None,
                'stars': repo.get('stargazerCount', 0),
                'forks': repo.get('forkCount', 0),
                'watchers': repo.get('watchers', {}).get('totalCount', 0),
                'created_at': repo.get('createdAt'),
                'updated_at': repo.get('updatedAt'),
                'url': repo.get('url'),
                'archived': repo.get('isArchived', False),
                'disabled': repo.get('isDisabled', False),
                'has_issues': repo.get('hasIssuesEnabled', False),
                'pr_count': pr_count
            }
        except Exception as e:
            logger.warning(f"Erro ao processar repositório: {e}")
            return None
    
    def _process_pull_request_data(self, pr: Dict[str, Any], repo_owner: str, repo_name: str) -> Optional[Dict[str, Any]]:
        """Processa dados de PR do GraphQL"""
        try:
            # Calcula métricas de participantes
            participants = pr.get('participants', {}).get('nodes', [])
            participants_logins = [p.get('login') for p in participants if p.get('login')]
            
            # Autor do PR
            author_login = pr.get('author', {}).get('login') if pr.get('author') else 'unknown'
            
            # Adiciona autor à lista de participantes se não estiver
            if author_login not in participants_logins:
                participants_logins.append(author_login)
            
            # Informações de revisões
            reviews = pr.get('reviews', {}).get('nodes', [])
            reviews_count = pr.get('reviews', {}).get('totalCount', 0)
            
            # Informações de arquivos e mudanças
            files_info = pr.get('files', {}).get('nodes', [])
            total_additions = sum(f.get('additions', 0) for f in files_info)
            total_deletions = sum(f.get('deletions', 0) for f in files_info)
            
            # Usa dados do PR se disponível, senão calcula
            additions = pr.get('additions', total_additions)
            deletions = pr.get('deletions', total_deletions)
            files_changed = pr.get('changedFiles', len(files_info))
            
            # Comentários
            comments_count = pr.get('comments', {}).get('totalCount', 0)
            
            # Tempo de análise
            analysis_time_hours = self._calculate_analysis_time_hours(pr)
            
            return {
                'id': pr.get('id'),
                'number': pr.get('number'),
                'title': pr.get('title', ''),
                'body': pr.get('body', ''),
                'state': pr.get('state', '').lower(),
                'merged': pr.get('merged', False),
                'created_at': pr.get('createdAt'),
                'updated_at': pr.get('updatedAt'),
                'closed_at': pr.get('closedAt'),
                'merged_at': pr.get('mergedAt'),
                'user': author_login,
                'url': pr.get('url'),
                
                # Métricas calculadas
                'participants_count': len(participants_logins),
                'participants': participants_logins,
                'comments_count': comments_count,
                'review_comments_count': 0,  # GraphQL não separa review comments facilmente
                'total_comments': comments_count,
                'reviews_count': reviews_count,
                
                # Tamanho
                'files_changed': files_changed,
                'additions': additions,
                'deletions': deletions,
                'total_changes': additions + deletions,
                
                # Descrição
                'description_length': len(pr.get('body', '')),
                'has_description': bool(pr.get('body', '').strip()),
                
                # Tempo
                'analysis_time_hours': analysis_time_hours,
                'analysis_time_days': analysis_time_hours / 24 if analysis_time_hours > 0 else 0,
                
                # Repositório
                'repo_full_name': f"{repo_owner}/{repo_name}",
                'repo_owner': repo_owner,
                'repo_name': repo_name,
                
                # Status final
                'final_status': 'MERGED' if pr.get('merged') else 'CLOSED'
            }
            
        except Exception as e:
            logger.warning(f"Erro ao processar PR {pr.get('number', 'N/A')}: {e}")
            return None
    
    def _should_include_pr(self, pr_data: Dict[str, Any]) -> bool:
        """
        Determina se um PR deve ser incluído conforme metodologia do laboratório:
        - Status MERGED ou CLOSED
        - Pelo menos uma revisão 
        - Tempo de análise > 1 hora (elimina automação)
        """
        try:
            # Critério 1: Status MERGED ou CLOSED
            state = pr_data.get('state', '').lower()
            merged = pr_data.get('merged', False)
            
            if not (state == 'closed' or merged):
                return False
            
            # Critério 2: Pelo menos uma revisão
            reviews_count = pr_data.get('reviews_count', 0)
            if reviews_count < 1:
                return False
            
            # Critério 3: Tempo > 1 hora (elimina bots/CI/CD)
            analysis_time = pr_data.get('analysis_time_hours', 0)
            if analysis_time <= Config.MIN_REVIEW_TIME_HOURS:
                return False
            
            logger.debug(f"PR incluído: state={state}, merged={merged}, reviews={reviews_count}, time={analysis_time:.2f}h")
            return True
            
        except Exception as e:
            logger.warning(f"Erro ao validar PR: {e}")
            return False
    
    def _calculate_analysis_time_hours(self, pr: Dict[str, Any]) -> float:
        """Calcula tempo de análise em horas"""
        try:
            created_at = pr.get('createdAt')
            end_time = pr.get('mergedAt') or pr.get('closedAt')
            
            if not created_at or not end_time:
                return 0.0
            
            # Parse das datas
            created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            ended = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            delta = ended - created
            return delta.total_seconds() / 3600
            
        except Exception as e:
            logger.warning(f"Erro ao calcular tempo de análise: {e}")
            return 0.0
    
    def _execute_query(self, query: str, variables: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Executa query GraphQL com tratamento de erros"""
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            # Verifica rate limit antes da requisição
            if self.rate_limit_remaining <= 10:
                self._wait_for_rate_limit_reset()
            
            response = self.session.post(
                self.api_url, 
                json=payload,
                timeout=30
            )
            
            self.requests_made += 1
            
            if response.status_code == 200:
                data = response.json()
                
                if 'errors' in data:
                    logger.error(f"Erros GraphQL: {data['errors']}")
                    return None
                
                return data
            
            elif response.status_code == 403:
                logger.warning("Rate limit excedido, aguardando...")
                self._wait_for_rate_limit_reset()
                return self._execute_query(query, variables)  # Retry
            
            else:
                logger.error(f"Erro HTTP {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout na requisição GraphQL")
            return None
        except Exception as e:
            logger.error(f"Erro na execução da query: {e}")
            return None
    
    def _update_rate_limit(self, rate_limit_data: Dict[str, Any]):
        """Atualiza informações de rate limit"""
        self.rate_limit_remaining = rate_limit_data.get('remaining', 0)
        reset_at = rate_limit_data.get('resetAt')
        
        if reset_at:
            self.rate_limit_reset = datetime.fromisoformat(reset_at.replace('Z', '+00:00'))
        
        logger.debug(f"Rate limit: {self.rate_limit_remaining} restantes")
    
    def _handle_rate_limiting(self):
        """Gerencia rate limiting de forma mais conservadora"""
        # Sempre aguarda o tempo configurado
        time.sleep(Config.SLEEP_TIME)
        
        if self.rate_limit_remaining <= 100:
            wait_time = 5  # Aguarda mais quando rate limit baixo
            logger.info(f"Rate limit baixo ({self.rate_limit_remaining}), aguardando {wait_time}s...")
            time.sleep(wait_time)
        elif self.requests_made % Config.BATCH_SIZE == 0:
            # Pausa após cada lote processado
            time.sleep(1.0)
    
    def _wait_for_rate_limit_reset(self):
        """Aguarda reset do rate limit"""
        if self.rate_limit_reset:
            now = datetime.now(self.rate_limit_reset.tzinfo)
            if self.rate_limit_reset > now:
                wait_time = (self.rate_limit_reset - now).total_seconds()
                logger.warning(f"Aguardando reset do rate limit: {wait_time:.0f}s")
                time.sleep(min(wait_time, 3600))  # Máximo 1 hora
        else:
            # Fallback: aguarda 1 hora
            logger.warning("Rate limit excedido, aguardando 1 hora...")
            time.sleep(3600)
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Obtém informações atuais do rate limit"""
        query = """
        query {
          rateLimit {
            limit
            remaining
            resetAt
            used
          }
        }
        """
        
        response = self._execute_query(query)
        if response and 'data' in response:
            return response['data']['rateLimit']
        
        return {}
    
    def save_data_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Salva dados em CSV"""
        filepath = Config.DATA_DIR / filename
        
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Dados salvos em: {filepath}")
        else:
            logger.warning("Nenhum dado para salvar")
        
        return str(filepath)