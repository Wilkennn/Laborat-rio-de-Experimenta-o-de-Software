import os
import requests
import pandas as pd
import subprocess
import shutil
import time
import json
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import *

class RestDataCollector:
    """
    Coletor de dados para repositórios Java do GitHub.
    Coleta os top 1000 repositórios Java e suas métricas de qualidade.
    """

    def __init__(self, ck_jar_path=DEFAULT_CK_PATH, test_mode=TEST_MODE):
        self.base_api_url = 'https://api.github.com'
        self.headers = HEADERS
        self.test_mode = test_mode
        self.ck_jar_path = ck_jar_path
        
        # Configurar quantidade de repos baseado no modo
        if test_mode:
            self.total_repos_to_fetch = TEST_REPOS_COUNT
            self.csv_filepath = CSV_TEST_FILEPATH
            print("Modo de teste: analisando apenas 1 repositório")
        else:
            self.total_repos_to_fetch = TOTAL_REPOS_TO_FETCH
            self.csv_filepath = CSV_FILEPATH
            print(f"Modo completo: analisando {self.total_repos_to_fetch} repositórios")
        
        self.repos_per_page = REPOS_PER_PAGE
        self.raw_data = []
        self.dataframe = None
        
        # Criar diretórios necessários
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        # Verificar ferramenta CK (opcional)
        self.ck_available = self._check_ck_tool()

    def _check_ck_tool(self):
        if not os.path.exists(self.ck_jar_path):
            print(f"Aviso: Ferramenta CK não encontrada em: {self.ck_jar_path}")
            print("Continuando com coleta de métricas básicas")
            return False
        
        try:
            result = subprocess.run([
                "java", "-jar", self.ck_jar_path, "--help"
            ], capture_output=True, text=True, timeout=10)
            print("Ferramenta CK verificada com sucesso")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            print("Aviso: Java não encontrado ou ferramenta CK não funcional")
            print("Continuando com coleta de métricas básicas")
            return Falseess
import shutil
import time
import json
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import *

