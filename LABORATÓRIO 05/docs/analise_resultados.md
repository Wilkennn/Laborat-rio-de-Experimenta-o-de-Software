# Análise de Resultados - Experimento GraphQL vs REST

## 📊 Resumo Executivo

Este documento apresenta a análise dos resultados obtidos no experimento comparativo entre APIs GraphQL e REST.

## 🎯 Hipóteses Testadas

### H1: GraphQL é mais rápido que REST
**Justificativa**: GraphQL permite buscar apenas os dados necessários em uma única requisição.

### H2: GraphQL transfere menos dados que REST
**Justificativa**: REST retorna objetos completos, enquanto GraphQL retorna apenas campos solicitados.

### H3: GraphQL reduz o problema N+1
**Justificativa**: GraphQL permite buscar dados relacionados em uma única query.

## 📈 Metodologia

- **Execuções**: 30 rodadas (5 descartadas de aquecimento)
- **Cenários**: 3 casos de uso reais
- **Métricas**: Tempo (ms), Tamanho (bytes), Requisições HTTP
- **Análise**: Teste T de Student (p-value < 0.05 = significativo)

## 🔬 Resultados por Cenário

### Cenário 1: Consulta Escalar
**Descrição**: Buscar informações básicas de uma organização.

**Expectativa**:
- Diferenças mínimas, ambos fazem 1 requisição
- GraphQL pode ser ligeiramente mais leve (menos campos)

**Análise**:
- Se p-value < 0.05: Diferença significativa
- Se speedup > 1.2x: GraphQL substancialmente mais rápido

### Cenário 2: Listagem Simples
**Descrição**: Listar 50 repositórios com nome e estrelas.

**Expectativa**:
- REST retorna MUITO mais dados (objetos completos)
- GraphQL mais leve (apenas name + stargazerCount)
- Tempos similares (mesma complexidade de query)

**Análise**:
- Redução de dados esperada: 10x-100x
- Tempo similar ou GraphQL ligeiramente mais rápido

### Cenário 3: Dashboard Complexa (N+1)
**Descrição**: 5 repos + suas issues + linguagens.

**Expectativa**:
- REST: 1 + 5×2 = 11 requisições (problema N+1!)
- GraphQL: 1 requisição apenas
- **Maior diferença esperada aqui**

**Análise**:
- Speedup esperado: 3x-10x para GraphQL
- Redução de dados: significativa
- P-value: deve ser < 0.05 (diferença clara)

## 📊 Interpretação dos Gráficos

### Gráfico de Tempo (Barras com IC 95%)
- **Barras de erro NÃO se sobrepõem**: Diferença estatisticamente significativa
- **Barras se sobrepõem**: Diferença não conclusiva

### Boxplot de Estabilidade
- **Caixa menor**: Mais estável (menos variação)
- **Outliers**: Medir impacto de cache/rede

### Matriz de Correlação
- **tempo_ms × n_requests**: Esperado positivo (mais requests = mais tempo)
- **tamanho_bytes × tempo_ms**: Esperado positivo (mais dados = mais tempo)

## 🎓 Conclusões Esperadas

### Se GraphQL vencer:
1. **Tempo**: Principalmente no Cenário 3 (N+1)
2. **Dados**: Em todos os cenários (overfetching)
3. **Escalabilidade**: Melhor para aplicações complexas

### Se REST vencer:
1. Possíveis causas:
   - Overhead de parsing GraphQL
   - Cache do GitHub para REST
   - Simplicidade da query

### Cenários Neutros:
- **Consultas simples**: REST pode ser suficiente
- **Sem relações**: Diferença mínima

## 📝 Como Preencher no Relatório

### Seção "Resultados"
```markdown
## Resultados

### Cenário 1 - Consulta Escalar
- Tempo médio REST: XXX ms (±YY)
- Tempo médio GraphQL: XXX ms (±YY)
- P-value: 0.XXX (significativo/não significativo)
- Conclusão: [Descrever]

[Repetir para outros cenários]
```

### Seção "Discussão"
- Interpretar os p-values
- Explicar por que GraphQL foi melhor/pior
- Relacionar com teoria (problema N+1, overfetching)
- Discutir outliers e variações

### Seção "Limitações"
- Testar apenas 1 organização (facebook)
- Dependência da rede/cache do GitHub
- Número limitado de execuções
- Não testar queries muito complexas

## 🔍 Checklist de Análise

- [ ] Verificar se todas as 25 medições válidas foram coletadas
- [ ] Confirmar que p-values foram calculados
- [ ] Identificar cenário com maior diferença
- [ ] Verificar se IC 95% se sobrepõem
- [ ] Analisar outliers no boxplot
- [ ] Calcular speedup e redução de dados
- [ ] Comparar com hipóteses iniciais
- [ ] Documentar conclusões

## 📚 Conceitos Estatísticos

### P-value
- **< 0.05**: Diferença estatisticamente significativa (95% de confiança)
- **≥ 0.05**: Diferença pode ser aleatória

### Intervalo de Confiança (IC 95%)
- Faixa onde a média real provavelmente está
- Se ICs não se sobrepõem → diferença real

### Speedup
```
Speedup = Tempo_REST / Tempo_GraphQL
> 1: GraphQL mais rápido
< 1: REST mais rápido
```

## 🚀 Próximos Passos

1. Executar o experimento: `python experiment/main.py`
2. Abrir dashboard: `streamlit run experiment/dashboard.py`
3. Analisar gráficos e tabelas
4. Documentar resultados no relatório
5. Discutir implicações práticas

---

**Dica**: Use o dashboard interativo para explorar os dados antes de escrever o relatório final!
