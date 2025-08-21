"""
Arquivo para testar query GraphQL simplificada
"""
import requests
import json
from src import config

def test_simple_query():
    query = """
    query TopRepos {
      search(
        query: "stars:>1 sort:stars-desc",
        type: REPOSITORY,
        first: 3
      ) {
        nodes {
          ... on Repository {
            nameWithOwner
            stargazers {
              totalCount
            }
          }
        }
      }
    }
    """
    
    headers = {
        'Authorization': f'token {config.GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json={'query': query}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print(f"Erros GraphQL: {data['errors']}")
        else:
            repos = data['data']['search']['nodes']
            print(f"✅ Sucesso! Encontrados {len(repos)} repositórios")
            for repo in repos:
                print(f"  - {repo['nameWithOwner']}: {repo['stargazers']['totalCount']} ⭐")
    else:
        print(f"❌ Erro HTTP: {response.text}")

if __name__ == "__main__":
    test_simple_query()