class RestDataCollector:
    """
    Coletor de dados para repositórios Java do GitHub.
    Coleta os top 1000 repositórios Java e suas métricas de qualidade.
    """

    def __init__(self, ck_jar_path=DEFAULT_CK_PATH, test_mode=TEST_MODE):
        self.base_api_url = 'https://api.github.com'
        self.headers = HEADERS
        self.test_mode = test_mode
        self.ck_jar_path = ck_jar_path
        
        # Configurar quantidade de repos baseado no modo
        if test_mode:
            self.total_repos_to_fetch = TEST_REPOS_COUNT
            self.csv_filepath = CSV_TEST_FILEPATH
            print("Modo de teste: analisando apenas 1 repositório")
        else:
            self.total_repos_to_fetch = TOTAL_REPOS_TO_FETCH
            self.csv_filepath = CSV_FILEPATH
            print(f"Modo completo: analisando {self.total_repos_to_fetch} repositórios")
        
        self.repos_per_page = REPOS_PER_PAGE
        self.raw_data = []
        self.dataframe = None
        
        # Criar diretórios necessários
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        # Verificar ferramenta CK (opcional)
        self.ck_available = self._check_ck_tool()

    def _check_ck_tool(self):
        """Verifica se a ferramenta CK está disponível (não obrigatório)."""
        if not os.path.exists(self.ck_jar_path):
            print(f"⚠️  AVISO: Ferramenta CK não encontrada em: {self.ck_jar_path}")
            print("� Continuando com coleta de métricas básicas (sem análise CK)")
            return False
        
        try:
            result = subprocess.run([
                "java", "-jar", self.ck_jar_path, "--help"
            ], capture_output=True, text=True, timeout=10)
            print("✅ Ferramenta CK verificada com sucesso")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  AVISO: Java não encontrado ou ferramenta CK não funcional")
            print("� Continuando com coleta de métricas básicas")
            return False

    def _make_api_request(self, url, params=None):
        """Faz requisições à API do GitHub com tratamento de rate limiting."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                # Verificar rate limit
                remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
                if remaining < 10:
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    sleep_time = max(0, reset_time - int(time.time())) + 1
                    print(f"Rate limit baixo ({remaining}). Aguardando {sleep_time}s...")
                    time.sleep(sleep_time)
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print("Limite de rate da API atingido. Aguardando...")
                    time.sleep(60)
                    continue
                elif 500 <= e.response.status_code < 600:
                    print(f"Erro de servidor ({e.response.status_code}). Tentativa {attempt+1}/{max_retries}")
                    time.sleep(5)
                    continue
                else:
                    print(f"Erro HTTP {e.response.status_code}: {e}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"Erro de rede: {e}. Tentativa {attempt+1}/{max_retries}")
                time.sleep(5)
        
        print("Todas as tentativas falharam")
        return None

    def fetch_top_java_repos_list(self):
        """Busca a lista dos top repositórios Java mais populares."""
        print("\nColetando lista dos repositórios Java mais populares")
        print("="*50)
        
        search_url = f"{self.base_api_url}/search/repositories"
        repo_list = []
        total_pages = (self.total_repos_to_fetch + self.repos_per_page - 1) // self.repos_per_page
        
        for page in range(1, total_pages + 1):
            params = {
                'q': 'language:java stars:>100',
                'sort': 'stars',
                'order': 'desc',
                'per_page': self.repos_per_page,
                'page': page
            }
            
            print(f"Buscando página {page}/{total_pages}...")
            response = self._make_api_request(search_url, params=params)
            
            if response:
                items = response.json().get('items', [])
                repo_list.extend(items)
                print(f"Página {page} coletada: {len(items)} repositórios")
                
                # Limitar ao número exato solicitado
                if len(repo_list) >= self.total_repos_to_fetch:
                    repo_list = repo_list[:self.total_repos_to_fetch]
                    break
                    
                time.sleep(1)  # Respeitar rate limit
            else:
                print(f"Falha ao coletar página {page}")
                break
        
        if not repo_list:
            print("Nenhum repositório encontrado")
            return None
        
        # Salvar lista de repositórios
        repos_df = pd.DataFrame([{
            'rank': i + 1,
            'name': repo['full_name'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'language': repo['language'],
            'description': repo['description'],
            'url': repo['html_url'],
            'clone_url': repo['clone_url'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at']
        } for i, repo in enumerate(repo_list)])
        
        repos_df.to_csv(REPOS_LIST_FILEPATH, index=False)
        print(f"Lista salva em: {REPOS_LIST_FILEPATH}")
        print(f"Total coletado: {len(repo_list)} repositórios")
        
        return repo_list

    def collect_repository_metrics(self, repo_info):
        """Coleta métricas detalhadas de um repositório específico."""
        repo_name = repo_info['full_name']
        print(f"\nColetando métricas para: {repo_name}")
        
        # Preparar diretórios
        safe_name = repo_name.replace("/", "_")
        repo_dir = os.path.join(TEMP_DIR, safe_name)
        ck_output_dir = os.path.join(TEMP_DIR, f"{safe_name}_metrics")
        
        # Limpar diretórios existentes
        shutil.rmtree(repo_dir, ignore_errors=True)
        shutil.rmtree(ck_output_dir, ignore_errors=True)
        os.makedirs(ck_output_dir, exist_ok=True)
        
        metrics = {
            'name': repo_name,
            'url': repo_info['html_url'],
            'clone_url': repo_info['clone_url'],
            'language': repo_info['language'],
            'description': repo_info['description'],
            'created_at': repo_info['created_at'],
            'updated_at': repo_info['updated_at']
        }
        
        try:
            # Métricas de processo via API
            print("  Coletando métricas de processo...")
            
            # Popularidade (estrelas)
            metrics['stars'] = repo_info['stargazers_count']
            metrics['forks'] = repo_info['forks_count']
            metrics['watchers'] = repo_info['watchers_count']
            
            # Atividade (releases)
            releases_url = f"{self.base_api_url}/repos/{repo_name}/releases"
            releases_response = self._make_api_request(releases_url, params={'per_page': 1})
            if releases_response:
                try:
                    # Contar total de releases via header Link
                    link_header = releases_response.headers.get('Link', '')
                    if 'rel="last"' in link_header:
                        last_page = [s for s in link_header.split(',') if 'rel="last"' in s][0]
                        releases_count = int(last_page.split('page=')[1].split('>')[0])
                    else:
                        releases_count = len(releases_response.json())
                except:
                    releases_count = 0
            else:
                releases_count = 0
            metrics['releases'] = releases_count
            
            # Maturidade (idade em anos)
            created_date = datetime.strptime(repo_info['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            age_years = round((datetime.utcnow() - created_date).days / 365.25, 2)
            metrics['age_years'] = age_years
            
            # Contribuidores
            contributors_url = f"{self.base_api_url}/repos/{repo_name}/contributors"
            contributors_response = self._make_api_request(contributors_url, params={'per_page': 1})
            if contributors_response:
                try:
                    link_header = contributors_response.headers.get('Link', '')
                    if 'rel="last"' in link_header:
                        last_page = [s for s in link_header.split(',') if 'rel="last"' in s][0]
                        contributors_count = int(last_page.split('page=')[1].split('>')[0])
                    else:
                        contributors_count = len(contributors_response.json())
                except:
                    contributors_count = 1
            else:
                contributors_count = 1
            metrics['contributors'] = contributors_count
            
            # Clonar repositório
            print("  Clonando repositório...")
            clone_cmd = ["git", "clone", "--depth", "1", repo_info['clone_url'], repo_dir]
            result = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"  Erro ao clonar: {result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, clone_cmd)
            
            print("  Repositório clonado com sucesso")
            
            # Análise de qualidade
            if self.ck_available:
                print("  Executando análise CK...")
                ck_cmd = ["java", "-jar", self.ck_jar_path, repo_dir, ck_output_dir]
                result = subprocess.run(ck_cmd, capture_output=True, text=True, timeout=600)
                
                if result.returncode != 0:
                    print(f"  CK retornou código {result.returncode}: {result.stderr}")
                
                # Processar resultados do CK
                metrics.update(self._process_ck_results(ck_output_dir))
                print("  Métricas de qualidade coletadas")
            else:
                print("  Usando métricas básicas (CK não disponível)")
                metrics.update(self._get_basic_code_metrics(repo_dir))
            
        except subprocess.TimeoutExpired:
            print("  Timeout na coleta - repositório muito grande")
            metrics.update(self._get_default_quality_metrics())
        except subprocess.CalledProcessError as e:
            print(f"  Erro no processo: {e}")
            metrics.update(self._get_default_quality_metrics())
        except Exception as e:
            print(f"  Erro inesperado: {e}")
            metrics.update(self._get_default_quality_metrics())
        finally:
            # Limpar arquivos temporários
            shutil.rmtree(repo_dir, ignore_errors=True)
            shutil.rmtree(ck_output_dir, ignore_errors=True)
        
        print(f"  Métricas coletadas para {repo_name}")
        return metrics

    def _process_ck_results(self, ck_output_dir):
        """Processa os arquivos CSV gerados pela ferramenta CK."""
        quality_metrics = self._get_default_quality_metrics()
        
        try:
            # Arquivo principal com métricas de classe
            class_csv = os.path.join(ck_output_dir, "class.csv")
            method_csv = os.path.join(ck_output_dir, "method.csv")
            
            if os.path.exists(class_csv):
                df_class = pd.read_csv(class_csv)
                if not df_class.empty:
                    # Métricas de qualidade (valores médios)
                    quality_metrics['cbo_avg'] = round(df_class['cbo'].mean(), 2)
                    quality_metrics['cbo_max'] = int(df_class['cbo'].max())
                    quality_metrics['dit_avg'] = round(df_class['dit'].mean(), 2)
                    quality_metrics['dit_max'] = int(df_class['dit'].max())
                    quality_metrics['lcom_avg'] = round(df_class['lcom'].mean(), 2)
                    quality_metrics['lcom_max'] = int(df_class['lcom'].max())
                    
                    # Métricas de tamanho
                    quality_metrics['loc_total'] = int(df_class['loc'].sum())
                    quality_metrics['loc_comments_total'] = int(df_class['locComment'].sum())
                    quality_metrics['classes_count'] = len(df_class)
                    
                    # Outras métricas úteis
                    quality_metrics['wmc_avg'] = round(df_class['wmc'].mean(), 2) if 'wmc' in df_class.columns else 0
                    quality_metrics['noc_avg'] = round(df_class['noc'].mean(), 2) if 'noc' in df_class.columns else 0
            
            if os.path.exists(method_csv):
                df_method = pd.read_csv(method_csv)
                if not df_method.empty:
                    quality_metrics['methods_count'] = len(df_method)
                    quality_metrics['cc_avg'] = round(df_method['cc'].mean(), 2) if 'cc' in df_method.columns else 0
            
        except Exception as e:
            print(f"  Erro ao processar resultados CK: {e}")
        
        return quality_metrics

    def _get_basic_code_metrics(self, repo_dir):
        """Coleta métricas básicas de código sem usar CK."""
        metrics = self._get_default_quality_metrics()
        
        try:
            # Contar arquivos Java e estimar métricas básicas
            java_files = []
            for root, dirs, files in os.walk(repo_dir):
                for file in files:
                    if file.endswith('.java'):
                        java_files.append(os.path.join(root, file))
            
            if java_files:
                total_loc = 0
                total_comments = 0
                total_classes = 0
                total_methods = 0
                
                for java_file in java_files[:50]:  # Limitar para não demorar muito
                    try:
                        with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            
                        # Contar LOC
                        code_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
                        total_loc += len(code_lines)
                        
                        # Contar comentários
                        comment_lines = [line for line in lines if line.strip().startswith('//')]
                        total_comments += len(comment_lines)
                        
                        # Estimar classes
                        class_lines = [line for line in lines if ' class ' in line]
                        total_classes += len(class_lines)
                        
                        # Estimar métodos
                        method_lines = [line for line in lines if '(' in line and '{' in line and not any(keyword in line for keyword in ['if', 'for', 'while', 'switch'])]
                        total_methods += len(method_lines)
                        
                    except Exception:
                        continue
                
                # Extrapolar para todos os arquivos se necessário
                if len(java_files) > 50:
                    factor = len(java_files) / 50
                    total_loc = int(total_loc * factor)
                    total_comments = int(total_comments * factor)
                    total_classes = int(total_classes * factor)
                    total_methods = int(total_methods * factor)
                
                metrics.update({
                    'loc_total': total_loc,
                    'loc_comments_total': total_comments,
                    'classes_count': total_classes,
                    'methods_count': total_methods,
                    'java_files_count': len(java_files)
                })
                
        except Exception as e:
            print(f"  Erro ao calcular métricas básicas: {e}")
        
        return metrics

    def _get_default_quality_metrics(self):
        """Retorna métricas de qualidade padrão (zeros) quando CK falha."""
        return {
            'loc_total': 0,
            'loc_comments_total': 0,
            'classes_count': 0,
            'methods_count': 0,
            'cbo_avg': 0.0,
            'cbo_max': 0,
            'dit_avg': 0.0,
            'dit_max': 0,
            'lcom_avg': 0.0,
            'lcom_max': 0,
            'wmc_avg': 0.0,
            'noc_avg': 0.0,
            'cc_avg': 0.0
        }

    def run_sprint1(self):
        """Executa a Sprint 1: coleta dos repositórios e suas métricas."""
        print("\nIniciando Sprint 1")
        print("="*30)
        print("Requisitos:")
        print("- Lista dos repositórios Java")
        print("- Script de automação de clone e coleta")
        print("- Arquivo CSV com métricas")
        print("="*30)
        
        start_time = time.time()
        
        # Etapa 1: Buscar lista de repositórios
        repo_list = self.fetch_top_java_repos_list()
        if not repo_list:
            print("Falha ao obter lista de repositórios")
            return False
        
        # Etapa 2: Coletar métricas detalhadas
        print("\nColetando métricas detalhadas dos repositórios")
        print("="*50)
        
        collected_data = []
        total_repos = len(repo_list)
        
        for i, repo in enumerate(repo_list):
            print(f"\nProgresso: {i+1}/{total_repos}")
            metrics = self.collect_repository_metrics(repo)
            collected_data.append(metrics)
            
            # Backup incremental a cada 10 repositórios
            if (i + 1) % 10 == 0 or i == total_repos - 1:
                self._save_intermediate_results(collected_data, i + 1)
        
        # Etapa 3: Salvar resultados finais
        print("\nSalvando resultados finais")
        print("="*30)
        
        self.dataframe = pd.DataFrame(collected_data)
        self._save_final_results()
        
        # Relatório final
        elapsed_time = time.time() - start_time
        print(f"\nSprint 1 concluída com sucesso!")
        print(f"Tempo total: {elapsed_time:.1f} segundos")
        print(f"Repositórios analisados: {len(collected_data)}")
        print(f"Arquivos gerados:")
        print(f"- Lista de repositórios: {REPOS_LIST_FILEPATH}")
        print(f"- Métricas detalhadas: {self.csv_filepath}")
        
        return True

    def _save_intermediate_results(self, data, count):
        """Salva backup intermediário."""
        temp_df = pd.DataFrame(data)
        temp_file = self.csv_filepath.replace('.csv', f'_temp_{count}.csv')
        temp_df.to_csv(temp_file, index=False)
        print(f"  Backup salvo: {count} repositórios")

    def _save_final_results(self):
        """Salva os resultados finais em CSV."""
        if self.dataframe is None or self.dataframe.empty:
            print("Nenhum dado para salvar")
            return
        
        # Reorganizar colunas para melhor legibilidade
        column_order = [
            'name', 'url', 'language', 'description', 'created_at', 'updated_at',
            # Métricas de Processo
            'stars', 'forks', 'watchers', 'contributors', 'releases', 'age_years',
            # Métricas de Qualidade (CK)
            'loc_total', 'loc_comments_total', 'classes_count', 'methods_count',
            'cbo_avg', 'cbo_max', 'dit_avg', 'dit_max', 'lcom_avg', 'lcom_max',
            'wmc_avg', 'noc_avg', 'cc_avg', 'clone_url'
        ]
        
        # Reorganizar DataFrame
        available_columns = [col for col in column_order if col in self.dataframe.columns]
        self.dataframe = self.dataframe[available_columns]
        
        # Salvar arquivo final
        self.dataframe.to_csv(self.csv_filepath, index=False)
        print(f"Resultados salvos em: {self.csv_filepath}")
        
        # Mostrar resumo estatístico
        self._print_summary_statistics()

    def _print_summary_statistics(self):
        """Imprime estatísticas resumidas dos dados coletados."""
        print("\nResumo estatístico:")
        print("-" * 30)
        
        if 'stars' in self.dataframe.columns:
            print(f"Estrelas - Mediana: {self.dataframe['stars'].median():.0f}, Média: {self.dataframe['stars'].mean():.0f}")
        
        if 'age_years' in self.dataframe.columns:
            print(f"Idade - Mediana: {self.dataframe['age_years'].median():.1f} anos, Média: {self.dataframe['age_years'].mean():.1f} anos")
        
        if 'loc_total' in self.dataframe.columns:
            print(f"LOC - Mediana: {self.dataframe['loc_total'].median():.0f}, Média: {self.dataframe['loc_total'].mean():.0f}")
        
        if 'cbo_avg' in self.dataframe.columns:
            print(f"CBO - Mediana: {self.dataframe['cbo_avg'].median():.2f}, Média: {self.dataframe['cbo_avg'].mean():.2f}")
        
        if 'dit_avg' in self.dataframe.columns:
            print(f"DIT - Mediana: {self.dataframe['dit_avg'].median():.2f}, Média: {self.dataframe['dit_avg'].mean():.2f}")
        
        if 'lcom_avg' in self.dataframe.columns:
            print(f"LCOM - Mediana: {self.dataframe['lcom_avg'].median():.2f}, Média: {self.dataframe['lcom_avg'].mean():.2f}")
