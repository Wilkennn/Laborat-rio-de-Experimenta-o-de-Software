# tests/test_simple_query.py

import pytest
import requests
from src import config

# Marcador para pular o teste se o token não estiver configurado.
# Essencial para testes que dependem de uma API externa e autenticação.
requires_token = pytest.mark.skipif(
    not config.GITHUB_TOKEN,
    reason="Token de API do GitHub não configurado no arquivo .env"
)

@requires_token
def test_simple_repository_query():
    """
    Testa uma query GraphQL simples para buscar 3 repositórios populares.
    Valida o status da resposta, a ausência de erros e a estrutura dos dados.
    """
    query = """
    query TopRepos {
        search(query: "stars:>1 sort:stars-desc", type: REPOSITORY, first: 3) {
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
        config.GRAPHQL_API_URL,  # Reutilizando a URL do seu arquivo de configuração
        headers=config.HEADERS,    # Reutilizando os headers do seu arquivo de configuração
        json={'query': query},
        timeout=15
    )
    
    # 1. Valida se a requisição HTTP foi bem-sucedida (status 200)
    assert response.status_code == 200, f"Falha na requisição HTTP: {response.text}"
    
    data = response.json()
    
    # 2. Garante que não há erros na resposta da API GraphQL
    assert "errors" not in data, f"A API retornou erros: {data.get('errors')}"
    
    # 3. Valida a estrutura da resposta e se o número de resultados está correto
    assert "data" in data, "A chave 'data' não foi encontrada na resposta."
    repos = data["data"]["search"]["nodes"]
    assert isinstance(repos, list), "O resultado da busca não é uma lista."
    assert len(repos) == 3, "A consulta não retornou o número esperado de repositórios (3)."