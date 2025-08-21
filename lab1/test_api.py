#!/usr/bin/env python3
# Teste de conectividade com a API GraphQL do GitHub

import requests
from src import config

def test_github_api():
    print("=== TESTE DE CONECTIVIDADE COM GITHUB API ===")
    
    # Teste 1: Token configurado
    print(f"1. Token configurado: {'✅ SIM' if config.GITHUB_TOKEN else '❌ NÃO'}")
    
    if not config.GITHUB_TOKEN:
        print("❌ Configure o token no arquivo .env primeiro!")
        return False
    
    # Teste 2: GraphQL API
    print("2. Testando GraphQL API...")
    
    test_query = """
    query {
        viewer {
            login
        }
        rateLimit {
            limit
            remaining
            resetAt
        }
    }
    """
    
    try:
        response = requests.post(
            config.GRAPHQL_API_URL,
            headers=config.HEADERS,
            json={'query': test_query},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'errors' in data:
                print(f"❌ Erro na API: {data['errors']}")
                return False
            
            if 'data' in data:
                viewer = data['data'].get('viewer', {})
                rate_limit = data['data'].get('rateLimit', {})
                
                print(f"✅ GraphQL conectado com sucesso!")
                print(f"   Usuário: {viewer.get('login', 'N/A')}")
                print(f"   Rate limit: {rate_limit.get('remaining', 0)}/{rate_limit.get('limit', 0)}")
                return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

# Teste 3: Consulta simples de repositórios
def test_repo_query():
    print("\n3. Testando consulta de repositórios...")
    
    repo_query = """
    query {
        search(
            query: "stars:>100000 sort:stars-desc",
            type: REPOSITORY,
            first: 2
        ) {
            nodes {
                ... on Repository {
                    nameWithOwner
                    stargazers {
                        totalCount
                    }
                    createdAt
                    primaryLanguage {
                        name
                    }
                }
            }
        }
    }
    """
    
    try:
        response = requests.post(
            config.GRAPHQL_API_URL,
            headers=config.HEADERS,
            json={'query': repo_query},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'errors' in data:
                print(f"❌ Erro na consulta: {data['errors']}")
                return False
            
            repos = data['data']['search']['nodes']
            print(f"✅ Consulta de repositórios funcionando!")
            print(f"   Encontrados: {len(repos)} repositórios")
            
            for repo in repos:
                name = repo.get('nameWithOwner', 'N/A')
                stars = repo.get('stargazers', {}).get('totalCount', 0)
                lang = repo.get('primaryLanguage', {})
                lang_name = lang.get('name', 'N/A') if lang else 'N/A'
                print(f"   - {name}: {stars:,} ⭐ ({lang_name})")
            
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
        return False

if __name__ == "__main__":
    api_ok = test_github_api()
    
    if api_ok:
        repo_ok = test_repo_query()
        
        if repo_ok:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ O sistema está pronto para executar!")
        else:
            print("\n❌ Problema na consulta de repositórios")
    else:
        print("\n❌ Problema na conexão com a API")
