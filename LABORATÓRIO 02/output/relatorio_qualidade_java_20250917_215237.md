# Relatório de Análise de Qualidade - Repositórios Java

Data de Análise: 17/09/2025 21:52:37

## Resumo Executivo

Análise de 100 repositórios Java para responder questões sobre qualidade de código.

## Dados Analisados

- Total de repositórios: 100
- Média de stars: 35879.4
- Média de forks: 9794.2
- Idade média: 9.3 anos
- Range de popularidade: 18785 - 151774 stars

## Questões de Pesquisa

### RQ01: Relação entre popularidade e qualidade

**Hipótese:** Repositórios mais populares têm melhor qualidade

**Conclusão:** Análise de correlação entre popularidade e métricas de qualidade

**Correlações:**
- Stars vs CBO: 0.096
- Stars vs DIT: -0.249
- Stars vs LCOM: -0.055

### RQ02: Relação entre maturidade e qualidade

**Hipótese:** Repositórios mais maduros têm melhor qualidade

**Conclusão:** Análise da relação entre idade e qualidade

### RQ03: Relação entre atividade e qualidade

**Hipótese:** Repositórios mais ativos têm melhor qualidade

**Conclusão:** Análise da relação entre atividade e qualidade

### RQ04: Relação entre tamanho e qualidade

**Hipótese:** Existe relação entre tamanho do código e qualidade

**Conclusão:** Análise da relação entre tamanho e qualidade

## Visualizações

- output/plots/rq01_popularity_quality.png
- output/plots/rq02_maturity_quality.png
- output/plots/rq03_activity_quality.png
- output/plots/correlation_matrix.png

## Metodologia

1. Coleta via GitHub API
2. Métricas: CBO, DIT, LCOM, WMC, CC
3. Análise estatística de correlação
4. Visualizações gráficas

