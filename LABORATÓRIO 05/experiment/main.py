import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import pandas as pd
import sys

# ==============================================================================
# CONFIGURAÇÃO DO EXPERIMENTO
# ==============================================================================

# 1. INSIRA SEU TOKEN AQUI
GITHUB_TOKEN = "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" 

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
    if "SEU_TOKEN" in GITHUB_TOKEN:
        print("ERRO: Você esqueceu de colocar seu Token do GitHub no script!")
        sys.exit(1)

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
    print(f"--- INICIANDO EXPERIMENTO BLINDADO ---")
    
    for i in range(1, NUM_EXECUCOES + 1):
        print(f"Executando Rodada {i}/{NUM_EXECUCOES}...", end="\r")
        valido = i > DESCARTAR_PRIMEIROS
        
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

    print("\n--- Concluído ---")
    df = pd.DataFrame(resultados)
    df.to_csv("resultados_experimento_final.csv", index=False)
    print("Salvo: resultados_experimento_final.csv")
    
    if not df.empty:
        print(df[df['valido']==True].groupby(['cenario', 'tecnologia'])[['tempo_ms']].mean())