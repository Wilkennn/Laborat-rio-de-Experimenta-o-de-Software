# Relatório de Análise de Qualidade - Repositórios Java

**Data de Análise:** 17/09/2025 21:48:31

## Resumo Executivo

Este relatório apresenta a análise de **1000 repositórios Java** visando responder às questões de pesquisa sobre qualidade de código.

## Dados Analisados

- **Total de repositórios:** 1000
- **Média de stars:** 34563.9
- **Média de forks:** 8491.1
- **Idade média:** 8.0 anos
- **Range de popularidade:** 127 - 69971 stars

## Questões de Pesquisa

### RQ01: Relação entre popularidade (stars) e qualidade de código

**Hipótese:** Repositórios mais populares têm melhor qualidade de código

**Conclusão:** Análise de correlação entre popularidade e métricas de qualidade

**Correlações encontradas:**
- Stars vs CBO: -0.023
- Stars vs DIT: 0.045
- Stars vs LCOM: -0.007

### RQ02: Relação entre maturidade (idade) e qualidade de código

**Hipótese:** Repositórios mais maduros têm melhor qualidade de código

**Conclusão:** Análise da relação entre idade do repositório e métricas de qualidade

### RQ03: Relação entre atividade (forks) e qualidade de código

**Hipótese:** Repositórios mais ativos têm melhor qualidade de código

**Conclusão:** Análise da relação entre atividade e métricas de qualidade

### RQ04: Relação entre tamanho (LOC) e qualidade de código

**Hipótese:** Existe uma relação entre tamanho do código e qualidade

**Conclusão:** Análise da relação entre tamanho do código e métricas de qualidade

## Visualizações Geradas

- `output/plots/rq01_popularity_quality.png` - Popularidade vs Qualidade
- `output/plots/rq02_maturity_quality.png` - Maturidade vs Qualidade
- `output/plots/rq03_activity_quality.png` - Atividade vs Qualidade
- `output/plots/correlation_matrix.png` - Matriz de Correlação

## Metodologia

1. **Coleta de Dados:** Via GitHub API
2. **Métricas de Qualidade:** CBO, DIT, LCOM, WMC, CC
3. **Análise Estatística:** Correlação de Pearson
4. **Visualização:** Gráficos de dispersão e matriz de correlação

## Limitações

---
*Relatório gerado automaticamente pelo Lab 02 - Experimentação de Software*
