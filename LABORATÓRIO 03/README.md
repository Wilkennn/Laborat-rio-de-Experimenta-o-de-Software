# LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub

## 🎯 Objetivos

Este laboratório implementa uma análise completa da atividade de code review em repositórios populares do GitHub, respondendo a 8 questões de pesquisa sobre fatores que influenciam no resultado final dos Pull Requests.

## 🚀 Status do Projeto - LAB03S03 COMPLETO ✅

**✅ LAB03S01** - Seleção de repositórios + Coleta de PRs  
**✅ LAB03S02** - Dataset completo + Hipóteses  
**✅ LAB03S03** - Análise estatística + Visualizações + Relatório final  

## 📋 Questões de Pesquisa

### Grupo A: Feedback Final das Revisões (MERGED vs CLOSED)
- **RQ01**: Tamanho dos PRs vs Feedback final
- **RQ02**: Tempo de análise vs Feedback final  
- **RQ03**: Descrição dos PRs vs Feedback final
- **RQ04**: Interações nos PRs vs Feedback final

### Grupo B: Número de Revisões
- **RQ05**: Tamanho dos PRs vs Número de revisões
- **RQ06**: Tempo de análise vs Número de revisões
- **RQ07**: Descrição dos PRs vs Número de revisões
- **RQ08**: Interações nos PRs vs Número de revisões

## 🛠️ Funcionalidades Implementadas

### 📊 Coleta de Dados
- ✅ Seleção automática dos 200 repositórios mais populares
- ✅ Filtragem por critérios de atividade (min 100 PRs)
- ✅ Coleta detalhada de PRs com critérios de qualidade
- ✅ Cálculo automático de todas as métricas definidas

### 🔬 Análise Estatística
- ✅ **Testes de hipótese**: Mann-Whitney U, Chi-quadrado
- ✅ **Análise de correlação**: Spearman e Pearson
- ✅ **Estatísticas descritivas**: Medianas, quartis, médias
- ✅ **Interpretação automática** dos resultados

### 📈 Visualização de Dados
- ✅ **Plots estáticos** (Matplotlib/Seaborn): Box plots, histogramas, scatter plots, heatmaps
- ✅ **Visualizações interativas** (Plotly): Dashboards 3D, gráficos exploratórios
- ✅ **Matriz de correlação** com interpretação visual
- ✅ **Plots específicos para cada RQ** (RQ01-RQ08)

### 📝 Geração de Relatório
- ✅ **Relatório final completo** em Markdown
- ✅ **Estrutura acadêmica**: Introdução, metodologia, resultados, discussão, conclusões
- ✅ **Hipóteses informais** e validação
- ✅ **Interpretação dos resultados** estatísticos
- ✅ **Exportação em JSON** dos resultados detalhados

## 🏗️ Arquitetura do Projeto

```
LABORATÓRIO 03/
├── 📄 README.md                    # Este arquivo
├── 🐍 main.py                     # Ponto de entrada principal  
├── 🧪 quick_test.py               # Teste rápido dos módulos
├── 📋 requirements.txt            # Dependências Python
├── ⚙️  .env                       # Configuração do token GitHub
├── 📁 src/
│   ├── ⚙️  config/
│   │   └── config.py              # Configurações gerais
│   ├── 🔍 collectors/             # Coleta de dados
│   │   ├── repo_selector.py       # Seleção de repositórios
│   │   └── github_collector.py    # Coleta de PRs via API
│   ├── 📊 modules/                # Análise e processamento
│   │   ├── metrics_calculator.py  # Cálculo de métricas
│   │   ├── statistical_analyzer.py # Análise estatística (RQ01-RQ08)
│   │   ├── data_visualizer.py     # Geração de visualizações
│   │   └── report_generator.py    # Relatório final
│   └── 🔄 pipelines/
│       └── AnalysisPipeline.py    # Orquestração do fluxo
├── 📊 output/                     # Arquivos de saída
│   ├── 📁 data/                   # Datasets CSV/JSON
│   └── 📈 plots/                  # Gráficos e visualizações
└── 🧪 test/                      # Testes unitários
```

## 🚀 Como Executar

### 1. Configuração Inicial

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar token do GitHub
# Edite o arquivo .env e substitua 'seu_token_aqui' pelo seu token pessoal
```

**Como obter token do GitHub:**
1. Acesse: https://github.com/settings/tokens
2. Generate new token (classic)
3. Selecione escopo: `public_repo`
4. Copie o token gerado para o arquivo `.env`

### 2. Teste Rápido

```bash
# Teste se todos os módulos estão funcionando
python quick_test.py
```

### 3. Execução Completa

```bash
# Execução completa (todas as etapas)
python main.py

