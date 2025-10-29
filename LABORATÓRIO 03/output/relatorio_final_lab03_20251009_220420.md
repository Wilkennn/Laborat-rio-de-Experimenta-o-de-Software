# LABORATÓRIO 03 - Caracterizando a Atividade de Code Review no GitHub

**Data do Relatório:** 09/10/2025 às 22:04:20

**Autores:** [Inserir nomes dos integrantes do grupo]

---\n\n## 1. Introdução

### Contexto

A prática de code review tornou-se fundamental nos processos de desenvolvimento ágil, especialmente em projetos open source hospedados no GitHub. Este estudo analisa sistematicamente a atividade de code review através da análise de Pull Requests (PRs) em repositórios populares, com o objetivo de identificar variáveis que influenciam no resultado final das revisões.

### Hipóteses Informais

Baseando-se na literatura e experiência prática em desenvolvimento de software, formulamos as seguintes hipóteses informais:

#### **Hipóteses sobre Feedback Final (RQ01-RQ04):**

- **H1 (Tamanho):** PRs menores têm maior probabilidade de serem aprovados (MERGED), pois são mais fáceis de revisar e têm menor risco de introduzir bugs.

- **H2 (Tempo):** PRs que são analisados mais rapidamente têm maior probabilidade de serem aprovados, indicando consenso sobre a mudança.

- **H3 (Descrição):** PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados, pois facilitam o entendimento do revisor.

- **H4 (Interações):** PRs com mais interações (comentários, participantes) podem ter menor probabilidade de aprovação, indicando controvérsias ou problemas na implementação.

#### **Hipóteses sobre Número de Revisões (RQ05-RQ08):**

- **H5 (Tamanho):** PRs maiores requerem mais revisões devido à complexidade.

- **H6 (Tempo):** Maior tempo de análise está correlacionado com maior número de revisões.

- **H7 (Descrição):** PRs com melhor descrição requerem menos revisões devido à clareza.

- **H8 (Interações):** Existe correlação positiva forte entre número de interações e número de revisões.\n\n## 2. Metodologia

### 2.1 Seleção dos Repositórios

- **Critério de Popularidade:** 200 repositórios mais populares do GitHub (ordenados por estrelas)
- **Critério de Atividade:** Repositórios com pelo menos 100 PRs (MERGED + CLOSED)
- **Fonte:** GitHub API v3

### 2.2 Critérios de Seleção dos Pull Requests

Para garantir que analisamos PRs que passaram por processo real de code review:

- **Status:** Apenas PRs com status MERGED ou CLOSED
- **Revisões:** PRs com pelo menos uma revisão registrada
- **Tempo Mínimo:** Tempo de análise superior a 1 hora (elimina aprovações automáticas)

### 2.3 Métricas Coletadas

#### **Tamanho dos PRs:**
- Número de arquivos modificados
- Total de linhas adicionadas
- Total de linhas removidas  
- Total de mudanças (adições + remoções)

#### **Tempo de Análise:**
- Intervalo entre criação e fechamento/merge do PR
- Medido em horas e dias

#### **Descrição:**
- Número de caracteres na descrição
- Presença ou ausência de descrição

#### **Interações:**
- Número de participantes únicos
- Número de comentários gerais
- Número de comentários de revisão
- Total de comentários

### 2.4 Métodos Estatísticos

#### **Testes de Hipótese:**
- **Mann-Whitney U:** Para comparar distribuições entre grupos (MERGED vs CLOSED)
- **Chi-quadrado:** Para variáveis categóricas
- **Justificativa:** Dados não seguem distribuição normal, métodos não-paramétricos são mais robustos

#### **Análise de Correlação:**
- **Spearman:** Correlação não-paramétrica (método principal)
- **Pearson:** Correlação paramétrica (comparação)
- **Justificativa:** Correlação de Spearman é mais robusta para dados com outliers e não-normais

#### **Nível de Significância:**
- α = 0.05 (5%)\n\n## 3. Caracterização do Dataset

### 3.1 Composição Geral

- **Total de Pull Requests:** 351
- **PRs Aprovados (MERGED):** 229 (65.2%)
- **PRs Rejeitados (CLOSED):** 122 (34.8%)
- **Repositórios Analisados:** 5
- **Taxa de Aprovação Geral:** 65.2%

### 3.2 Estatísticas Descritivas das Métricas

#### **Métricas de Tamanho:**
- **Total Changes:**
  - Mediana: 3.0
  - Média: 320.5 (±1942.8)
  - Quartis: Q1=1.0, Q3=47.5
- **Files Changed:**
  - Mediana: 1.0
  - Média: 14.3 (±122.5)
  - Quartis: Q1=1.0, Q3=2.0
