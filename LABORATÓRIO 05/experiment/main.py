import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import pandas as pd
import sys
import logging
from datetime import datetime
import json
import os

# ==============================================================================
# CONFIGURAÇÃO DO EXPERIMENTO
# ==============================================================================

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'experimento_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 1. INSIRA SEU TOKEN AQUI
GITHUB_TOKEN = "TOKEN" 

# 2. Configurações Gerais
ORG_NAME = "facebook"
NUM_EXECUCOES = 30       
DESCARTAR_PRIMEIROS = 5  
INTERVALO_ENTRE_RODADAS = 2 # Aumentei um pouco para garantir

# URLs Base
URL_REST = "https://api.github.com"
URL_GRAPHQL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ==============================================================================
# CONFIGURAÇÃO DE SESSÃO ROBUSTA (A CURA PARA O TIMEOUT)
# ==============================================================================

def criar_sessao_robusta():
    session = requests.Session()
    # Configura retry: Tenta 3 vezes, parando 1s, 2s, 4s entre falhas (backoff)
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "POST", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS) # Já embute o token em tudo
    return session

# Cria a sessão global para ser usada em todas as funções
sessao = criar_sessao_robusta()

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def validar_token():
    if "TOKEN" in GITHUB_TOKEN or len(GITHUB_TOKEN) < 20:
        logger.error("Token do GitHub inválido ou não configurado!")
        print("ERRO: Você esqueceu de colocar seu Token do GitHub no script!")
        print("Edite a variável GITHUB_TOKEN no início do arquivo.")
        sys.exit(1)
    logger.info("Token validado com sucesso.")

def medir_request(func):
    def wrapper():
        start_time = time.time()
        try:
            # Passamos a sessão para a função usar
            tamanho, n_reqs = func() 
            end_time = time.time()
            tempo_ms = (end_time - start_time) * 1000
            return tempo_ms, tamanho, n_reqs
        except Exception as e:
            print(f"\n[ERRO] Falha na requisição: {e}")
            return None, None, None # Retorna nulo para não quebrar o CSV
    return wrapper

# ==============================================================================
# CENÁRIO 1: CONSULTA ESCALAR
# ==============================================================================

def cenario1_rest():
    # Timeout de 10s para não ficar travado
    resp = sessao.get(f"{URL_REST}/orgs/{ORG_NAME}", timeout=10)
    return len(resp.content), 1 

def cenario1_graphql():
    query = """
    query {
      organization(login: "facebook") {
        name
        description
        websiteUrl
        location
      }
    }
    """
    resp = sessao.post(URL_GRAPHQL, json={'query': query}, timeout=10)
    return len(resp.content), 1 

# ==============================================================================
# CENÁRIO 2: LISTAGEM 
# ==============================================================================

def cenario2_rest():
    resp = sessao.get(f"{URL_REST}/orgs/{ORG_NAME}/repos?per_page=50", timeout=15)
    return len(resp.content), 1 

def cenario2_graphql():
    query = """
    query {
      organization(login: "facebook") {
        repositories(first: 50) {
          nodes { name stargazerCount }
        }
      }
    }
    """
    resp = sessao.post(URL_GRAPHQL, json={'query': query}, timeout=15)
    return len(resp.content), 1 

# ==============================================================================
# CENÁRIO 3: DASHBOARD COMPLEXA
# ==============================================================================

def cenario3_rest():
    tamanho_total = 0
    n_requests = 0
    
    # 1. Lista Repos
    resp_repos = sessao.get(f"{URL_REST}/orgs/{ORG_NAME}/repos?per_page=5", timeout=10)
    repos = resp_repos.json()
    tamanho_total += len(resp_repos.content)
    n_requests += 1
    
    for repo in repos:
        repo_name = repo['name']
        
        # 2. Issues
        resp_issues = sessao.get(f"{URL_REST}/repos/{ORG_NAME}/{repo_name}/issues?per_page=3", timeout=10)
        tamanho_total += len(resp_issues.content)
        n_requests += 1
        
        # 3. Linguagens
        resp_langs = sessao.get(f"{URL_REST}/repos/{ORG_NAME}/{repo_name}/languages", timeout=10)
        tamanho_total += len(resp_langs.content)
        n_requests += 1
        
    return tamanho_total, n_requests 

