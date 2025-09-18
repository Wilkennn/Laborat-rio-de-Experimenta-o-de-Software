# tests/test_api_connectivity.py

import pytest
import requests
from src import config

# Marcador para pular os testes se o token não estiver configurado.
# Isso evita que os testes falhem por um problema de configuração.
requires_token = pytest.mark.skipif(
    not config.GITHUB_TOKEN,
    reason="Token de API do GitHub não configurado no arquivo .env"
)

@requires_token
def test_github_api_connectivity_and_auth():
    """
    Testa a conectividade básica e a autenticação com a API GraphQL do GitHub.
    Verifica se a resposta é bem-sucedida e contém o login do usuário.
    """
    test_query = """
    query {
        viewer {
            login
        }
    }
    """
    
    response = requests.post(
        config.GRAPHQL_API_URL,
        headers=config.HEADERS,
        json={'query': test_query},
        timeout=10
    )
    
    # 1. Verifica se a requisição HTTP foi bem-sucedida (código 200)
    assert response.status_code == 200, f"Falha na requisição HTTP: {response.text}"
    
    data = response.json()
    
    # 2. Garante que não há erros na resposta da API GraphQL
    assert "errors" not in data, f"API retornou erros: {data.get('errors')}"
    
    # 3. Valida se a estrutura de dados esperada está presente
    assert "data" in data, "Chave 'data' não encontrada na resposta."
    assert "viewer" in data["data"], "Objeto 'viewer' não encontrado nos dados."
    assert "login" in data["data"]["viewer"], "Login do usuário não encontrado."
    
    print(f"\n✅ Conectado como: {data['data']['viewer']['login']}")


@requires_token
def test_search_repositories_query():
    """
    Testa uma consulta para buscar repositórios populares.
    Verifica se a API retorna uma lista de repositórios sem erros.
    """
    repo_query = """
    query {
        search(query: "stars:>100000", type: REPOSITORY, first: 2) {
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
    
    response = requests.post(
        config.GRAPHQL_API_URL,
        headers=config.HEADERS,
        json={'query': repo_query},
        timeout=15
    )
    
    # 1. Verifica se a requisição HTTP foi bem-sucedida
    assert response.status_code == 200, f"Falha na requisição HTTP: {response.text}"
    
    data = response.json()
    
    # 2. Garante que não há erros na resposta da API
    assert "errors" not in data, f"API retornou erros: {data.get('errors')}"
    
    # 3. Valida a estrutura e o conteúdo da resposta
    assert "data" in data
    nodes = data["data"]["search"]["nodes"]
    assert isinstance(nodes, list), "O resultado da busca não é uma lista."
    assert len(nodes) > 0, "A busca não retornou nenhum repositório."
    
    # Imprime os resultados para visualização (opcional)
    print("\n✅ Repositórios encontrados:")
    for repo in nodes:
        name = repo.get('nameWithOwner', 'N/A')
        stars = repo.get('stargazers', {}).get('totalCount', 0)
        print(f"  - {name} ({stars:,} ⭐)")