# Execução rápida para teste (5 repositórios apenas)
python main.py --quick-test

# Apenas análise estatística (usa dados já coletados)
python main.py --only-analysis
```

### 4. Opções Avançadas

```bash
# Controle granular das etapas
python main.py --max-repos 10 --skip-selection    # Usar dados existentes
python main.py --skip-collection --skip-metrics   # Apenas análise
python main.py --repos 50 --min-prs 50           # Parâmetros customizados
```

## 📊 Arquivos de Saída

Após a execução, os seguintes arquivos são gerados:

### 📁 output/data/
- `selected_repositories.csv` - Lista de repositórios selecionados
- `pull_requests_data.csv` - Dados brutos dos PRs coletados
- `prs_with_metrics.csv` - Dataset completo com métricas calculadas
- `analysis_results_YYYYMMDD_HHMMSS.json` - Resultados da análise estatística

### 📈 output/plots/  
- `00_summary_analysis.png` - Resumo visual da análise
- `01_status_distribution.png` - Distribuição MERGED vs CLOSED
- `02_metrics_distributions.png` - Histogramas das métricas principais
- `03_rq01_size_vs_feedback.png` - RQ01: Tamanho vs Feedback
- `04_rq02_time_vs_feedback.png` - RQ02: Tempo vs Feedback  
- `05_rq03_description_vs_feedback.png` - RQ03: Descrição vs Feedback
- `06_rq04_interactions_vs_feedback.png` - RQ04: Interações vs Feedback
- `07_rq05_size_vs_reviews.png` - RQ05: Tamanho vs Revisões
- `08_rq06_time_vs_reviews.png` - RQ06: Tempo vs Revisões
- `09_correlation_matrix_spearman.png` - Matriz de correlação
- `10_interactive_3d_scatter.html` - Visualização 3D interativa
- `11_interactive_dashboard.html` - Dashboard interativo

### 📝 output/
- `relatorio_final_lab03_YYYYMMDD_HHMMSS.md` - **RELATÓRIO FINAL COMPLETO**

## 🧪 Metodologia Científica

### Métodos Estatísticos
- **Mann-Whitney U**: Comparação não-paramétrica entre grupos (robusto a outliers)
- **Chi-quadrado**: Análise de associação entre variáveis categóricas  
- **Correlação de Spearman**: Correlação não-paramétrica (método principal)
- **Correlação de Pearson**: Correlação paramétrica (comparação)

### Tratamento de Dados
- **Outliers**: Remoção usando método IQR (Q3 + 1.5*IQR)
- **Valores ausentes**: Exclusão listwise nas análises específicas
- **Normalização**: Não aplicada (métodos não-paramétricos)

### Critérios de Significância
- **Nível α**: 0.05 (5%)
- **Interpretação de correlações**: |ρ| < 0.3 (fraca), 0.3-0.7 (moderada), > 0.7 (forte)

## 📚 Dependências

```
requests>=2.31.0      # API do GitHub
pandas>=2.0.0         # Manipulação de dados
numpy>=1.24.0         # Computação numérica
matplotlib>=3.7.0     # Gráficos estáticos
seaborn>=0.12.0       # Visualização estatística
plotly>=5.15.0        # Gráficos interativos
scipy>=1.10.0         # Análises estatísticas
statsmodels>=0.14.0   # Modelos estatísticos
python-dotenv>=1.0.0  # Gerenciamento de variáveis
PyGithub>=1.59.0      # SDK do GitHub
tqdm>=4.65.0          # Barras de progresso
```

## 🎉 Resultados Esperados

O LAB03S03 produz:

1. **📊 Dataset científico** de PRs de repositórios populares
2. **🔬 Análise estatística rigorosa** das 8 questões de pesquisa  
3. **📈 Visualizações profissionais** para cada análise
4. **📝 Relatório acadêmico completo** com interpretação dos resultados
5. **🧪 Validação de hipóteses** sobre o processo de code review

## 🏆 Status Final

**✅ LAB03S03 IMPLEMENTADO E FUNCIONAL**

Todos os requisitos das 3 sprints foram implementados:
- ✅ Coleta automatizada de dados (LAB03S01)
- ✅ Dataset completo e métricas (LAB03S02)  
- ✅ Análise estatística completa (LAB03S03)
- ✅ Visualizações profissionais (LAB03S03)
- ✅ Relatório final acadêmico (LAB03S03)

**🎯 Pronto para entrega e apresentação!**
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