def cenario3_graphql():
    query = """
    query {
      organization(login: "facebook") {
        repositories(first: 5) {
          nodes {
            name
            issues(last: 3) { nodes { title } }
            languages(first: 3) { nodes { name } }
          }
        }
      }
    }
    """
    resp = sessao.post(URL_GRAPHQL, json={'query': query}, timeout=15)
    return len(resp.content), 1 

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    validar_token()
    resultados = []
    
    print(f"\n{'='*60}")
    print(f"  EXPERIMENTO: GraphQL vs REST API")
    print(f"  Organização: {ORG_NAME}")
    print(f"  Total de Execuções: {NUM_EXECUCOES}")
    print(f"  Aquecimento (descartado): {DESCARTAR_PRIMEIROS} rodadas")
    print(f"{'='*60}\n")
    logger.info("Iniciando experimento...")
    
    inicio_experimento = time.time()
    
    for i in range(1, NUM_EXECUCOES + 1):
        valido = i > DESCARTAR_PRIMEIROS
        status = "[VÁLIDA]" if valido else "[AQUECIMENTO]"
        print(f"\nRodada {i}/{NUM_EXECUCOES} {status}")
        logger.info(f"Executando rodada {i}/{NUM_EXECUCOES} - Valida: {valido}")
        
        # Execuções
        t_r1, s_r1, n_r1 = medir_request(cenario1_rest)()
        t_g1, s_g1, n_g1 = medir_request(cenario1_graphql)()
        
        t_r2, s_r2, n_r2 = medir_request(cenario2_rest)()
        t_g2, s_g2, n_g2 = medir_request(cenario2_graphql)()
        
        t_r3, s_r3, n_r3 = medir_request(cenario3_rest)()
        t_g3, s_g3, n_g3 = medir_request(cenario3_graphql)()
        
        # Função auxiliar para salvar
        def registrar(cen, tec, tem, tam, req):
            # Só salva se não deu erro (não é None)
            if tem is not None:
                resultados.append({
                    "rodada": i, "valido": valido, "cenario": cen, "tecnologia": tec,
                    "tempo_ms": tem, "tamanho_bytes": tam, "n_requests": req
                })

        registrar("1_Scalar", "REST", t_r1, s_r1, n_r1)
        registrar("1_Scalar", "GraphQL", t_g1, s_g1, n_g1)
        registrar("2_Listagem", "REST", t_r2, s_r2, n_r2)
        registrar("2_Listagem", "GraphQL", t_g2, s_g2, n_g2)
        registrar("3_Dashboard", "REST", t_r3, s_r3, n_r3)
        registrar("3_Dashboard", "GraphQL", t_g3, s_g3, n_g3)
        
        time.sleep(INTERVALO_ENTRE_RODADAS)

    fim_experimento = time.time()
    duracao_total = fim_experimento - inicio_experimento
    
    print(f"\n{'='*60}")
    print(f"  EXPERIMENTO CONCLUÍDO!")
    print(f"  Duração Total: {duracao_total:.2f} segundos ({duracao_total/60:.2f} minutos)")
    print(f"  Medições Realizadas: {len(resultados)}")
    print(f"{'='*60}\n")
    logger.info(f"Experimento finalizado em {duracao_total:.2f}s. Processando resultados...")
    
    df = pd.DataFrame(resultados)
    
    # Salva CSV principal
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "resultados_experimento_final.csv")
    df.to_csv(csv_path, index=False)
    logger.info(f"CSV salvo em: {csv_path}")
    
    if not df.empty:
        # Filtra dados válidos
        df_valido = df[df['valido'] == True]
        
        # Análise estatística
        print("\n=== RESULTADOS (Apenas Rodadas Válidas) ===")
        print("\nMédia de Tempo (ms) por Cenário:")
        media_tempo = df_valido.groupby(['cenario', 'tecnologia'])[['tempo_ms']].mean()
        print(media_tempo)
        
        print("\nMédia de Tamanho (bytes) por Cenário:")
        media_tamanho = df_valido.groupby(['cenario', 'tecnologia'])[['tamanho_bytes']].mean()
        print(media_tamanho)
        
        print("\nNúmero de Requisições por Cenário:")
        media_requests = df_valido.groupby(['cenario', 'tecnologia'])[['n_requests']].mean()
        print(media_requests)
        
        # Calcula estatísticas detalhadas
        stats_summary = df_valido.groupby(['cenario', 'tecnologia']).agg({
            'tempo_ms': ['mean', 'std', 'min', 'max', 'median'],
            'tamanho_bytes': ['mean', 'std', 'min', 'max'],
            'n_requests': ['mean', 'max']
        }).reset_index()
        
        # Salva relatório JSON
        report = {
            'data_execucao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'configuracao': {
                'organizacao': ORG_NAME,
                'total_execucoes': NUM_EXECUCOES,
                'execucoes_descartadas': DESCARTAR_PRIMEIROS,
                'execucoes_validas': NUM_EXECUCOES - DESCARTAR_PRIMEIROS
            },
            'estatisticas': stats_summary.to_dict('records'),
            'resumo_geral': {
                'total_medicoes': len(df),
                'medicoes_validas': len(df_valido),
                'cenarios_testados': df['cenario'].nunique(),
                'tecnologias_comparadas': df['tecnologia'].nunique()
            }
        }
        
        json_path = os.path.join(output_dir, f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logger.info(f"Relatório JSON salvo em: {json_path}")
        
        # Calcula e exibe comparações
        print("\n=== COMPARAÇÃO DIRETA: GraphQL vs REST ===")
        for cenario in df_valido['cenario'].unique():
            df_cen = df_valido[df_valido['cenario'] == cenario]
            rest_tempo = df_cen[df_cen['tecnologia'] == 'REST']['tempo_ms'].mean()
            gql_tempo = df_cen[df_cen['tecnologia'] == 'GraphQL']['tempo_ms'].mean()
            rest_tam = df_cen[df_cen['tecnologia'] == 'REST']['tamanho_bytes'].mean()
            gql_tam = df_cen[df_cen['tecnologia'] == 'GraphQL']['tamanho_bytes'].mean()
            
            if rest_tempo > 0 and gql_tempo > 0:
                speedup = rest_tempo / gql_tempo
                reducao = rest_tam / gql_tam
                print(f"\n{cenario}:")
                print(f"  Speedup de Tempo: {speedup:.2f}x {'(GraphQL mais rápido)' if speedup > 1 else '(REST mais rápido)'}")
                print(f"  Redução de Dados: {reducao:.2f}x {'(GraphQL mais leve)' if reducao > 1 else '(REST mais leve)'}")
        
        logger.info("Análise concluída com sucesso!")
    else:
        logger.warning("Nenhum dado foi coletado!")