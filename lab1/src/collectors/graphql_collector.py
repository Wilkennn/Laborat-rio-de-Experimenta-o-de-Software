import os
import requests
import pandas as pd
import time
from .. import config

class GraphQLDataCollector:
    
    def __init__(self):
        self.api_url = config.GRAPHQL_API_URL
        self.headers = config.HEADERS
        self.total_repos_to_fetch = config.TOTAL_REPOS_TO_FETCH
        self.repos_per_page = config.REPOS_PER_PAGE
        self.csv_filepath = config.CSV_FILEPATH
        
        self.all_repo_nodes = []
        self.dataframe = None

    def _run_graphql_query(self, cursor=None):
        query = """
        query TopRepos($cursor: String) {
          search(
            query: "stars:>1 sort:stars-desc",
            type: REPOSITORY,
            first: %d,
            after: $cursor
          ) {
            nodes {
              ... on Repository {
                nameWithOwner
                description
                url
                createdAt
                updatedAt
                stargazers {
                  totalCount
                }
                forkCount
                primaryLanguage {
                  name
                }
                licenseInfo {
                  spdxId
                }
                issues(states: OPEN) {
                  totalCount
                }
                issuesClosed: issues(states: CLOSED) {
                  totalCount
                }
                pullRequests(states: MERGED) {
                  totalCount
                }
                releases {
                  totalCount
                }
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
        }
        """ % self.repos_per_page
        
        # Lógica de retentativa para lidar com instabilidades da API
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={'query': query, 'variables': {'cursor': cursor}}
                )
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.HTTPError as e:
                if 500 <= e.response.status_code < 600:
                    print(f"Erro {e.response.status_code} - tentativa {attempt + 1}/{max_retries}")
                    time.sleep(10)
                else:
                    print(f"Erro HTTP: {e}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Erro de requisição: {e}")
                time.sleep(5)
        
        print("Todas as tentativas falharam.")
        return None

    def _fetch_all_repos(self):
        cursor = None
        has_next_page = True
        total_pages = self.total_repos_to_fetch // self.repos_per_page
        
        print(f"Iniciando a coleta de {self.total_repos_to_fetch} repositórios via GraphQL...")

        for page_num in range(1, total_pages + 1):
            if not has_next_page:
                print("Não há mais páginas para buscar.")
                break
            
            data = self._run_graphql_query(cursor)
            
            if data and 'data' in data and data['data']['search']:
                search_results = data['data']['search']
                self.all_repo_nodes.extend(search_results['nodes'])
                
                page_info = search_results['pageInfo']
                cursor = page_info['endCursor']
                has_next_page = page_info['hasNextPage']
                
                print(f"Página {page_num}/{total_pages} coletada com sucesso.")
                
                # Delay respeitoso entre requests para não sobrecarregar a API
                if page_num < total_pages:  # Não precisa delay na última página
                    time.sleep(2)  # 2 segundos entre requests
            else:
                print(f"Erro ao buscar dados na página {page_num}. Resposta: {data}")
                return False
        return True

    def _parse_data(self):
        """
        Processa os 'nodes' da resposta GraphQL para um formato limpo,
        pronto para o DataFrame.
        """
        if not self.all_repo_nodes:
            print("Não há dados para processar.")
            return

        parsed_list = []
        for repo in self.all_repo_nodes:
            if not repo: continue

            # Calculando total de issues para RQ06
            open_issues = repo.get('issues', {}).get('totalCount', 0)
            closed_issues = repo.get('issuesClosed', {}).get('totalCount', 0)
            total_issues = open_issues + closed_issues

            parsed_list.append({
                'name': repo.get('nameWithOwner'),
                'stars': repo.get('stargazers', {}).get('totalCount', 0),
                'forks': repo.get('forkCount', 0),
                'language': repo.get('primaryLanguage', {}).get('name') if repo.get('primaryLanguage') else 'N/A',
                'license': repo.get('licenseInfo', {}).get('spdxId') if repo.get('licenseInfo') else 'No License',
                'open_issues': open_issues,
                'closed_issues': closed_issues,
                'total_issues': total_issues,
                'created_at': repo.get('createdAt'),
                'updated_at': repo.get('updatedAt'),
                'description': repo.get('description'),
                'url': repo.get('url'),
                'merged_pull_requests': repo.get('pullRequests', {}).get('totalCount', 0),
                'releases': repo.get('releases', {}).get('totalCount', 0)
            })
        self.dataframe = pd.DataFrame(parsed_list)

    def _save_to_csv(self):
        """Salva o DataFrame processado em um arquivo CSV."""
        if self.dataframe is None:
            print("Não há DataFrame para salvar.")
            return
        os.makedirs(os.path.dirname(self.csv_filepath), exist_ok=True)
        self.dataframe.to_csv(self.csv_filepath, index=False)
        print(f"\nDados salvos com sucesso em: {self.csv_filepath}")

    def run(self):
        """
        Método público que executa todo o fluxo de coleta e salvamento.
        """
        if self._fetch_all_repos():
            self._parse_data()
            self._save_to_csv()