- **Additions:**
  - Mediana: 2.0
  - Média: 219.0 (±1039.5)
  - Quartis: Q1=1.0, Q3=28.5
- **Deletions:**
  - Mediana: 1.0
  - Média: 101.5 (±1116.4)
  - Quartis: Q1=0.0, Q3=4.0\n#### **Métricas de Tempo:**
- **Tempo de Análise (horas):**
  - Mediana: 102.3 horas
  - Média: 2415.5 horas (±6050.3)
- **Tempo de Análise (dias):**
  - Mediana: 4.3 dias
  - Média: 100.6 dias (±252.1)\n#### **Métricas de Interação:**
- **Participants Count:**
  - Mediana: 3.0
  - Média: 3.4 (±1.1)
- **Total Comments:**
  - Mediana: 1.0
  - Média: 3.0 (±4.6)
- **Reviews Count:**
  - Mediana: 2.0
  - Média: 3.1 (±3.4)\n\n## 4. Resultados - Grupo A: Feedback Final das Revisões (RQ01-RQ04)

Esta seção analisa as variáveis que influenciam no resultado final dos PRs (MERGED vs CLOSED).\n### 4.1 RQ01: Relação entre Tamanho dos PRs e Feedback Final
**Questão:** RQ01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

**Resultados dos Testes Estatísticos:**
- **Files Changed:** Significante (p=0.0000)
- **Additions:** Significante (p=0.0000)
- **Deletions:** Significante (p=0.0000)
- **Total Changes:** Significante (p=0.0000)\n**Estatísticas Descritivas:**
- **Files Changed:** Mediana MERGED = 1.0, Mediana CLOSED = 1.0
- **Additions:** Mediana MERGED = 5.0, Mediana CLOSED = 1.0
- **Deletions:** Mediana MERGED = 1.0, Mediana CLOSED = 0.0
- **Total Changes:** Mediana MERGED = 8.0, Mediana CLOSED = 1.0\n### 4.2 RQ02: Relação entre Tempo de Análise e Feedback Final
**Questão:** RQ02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

**Resultados:**
- **Analysis Time Hours:** Significante (p=0.0000)
- **Analysis Time Days:** Significante (p=0.0000)\n### 4.3 RQ03: Relação entre Descrição e Feedback Final
**Questão:** RQ03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?

**Resultados:**
- **Description Length** (Mann-Whitney U): Não significante (p=0.7845)
- **Has Description** (Chi-quadrado): Significante (p=0.0168)\n### 4.4 RQ04: Relação entre Interações e Feedback Final
**Questão:** RQ04: Qual a relação entre as interações nos PRs e o feedback final das revisões?

**Resultados:**
- **Participants Count:** Significante (p=0.0043)
- **Comments Count:** Não significante (p=0.0523)
- **Review Comments Count:** Não significante (p=1.0000)
- **Total Comments:** Não significante (p=0.0523)\n\n## 5. Resultados - Grupo B: Número de Revisões (RQ05-RQ08)

Esta seção analisa as variáveis que se correlacionam com o número de revisões realizadas nos PRs.\n### 5.1 RQ05: Relação entre Tamanho dos PRs e Número de Revisões
**Questão:** RQ05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

**Correlações encontradas:**
- **Files Changed:** Correlação positiva fraca (ρ=0.125, significante)
- **Total Changes:** Correlação positiva fraca (ρ=0.131, significante)
- **Additions:** Correlação positiva fraca (ρ=0.192, significante)
- **Deletions:** Correlação negativa muito fraca (ρ=-0.033, não significante)\n### 5.2 RQ06: Relação entre Tempo de Análise e Número de Revisões
**Questão:** RQ06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
- **Analysis Time Hours:** Correlação positiva fraca (ρ=0.183, significante)\n### 5.3 RQ07: Relação entre Descrição e Número de Revisões\n[Análise detalhada da correlação entre qualidade da descrição e número de revisões]\n### 5.4 RQ08: Relação entre Interações e Número de Revisões\n[Análise detalhada da correlação entre nível de interação e número de revisões]\n\n## 6. Análise Geral de Correlações

### 6.1 Matriz de Correlação

A matriz de correlação de Spearman entre todas as métricas numéricas revelou os seguintes padrões:

[Análise da matriz de correlação será inserida aqui baseada nos resultados]

### 6.2 Correlações Mais Fortes

[Lista das correlações mais significativas encontradas]

### 6.3 Interpretação das Correlações

[Interpretação do significado prático das correlações encontradas]\n\n## 7. Discussão

### 7.1 Validação das Hipóteses

#### **Hipóteses sobre Feedback Final:**

**H1 (Tamanho vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ01]

**H2 (Tempo vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ02]  

**H3 (Descrição vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ03]

**H4 (Interações vs Aprovação):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ04]

#### **Hipóteses sobre Número de Revisões:**

