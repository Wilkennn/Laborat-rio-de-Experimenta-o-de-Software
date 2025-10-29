# Analisador de Repositórios Populares do GitHub

**Laboratório de Experimentação de Software - COMPLETO**  
**Sprints 1, 2 e 3 + Bonus implementadas**

Este projeto coleta e analisa dados dos 1.000 repositórios com o maior número de estrelas no GitHub para responder às questões de pesquisa do laboratório de experimentação.

## Funcionalidades Implementadas

### Sprint 1 (3 pontos) 
- Consulta GraphQL para 100 repositórios
- Requisição automática com paginação
- Todos os dados/métricas necessários para as RQs

### Sprint 2 (3 pontos)
- Paginação para 1000 repositórios
- Dados salvos em arquivo CSV
- Primeira versão do relatório com hipóteses informais

### Sprint 3 (9 pontos)
- Análise completa de dados com cálculo de medianas
- Visualização de dados (7 gráficos diferentes)
- Relatório final completo em Markdown

### Bonus (+1 ponto)
- **RQ07**: Análise por linguagem de programação
- Comparação entre linguagens populares vs outras

## Questões de Pesquisa Implementadas

| RQ | Questão | Métrica | Status |
|----|---------|---------|--------|
| **RQ01** | Sistemas populares são maduros/antigos? | Idade do repositório | Implementado |
| **RQ02** | Sistemas populares recebem muita contribuição externa? | Pull requests aceitas | Implementado |
| **RQ03** | Sistemas populares lançam releases com frequência? | Total de releases | Implementado |
| **RQ04** | Sistemas populares são atualizados com frequência? | Tempo até última atualização | Implementado |
| **RQ05** | Sistemas populares são escritos nas linguagens mais populares? | Linguagem primária | Implementado |
| **RQ06** | Sistemas populares possuem alto percentual de issues fechadas? | Razão issues fechadas/total | Implementado |
| **RQ07** | Análise por linguagem (BONUS) | Métricas RQ02, RQ03, RQ04 por linguagem | Implementado |

## Visualizações Geradas

1. **RQ01** - Distribuição da idade dos repositórios (histograma + box plot)
2. **RQ02** - Pull requests aceitas (distribuição + top 20)
3. **RQ03** - Distribuição de releases + correlação com popularidade
4. **RQ04** - Frequência de atualizações + categorias temporais
5. **RQ05** - Linguagens (top 15 + pie chart + estatísticas)
6. **RQ06** - Taxa de fechamento de issues + correlações
7. **Matriz de correlação** entre todas as métricas

## Estrutura do Projeto

```
lab1/
├── main.py                          # Ponto de entrada (todas as sprints)
├── src/
│   ├── config.py                    # Configurações gerais
│   ├── collectors/                  # Coleta de dados
│   │   ├── graphql_collector.py     # Coletor GraphQL
│   │   └── rest_collector.py        # Coletor REST
│   └── modules/                     # Análise e relatórios
│       ├── data_analyzer.py         # Análise das RQs
│       ├── data_visualizer.py       # Geração de gráficos
│       └── report_generator.py      # Geração do relatório
├── output/                          # Resultados (criado automaticamente)
│   ├── data/                        # Arquivos CSV
│   ├── plots/                       # Gráficos PNG
│   └── relatorio_analise_*.md       # Relatório final
├── requirements.txt                 # Dependências
├── .env                            # Token do GitHub
└── README.md                       # Este arquivo
```

## Como Configurar

### 1. **Clone e prepare o ambiente:**
```bash
git clone <url-do-repositorio>
cd labExp
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. **Configure o token do GitHub:**

1. Acesse: https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Permissões: `public_repo`, `read:org`, `read:user`
4. Crie arquivo `.env`:

```bash
# .env
GITHUB_TOKEN=seu_token_aqui
```

## Como Executar (TODAS as Sprints)

```bash
python main.py
```

### O sistema executará automaticamente:

1. **Etapa 1**: Coleta de dados (1000 repositórios)
2. **Etapa 2**: Análise de todas as RQs (incluindo RQ07)
3. **Etapa 3**: Geração de 7 visualizações
4. **Etapa 4**: Relatório final completo

### Resultados gerados:

- `output/data/top_1000_repos.csv` - Dados coletados
- `output/plots/` - 7 gráficos PNG
- `output/relatorio_analise_*.md` - Relatório final completo

## Configurações Disponíveis

No arquivo `src/config.py`:

```python
API_METHOD = 'GRAPHQL'           # ou 'REST'
TOTAL_REPOS_TO_FETCH = 1000      # Quantidade de repositórios
REPOS_PER_PAGE = 10              # Repositórios por requisição
```

## Pontuação Completa

- Sprint 1: 3 pontos
- Sprint 2: 3 pontos  
- Sprint 3: 9 pontos
- Bonus (RQ07): +1 ponto

**Total: 16/15 pontos possíveis**

## Funcionalidades Avançadas

- **Análise robusta**: Uso de medianas (resistente a outliers)
- **Visualizações profissionais**: 7 gráficos com Matplotlib/Seaborn
- **Relatório automático**: Markdown com hipóteses, metodologia, resultados e discussão
- **Análise de correlação**: Matriz de correlação entre métricas
- **Flexibilidade**: Suporte GraphQL e REST API
- **Tratamento de erros**: Retry automático e mensagens claras

---

**Projeto completo e pronto para avaliação**

4.  **Configure o Token da API:**
    - Crie um arquivo chamado `.env` na raiz do projeto.
    - Adicione seu Token de Acesso Pessoal do GitHub a ele:
      ```
      GITHUB_TOKEN="ghp_seu_token_aqui"
      ```

## Como Executar

Após a configuração, basta executar o script principal:

```bash
python main.py