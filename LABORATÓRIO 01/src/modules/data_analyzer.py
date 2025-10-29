import pandas as pd
import numpy as np
from datetime import datetime
import os
from .. import config

class DataAnalyzer:
    
    def __init__(self, csv_filepath=None):
        self.csv_filepath = csv_filepath or config.CSV_FILEPATH
        self.dataframe = None
        self.results = {}
    
    def load_data(self):
        if not os.path.exists(self.csv_filepath):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {self.csv_filepath}")
        
        self.dataframe = pd.read_csv(self.csv_filepath)
        print(f"Dados carregados: {len(self.dataframe)} repositórios")
        return self.dataframe
    
    def analyze_repository_age(self):
        # RQ01: Sistemas populares são maduros?
        if self.dataframe is None:
            self.load_data()
        
        self.dataframe['created_at'] = pd.to_datetime(self.dataframe['created_at']).dt.tz_localize(None)
        current_date = datetime.now()
        self.dataframe['age_years'] = (current_date - self.dataframe['created_at']).dt.days / 365.25
        
        median_age = self.dataframe['age_years'].median()
        self.results['RQ01'] = {
            'median_age_years': median_age,
            'description': f"Idade mediana dos repositórios: {median_age:.2f} anos"
        }
        
        return self.results['RQ01']
    
    def analyze_external_contributions(self):
        """
        RQ02: Sistemas populares recebem muita contribuição externa?
        Métrica: total de pull requests aceitas (merged)
        """
        if self.dataframe is None:
            self.load_data()
        
        median_prs = self.dataframe['merged_pull_requests'].median()
        self.results['RQ02'] = {
            'median_merged_prs': median_prs,
            'description': f"Mediana de PRs aceitas: {median_prs}"
        }
        
        return self.results['RQ02']
    
    def analyze_release_frequency(self):
        # RQ03: Frequência de releases
        if self.dataframe is None:
            self.load_data()
        
        median_releases = self.dataframe['releases'].median()
        self.results['RQ03'] = {
            'median_releases': median_releases,
            'description': f"Mediana de releases: {median_releases}"
        }
        
        return self.results['RQ03']
    
    def analyze_update_frequency(self):
        # RQ04: Frequência de atualizações
        if self.dataframe is None:
            self.load_data()
        
        self.dataframe['updated_at'] = pd.to_datetime(self.dataframe['updated_at']).dt.tz_localize(None)
        current_date = datetime.now()
        self.dataframe['days_since_update'] = (current_date - self.dataframe['updated_at']).dt.days
        
        median_days = self.dataframe['days_since_update'].median()
        self.results['RQ04'] = {
            'median_days_since_update': median_days,
            'description': f"Mediana de dias desde última atualização: {median_days}"
        }
        
        return self.results['RQ04']
    
    def analyze_popular_languages(self):
        """
        RQ05: Sistemas populares são escritos nas linguagens mais populares?
        Métrica: linguagem primária de cada repositório
        """
        if self.dataframe is None:
            self.load_data()
        
        language_counts = self.dataframe['language'].value_counts()
        self.results['RQ05'] = {
            'language_distribution': language_counts.to_dict(),
            'top_languages': language_counts.head(10).to_dict(),
            'description': f"Top 3 linguagens: {list(language_counts.head(3).index)}"
        }
        
        return self.results['RQ05']
    
    def analyze_issues_closure_rate(self):
        """
        RQ06: Sistemas populares possuem um alto percentual de issues fechadas?
        Métrica: razão entre número de issues fechadas pelo total de issues
        """
        if self.dataframe is None:
            self.load_data()
        
        # Calcular taxa de fechamento de issues
        self.dataframe['total_issues'] = self.dataframe['open_issues'] + self.dataframe['closed_issues']
        self.dataframe['issues_closure_rate'] = np.where(
            self.dataframe['total_issues'] > 0,
            self.dataframe['closed_issues'] / self.dataframe['total_issues'],
            0
        )
        
        median_closure_rate = self.dataframe['issues_closure_rate'].median()
        self.results['RQ06'] = {
            'median_closure_rate': median_closure_rate,
            'description': f"Taxa mediana de fechamento de issues: {median_closure_rate:.2%}"
        }
        
        return self.results['RQ06']
    
    def analyze_languages_vs_metrics(self):
        """
        RQ07 (BÔNUS): Sistemas escritos em linguagens mais populares recebem mais 
        contribuição externa, lançam mais releases e são atualizados com mais frequência?
        """
        if self.dataframe is None:
            self.load_data()
        
        # Definir linguagens populares (top 5)
        top_languages = self.dataframe['language'].value_counts().head(5).index.tolist()
        
        results_by_language = {}
        
        for lang in top_languages:
            lang_data = self.dataframe[self.dataframe['language'] == lang]
            
            if len(lang_data) > 0:
                results_by_language[lang] = {
                    'count': len(lang_data),
                    'median_merged_prs': lang_data['merged_pull_requests'].median(),
                    'median_releases': lang_data['releases'].median(),
                    'median_days_since_update': lang_data['days_since_update'].median(),
                    'median_stars': lang_data['stars'].median(),
                    'median_age': lang_data['age_years'].median()
                }
        
        # Comparar com "outras linguagens"
        other_langs_data = self.dataframe[~self.dataframe['language'].isin(top_languages)]
        if len(other_langs_data) > 0:
            results_by_language['Outras'] = {
                'count': len(other_langs_data),
                'median_merged_prs': other_langs_data['merged_pull_requests'].median(),
                'median_releases': other_langs_data['releases'].median(),
                'median_days_since_update': other_langs_data['days_since_update'].median(),
                'median_stars': other_langs_data['stars'].median(),
                'median_age': other_langs_data['age_years'].median()
            }
        
        self.results['RQ07'] = {
            'results_by_language': results_by_language,
            'top_languages': top_languages,
            'description': "Análise das métricas por linguagem de programação"
        }
        
        return self.results['RQ07']
    
    def run_all_analyses(self):
        """
        Executa todas as análises das questões de pesquisa.
        """
        print("=== EXECUTANDO ANÁLISES DAS QUESTÕES DE PESQUISA ===\n")
        
        rq01 = self.analyze_repository_age()
        print(f"RQ01 - {rq01['description']}")
        
        rq02 = self.analyze_external_contributions()
        print(f"RQ02 - {rq02['description']}")
        
        rq03 = self.analyze_release_frequency()
        print(f"RQ03 - {rq03['description']}")
        
        rq04 = self.analyze_update_frequency()
        print(f"RQ04 - {rq04['description']}")
        
        rq05 = self.analyze_popular_languages()
        print(f"RQ05 - {rq05['description']}")
        
        rq06 = self.analyze_issues_closure_rate()
        print(f"RQ06 - {rq06['description']}")
        
        rq07 = self.analyze_languages_vs_metrics()
        print(f"RQ07 (BÔNUS) - {rq07['description']}")
        
        print("\n=== ANÁLISES CONCLUÍDAS ===")
        return self.results