**H5 (Tamanho vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ05]

**H6 (Tempo vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ06]

**H7 (Descrição vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ07]

**H8 (Interações vs Revisões):** [Validada/Refutada] - [Explicação baseada nos resultados de RQ08]

### 7.2 Implicações Práticas

Os resultados desta análise têm implicações importantes para:

1. **Desenvolvedores:** [Recomendações baseadas nos achados]
2. **Revisores:** [Diretrizes para processo de revisão]  
3. **Gestores de Projeto:** [Insights para otimização do processo]

### 7.3 Limitações do Estudo

- **Representatividade:** Limitado aos repositórios mais populares do GitHub
- **Contexto Temporal:** Análise em ponto específico no tempo
- **Variáveis Não Controladas:** Fatores como complexidade do domínio, experiência dos desenvolvedores
- **Causalidade:** Correlações não implicam causalidade\n\n## 8. Conclusões

### 8.1 Principais Achados

Com base na análise de 351 Pull Requests de 5 repositórios populares do GitHub, concluímos:

1. **Taxa de Aprovação:** 65.2% dos PRs analisados foram aprovados (merged)

2. **Fatores de Aprovação:** [Listar principais fatores que influenciam na aprovação]

3. **Padrões de Revisão:** [Resumir padrões encontrados no número de revisões]

4. **Correlações Significativas:** [Destacar as correlações mais importantes encontradas]

### 8.2 Contribuições

Este estudo contribui para o entendimento da dinâmica de code review em projetos open source, fornecendo:

- Evidências empíricas sobre fatores que influenciam na aprovação de PRs
- Insights sobre o processo de revisão em repositórios populares  
- Base para futuras pesquisas sobre colaboração em desenvolvimento de software

### 8.3 Trabalhos Futuros

- Análise longitudinal para identificar tendências temporais
- Estudo de fatores qualitativos (complexidade do código, experiência dos desenvolvedores)
- Comparação entre diferentes tipos de repositórios (linguagens, domínios)
- Desenvolvimento de modelos preditivos para aprovação de PRs\n\n## 9. Visualizações

### 9.1 Gráficos Gerados

Os seguintes gráficos foram gerados para ilustrar os resultados da análise:
- **Status Distribution:** `01_status_distribution.png`
- **Metrics Distributions:** `02_metrics_distributions.png`
- **Rq01 Size Feedback:** `03_rq01_size_vs_feedback.png`
- **Rq02 Time Feedback:** `04_rq02_time_vs_feedback.png`
- **Rq03 Description Feedback:** `05_rq03_description_vs_feedback.png`
- **Rq04 Interactions Feedback:** `06_rq04_interactions_vs_feedback.png`
- **Rq05 Size Reviews:** `07_rq05_size_vs_reviews.png`
- **Rq06 Time Reviews:** `08_rq06_time_vs_reviews.png`
- **Correlation Matrix:** `09_correlation_matrix_spearman.png`
- **Interactive 3D:** `10_interactive_3d_scatter.html`
- **Interactive Dashboard:** `11_interactive_dashboard.html`

### 9.2 Como Interpretar

- **Box plots:** Mostram distribuição, mediana, quartis e outliers
- **Scatter plots:** Revelam correlações e padrões de relacionamento
- **Histogramas:** Mostram distribuição de frequências
- **Heatmaps:** Visualizam matriz de correlações

### 9.3 Visualizações Interativas

Gráficos interativos em HTML foram gerados para exploração mais detalhada dos dados.\n\n## 10. Apêndices

### 10.1 Metodologia Detalhada dos Testes Estatísticos

#### **Mann-Whitney U Test:**
- **Aplicação:** Comparação de distribuições entre grupos (MERGED vs CLOSED)
- **Pressupostos:** Amostras independentes, variável ordinal ou contínua
- **Interpretação:** p < 0.05 indica diferença estatisticamente significante

#### **Correlação de Spearman:**
- **Aplicação:** Medida de associação monotônica entre variáveis
- **Vantagem:** Robusta a outliers e não assume normalidade
- **Interpretação:** ρ entre -1 e 1, onde valores próximos aos extremos indicam correlação forte

### 10.2 Critérios de Qualidade dos Dados

- **Tratamento de Outliers:** Remoção de valores extremos (> Q3 + 1.5*IQR)
- **Valores Ausentes:** Exclusão de registros com dados incompletos nas análises específicas
- **Validação:** Verificação de consistência entre métricas relacionadas

### 10.3 Ferramentas Utilizadas

- **Coleta de Dados:** GitHub API v3
- **Processamento:** Python (pandas, numpy)
- **Análise Estatística:** SciPy
- **Visualização:** Matplotlib, Seaborn, Plotly
- **Relatórios:** Markdown com integração de plots