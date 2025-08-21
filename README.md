# 🔬 Laboratório de Experimentação de Software

**Análise de Características de Repositórios Populares no GitHub**

Este repositório contém a implementação completa dos laboratórios de experimentação de software, focando na análise de repositórios populares do GitHub através de métricas quantitativas e visualizações.

## 🎯 Objetivo

Estudar as principais características de sistemas populares open-source, analisando como são desenvolvidos, frequência de contribuições externas, lançamento de releases e outras métricas importantes.

## 📊 Questões de Pesquisa

| RQ | Questão | Métrica |
|----|---------|---------|
| **RQ01** | Sistemas populares são maduros/antigos? | Idade do repositório |
| **RQ02** | Sistemas populares recebem muita contribuição externa? | Pull requests aceitas |
| **RQ03** | Sistemas populares lançam releases com frequência? | Total de releases |
| **RQ04** | Sistemas populares são atualizados com frequência? | Tempo até última atualização |
| **RQ05** | Sistemas populares são escritos nas linguagens mais populares? | Linguagem primária |
| **RQ06** | Sistemas populares possuem alto percentual de issues fechadas? | Razão issues fechadas/total |
| **RQ07** | **BÔNUS**: Análise por linguagem de programação | Métricas RQ02-04 por linguagem |

## 🏗️ Estrutura do Projeto

```
Laboratorio-de-Experimentacao-de-Software/
├── README.md                               # Este arquivo
└── lab1/                                   # Laboratório 1 - Análise de Repositórios
    ├── main.py                            # Ponto de entrada principal
    ├── requirements.txt                   # Dependências Python
    ├── .env.example                       # Exemplo de configuração
    ├── README.md                         # Documentação específica do Lab1
    ├── src/                              # Código fonte
    │   ├── config.py                     # Configurações gerais
    │   ├── collectors/                   # Módulos de coleta de dados
    │   │   ├── __init__.py
    │   │   ├── graphql_collector.py      # Coletor via GraphQL API
    │   │   └── rest_collector.py         # Coletor via REST API
    │   └── modules/                      # Módulos de análise
    │       ├── data_analyzer.py          # Análise das questões de pesquisa
    │       ├── data_visualizer.py        # Geração de gráficos
    │       └── report_generator.py       # Geração do relatório final
    └── output/                           # Resultados (gerado automaticamente)
        ├── data/
        │   └── top_1000_repos.csv       # Dados coletados
        ├── plots/                        # Visualizações
        │   ├── rq01_age_distribution.png
        │   ├── rq02_pull_requests.png
        │   ├── rq03_releases.png
        │   ├── rq04_update_frequency.png
        │   ├── rq05_languages.png
        │   ├── rq06_issues_closure.png
        │   └── correlation_matrix.png
        └── relatorio_analise_*.md        # Relatório final
```

## 🚀 Execução Rápida

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Wilkennn/Laboratorio-de-Experimentacao-de-Software.git
   cd Laboratorio-de-Experimentacao-de-Software/lab1
   ```

2. **Configure o ambiente:**
   ```bash
   # Criar ambiente virtual
   python -m venv venv
   
   # Ativar ambiente virtual
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Instalar dependências
   pip install -r requirements.txt
   ```

3. **Configure o token do GitHub:**
   ```bash
   # Copie o arquivo de exemplo
   copy .env.example .env
   
   # Edite o arquivo .env e adicione seu token:
   # GITHUB_TOKEN=seu_token_aqui
   ```

4. **Execute a análise completa:**
   ```bash
   python main.py
   ```

## 📈 Resultados

O sistema gera automaticamente:

- **📊 Dados**: Arquivo CSV com dados de 1.000 repositórios
- **📈 Visualizações**: 7 gráficos profissionais em PNG
- **📄 Relatório**: Documento Markdown completo com:
  - Hipóteses informais
  - Metodologia utilizada
  - Resultados para cada RQ
  - Discussão e análise
  - Visualizações

## 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **APIs do GitHub**: GraphQL e REST
- **Análise de Dados**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn
- **Relatórios**: Markdown automático

## 📋 Processo de Desenvolvimento

### ✅ Lab01S01 (3 pontos)
- Consulta GraphQL para 100 repositórios
- Todas as métricas necessárias para as RQs
- Requisição automática com paginação

### ✅ Lab01S02 (3 pontos)  
- Paginação para 1.000 repositórios
- Dados salvos em arquivo CSV
- Primeira versão do relatório com hipóteses informais

### ✅ Lab01S03 (9 pontos)
- Análise completa de dados com medianas
- Visualização de dados (7 gráficos)
- Relatório final completo

### ✅ Bônus (+1 ponto)
- **RQ07**: Análise detalhada por linguagem de programação

## 👥 Contribuidores

- **Desenvolvedor Principal**: [Wilkennn](https://github.com/Wilkennn)

## 📜 Licença

Este projeto é desenvolvido para fins acadêmicos como parte do curso de Laboratório de Experimentação de Software.

---

**🎉 Projeto completo e pronto para avaliação - 16/15 pontos possíveis!**
