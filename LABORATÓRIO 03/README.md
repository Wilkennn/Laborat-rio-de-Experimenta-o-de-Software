# LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub

## Introdução

Este laboratório tem como objetivo analisar a atividade de code review desenvolvida em repositórios populares do GitHub, identificando variáveis que influenciam no merge de um Pull Request (PR), sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.

## Metodologia

### 1. Criação do Dataset

O dataset será composto por PRs submetidos a repositórios:
- **Populares**: 200 repositórios mais populares do GitHub
- **Com atividade significativa**: pelo menos 100 PRs (MERGED + CLOSED)

### 2. Critérios de Seleção dos PRs

- Status: MERGED ou CLOSED
- Com pelo menos uma revisão
- Tempo de revisão > 1 hora (para remover revisões automáticas)

### 3. Questões de Pesquisa

#### A. Feedback Final das Revisões (Status do PR):
- **RQ01**: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
- **RQ02**: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
- **RQ03**: Qual a relação entre a descrição dos PRs e o feedback final das revisões?
- **RQ04**: Qual a relação entre as interações nos PRs e o feedback final das revisões?

#### B. Número de Revisões:
- **RQ05**: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
- **RQ06**: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
- **RQ07**: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
- **RQ08**: Qual a relação entre as interações nos PRs e o número de revisões realizadas?

### 4. Métricas Definidas

- **Tamanho**: número de arquivos, total de linhas adicionadas e removidas
- **Tempo de Análise**: intervalo entre a criação do PR e a última atividade
- **Descrição**: número de caracteres do corpo de descrição do PR
- **Interações**: número de participantes, número de comentários

## Estrutura do Projeto

```
LABORATÓRIO 03/
├── README.md
├── main.py
├── requirements.txt
├── setup.py
├── src/
│   ├── config/
│   │   └── config.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── github_collector.py
│   │   └── repo_selector.py
│   └── modules/
│       ├── __init__.py
│       ├── data_processor.py
│       ├── metrics_calculator.py
│       └── analyzer.py
├── output/
│   └── data/
├── test/
│   └── __init__.py
└── docs/
```

## Processo de Desenvolvimento

- **Lab03S01**: Lista de repositórios selecionados + Script de coleta dos PRs e métricas (5 pontos)
- **Lab03S02**: Dataset completo + Primeira versão do relatório com hipóteses (5 pontos)
- **Lab03S03**: Análise, visualização de dados + Relatório final (10 pontos)

## Como Executar

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar token do GitHub em `src/config/config.py`

3. Executar coleta de dados:
```bash
python main.py
```

## Requisitos

- Python 3.8+
- Token de acesso do GitHub API
- Bibliotecas especificadas em requirements.txt
```
LABORATÓRIO 03
├─ docs
│  └─ github_token_setup.md
├─ main.py
├─ output
│  ├─ data
│  └─ plots
├─ quick_test.py
├─ README.md
├─ requirements.txt
├─ setup.py
├─ src
│  ├─ collectors
│  │  ├─ github_collector.py
│  │  ├─ repo_selector.py
│  │  └─ __init__.py
│  ├─ config
│  │  └─ config.py
│  └─ modules
│     ├─ metrics_calculator.py
│     └─ __init__.py
└─ test
   ├─ test_basic.py
   └─ __init__.py

```