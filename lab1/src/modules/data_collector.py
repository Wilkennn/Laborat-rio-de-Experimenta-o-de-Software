import os
import requests
import pandas as pd
from . import config

class DataCollector:
    """
    Classe responsável por coletar, processar e salvar os dados
    dos repositórios mais populares do GitHub.
    """
    def __init__(self):
        """
        Construtor da classe. Inicializa as configurações e o estado.
        """
        self.api_url = config.API_URL
        self.headers = config.HEADERS
        self.total_repos_to_fetch = config.TOTAL_REPOS_TO_FETCH
        self.repos_per_page = config.REPOS_PER_PAGE
        self.csv_filepath = config.CSV_FILEPATH
        
        # Atributos para armazenar os dados durante o processo
        self.raw_data = None
        self.dataframe = None

    def _fetch_page(self, page_number):
        """
        Busca uma única página de resultados da API do GitHub.
        Este método é "privado" (convenção do _ no início).
        """
        params = {
            'q': 'stars:>1',
            'sort': 'stars',
            'order': 'desc',
            'per_page': self.repos_per_page,
            'page': page_number
        }
        try:
            response = requests.get(self.api_url, headers=self.headers, params=params)
            response.raise_for_status() # Lança erro para status HTTP 4xx/5xx
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar a página {page_number}: {e}")
            return None

    def _fetch_all_repos(self):
        """
        Orquestra a busca por todas as páginas necessárias para obter o total de repositórios.
        """
        all_repos_data = []
        total_pages = self.total_repos_to_fetch // self.repos_per_page
        print(f"Iniciando a coleta de {self.total_repos_to_fetch} repositórios...")

        for page in range(1, total_pages + 1):
            page_data = self._fetch_page(page)
            if page_data:
                all_repos_data.extend(page_data)
                print(f"Página {page}/{total_pages} coletada com sucesso.")
            else:
                print("Coleta interrompida devido a um erro.")
                return None
        
        self.raw_data = all_repos_data
        return True

    def _parse_data(self):
        """
        Processa os dados brutos (JSON) e os converte para um formato limpo.
        """
        if not self.raw_data:
            print("Não há dados brutos para processar.")
            return
            
        parsed_list = []
        for repo in self.raw_data:
            parsed_list.append({
                'name': repo.get('full_name'),
                'stars': repo.get('stargazers_count'),
                'forks': repo.get('forks_count'),
                'language': repo.get('language'),
                'license': repo.get('license', {}).get('spdx_id') if repo.get('license') else 'No License',
                'open_issues': repo.get('open_issues_count'),
                'created_at': repo.get('created_at'),
                'description': repo.get('description'),
                'url': repo.get('html_url')
            })
        
        self.dataframe = pd.DataFrame(parsed_list)

    def _save_to_csv(self):
        """Salva o DataFrame processado em um arquivo CSV."""
        if self.dataframe is None:
            print("Não há DataFrame para salvar.")
            return

        # Garante que os diretórios de saída existam
        os.makedirs(os.path.dirname(self.csv_filepath), exist_ok=True)
        
        self.dataframe.to_csv(self.csv_filepath, index=False)
        print(f"\nDados salvos com sucesso em: {self.csv_filepath}")

    def run(self):
        """
        Método principal que executa todo o fluxo de coleta e salvamento.
        Este é o método que será chamado de fora da classe.
        """
        if self._fetch_all_repos():
            self._parse_data()
            self._save_to_csv()