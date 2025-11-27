import requests
import time
import pandas as pd
import sys

GITHUB_TOKEN = "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" 

ORG_NAME = "facebook"
NUM_EXECUCOES = 30   
DESCARTAR_PRIMEIROS = 5  
INTERVALO_ENTRE_RODADAS = 1.5 

# URLs Base
URL_REST = "https://api.github.com"
URL_GRAPHQL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def validar_token():
    if "SEU_TOKEN" in GITHUB_TOKEN:
        print("ERRO: Você esqueceu de colocar seu Token do GitHub no script!")
        print("Edite a linha 'GITHUB_TOKEN' no início do arquivo.")
        sys.exit(1)

def medir_request(func):
    """
    Executa uma função de cenário e mede:
    - Tempo (ms)
    - Tamanho (bytes)
    - Número de Requisições HTTP (n)
    """
    def wrapper():
        start_time = time.time()
        try:
            tamanho, n_reqs = func() 
            end_time = time.time()
            tempo_ms = (end_time - start_time) * 1000
            return tempo_ms, tamanho, n_reqs
        except Exception as e:
            print(f"Erro na execução: {e}")
            return None, None, None
    return wrapper

# ==============================================================================
# CENÁRIO 1: CONSULTA ESCALAR (BASELINE)
# Objetivo: Pegar 4 campos simples do perfil.
# ==============================================================================

def cenario1_rest():
    # GET /orgs/facebook
    resp = requests.get(f"{URL_REST}/orgs/{ORG_NAME}", headers=HEADERS)
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
    resp = requests.post(URL_GRAPHQL, json={'query': query}, headers=HEADERS)
    return len(resp.content), 1 

# ==============================================================================
# CENÁRIO 2: LISTAGEM / COLEÇÃO (OVERFETCHING)
# Objetivo: Listar 50 repositórios (apenas nome e estrelas).
# ==============================================================================
def cenario2_rest():
    resp = requests.get(f"{URL_REST}/orgs/{ORG_NAME}/repos?per_page=50", headers=HEADERS)
    return len(resp.content), 1 # 

def cenario2_graphql():

    query = """
    query {
      organization(login: "facebook") {
        repositories(first: 50) {
          nodes {
            name
            stargazerCount
          }
        }
      }
    }
    """
    resp = requests.post(URL_GRAPHQL, json={'query': query}, headers=HEADERS)
    return len(resp.content), 1 

# ==============================================================================
# CENÁRIO 3: DASHBOARD COMPLEXA (N+1 / UNDERFETCHING)
# Objetivo: 5 Repos + Issues + Linguagens.
# ==============================================================================

def cenario3_rest():
    tamanho_total = 0
    n_requests = 0
    
    resp_repos = requests.get(f"{URL_REST}/orgs/{ORG_NAME}/repos?per_page=5", headers=HEADERS)
    repos = resp_repos.json()
    tamanho_total += len(resp_repos.content)
    n_requests += 1
    
    for repo in repos:
        repo_name = repo['name']
        
        resp_issues = requests.get(f"{URL_REST}/repos/{ORG_NAME}/{repo_name}/issues?per_page=3", headers=HEADERS)
        tamanho_total += len(resp_issues.content)
        n_requests += 1
        
        resp_langs = requests.get(f"{URL_REST}/repos/{ORG_NAME}/{repo_name}/languages", headers=HEADERS)
        tamanho_total += len(resp_langs.content)
        n_requests += 1
        
    # Esperado: 1 (lista) + 5 (issues) + 5 (langs) = 11 Requisições
    return tamanho_total, n_requests 

def cenario3_graphql():
    query = """
    query {
      organization(login: "facebook") {
        repositories(first: 5) {
          nodes {
            name
            issues(last: 3) {
              nodes { title }
            }
            languages(first: 3) {
              nodes { name }
            }
          }
        }
      }
    }
    """
    resp = requests.post(URL_GRAPHQL, json={'query': query}, headers=HEADERS)
    return len(resp.content), 1 # Apenas 1 Requisição

# ==============================================================================
# LOOP PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    validar_token()
    
    resultados = []
    print(f"--- INICIANDO EXPERIMENTO CONTROLADO ---")
    print(f"Alvo: {ORG_NAME}")
    print(f"Rodadas: {NUM_EXECUCOES} (Descartando as {DESCARTAR_PRIMEIROS} primeiras)")
    print("-" * 50)

    for i in range(1, NUM_EXECUCOES + 1):
        print(f"Executando Rodada {i}/{NUM_EXECUCOES}...", end="\r")
        
        valido = i > DESCARTAR_PRIMEIROS
                
        t_r1, s_r1, n_r1 = medir_request(cenario1_rest)()
        t_g1, s_g1, n_g1 = medir_request(cenario1_graphql)()
        
        t_r2, s_r2, n_r2 = medir_request(cenario2_rest)()
        t_g2, s_g2, n_g2 = medir_request(cenario2_graphql)()
        
        t_r3, s_r3, n_r3 = medir_request(cenario3_rest)()
        t_g3, s_g3, n_g3 = medir_request(cenario3_graphql)()
        
        def registrar(cenario, tec, tempo, tam, reqs):
            resultados.append({
                "rodada": i,
                "valido": valido,
                "cenario": cenario,
                "tecnologia": tec,
                "tempo_ms": tempo,
                "tamanho_bytes": tam,
                "n_requests": reqs
            })

        registrar("1_Scalar", "REST", t_r1, s_r1, n_r1)
        registrar("1_Scalar", "GraphQL", t_g1, s_g1, n_g1)
        
        registrar("2_Listagem", "REST", t_r2, s_r2, n_r2)
        registrar("2_Listagem", "GraphQL", t_g2, s_g2, n_g2)
        
        registrar("3_Dashboard", "REST", t_r3, s_r3, n_r3)
        registrar("3_Dashboard", "GraphQL", t_g3, s_g3, n_g3)
        
        time.sleep(INTERVALO_ENTRE_RODADAS)

    print("\n\n--- EXPERIMENTO CONCLUÍDO! ---")
    
    # Salva em CSV
    df = pd.DataFrame(resultados)
    nome_arquivo = "resultados_experimento_final.csv"
    df.to_csv(nome_arquivo, index=False)
    
    print(f"Dados salvos em: {nome_arquivo}")
    
    if not df.empty:
        print("\n--- RESUMO DAS MÉDIAS (DADOS VÁLIDOS) ---")
        df_valido = df[df['valido'] == True]
        resumo = df_valido.groupby(['cenario', 'tecnologia'])[['tempo_ms', 'tamanho_bytes', 'n_requests']].mean()
        print(resumo)