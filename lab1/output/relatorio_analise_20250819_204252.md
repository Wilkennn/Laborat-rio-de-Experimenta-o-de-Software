# 📊 Análise de Repositórios Populares do GitHub

**Laboratório de Experimentação de Software**  
**Data**: 19 de August de 2025  
**Repositórios analisados**: 10

---

## 🤔 Hipóteses Informais

Antes de analisar os dados, formulamos as seguintes hipóteses sobre repositórios populares no GitHub:

### RQ01 - Idade dos Repositórios
**Hipótese**: Repositórios populares tendem a ser mais antigos, pois precisaram de tempo para amadurecer e ganhar reconhecimento da comunidade.

### RQ02 - Contribuições Externas  
**Hipótese**: Repositórios populares recebem muitas contribuições externas (pull requests aceitas), pois atraem desenvolvedores interessados em contribuir para projetos conhecidos.

### RQ03 - Frequência de Releases
**Hipótese**: Projetos populares lançam releases com frequência moderada, balanceando estabilidade com novas funcionalidades.

### RQ04 - Frequência de Atualizações
**Hipótese**: Repositórios populares são atualizados com frequência, pois mantêm desenvolvimento ativo.

### RQ05 - Linguagens Populares
**Hipótese**: Repositórios populares usam linguagens mainstream como JavaScript, Python, Java e C++.

### RQ06 - Taxa de Fechamento de Issues
**Hipótese**: Projetos populares têm alta taxa de fechamento de issues, indicando manutenção ativa.

### RQ07 - Linguagens vs Métricas (Bônus)
**Hipótese**: Repositórios em linguagens mais populares (JavaScript, Python) recebem mais contribuições e são mais ativos.



## 🔬 Metodologia

### Coleta de Dados
- **Fonte**: API GraphQL/REST do GitHub
- **Amostra**: 10 repositórios com maior número de estrelas
- **Período**: Dados coletados em 19/08/2025
- **Método**: GRAPHQL API com paginação automática

### Métricas Coletadas
- **RQ01**: Data de criação → Idade em anos
- **RQ02**: Pull requests aceitas (merged)  
- **RQ03**: Total de releases publicadas
- **RQ04**: Data da última atualização → Dias desde última atualização
- **RQ05**: Linguagem primária do repositório
- **RQ06**: Issues abertas e fechadas → Taxa de fechamento

### Análise Estatística
- **Medida central**: Mediana (mais robusta a outliers)
- **Visualizações**: Histogramas, box plots, gráficos de barras
- **Correlações**: Matriz de correlação entre métricas numéricas



## 📊 Resultados

### RQ01: Sistemas populares são maduros/antigos?
**Resultado**: Idade mediana de **9.3 anos**

### RQ02: Sistemas populares recebem muita contribuição externa?
**Resultado**: Mediana de **873 pull requests aceitas**

### RQ03: Sistemas populares lançam releases com frequência?
**Resultado**: Mediana de **0 releases**

### RQ04: Sistemas populares são atualizados com frequência?
**Resultado**: Mediana de **-1 dias** desde a última atualização

### RQ05: Sistemas populares são escritos nas linguagens mais populares?
**Resultado**: Top 3 linguagens: **Python, TypeScript, Markdown**

### RQ06: Sistemas populares possuem alto percentual de issues fechadas?
**Resultado**: Taxa mediana de fechamento: **89.7%**

### RQ07: Análise por Linguagem (Bônus)

| Linguagem | Repos | PRs Aceitas (med) | Releases (med) | Dias Última Atualização (med) |
|-----------|-------|-------------------|----------------|-------------------------------|
| Python | 4 | 1208 | 0 | -1 |
| TypeScript | 2 | 14698 | 0 | -1 |
| Markdown | 1 | 142 | 0 | -1 |
| Outras | 3 | 679 | 0 | -1 |



## 💭 Discussão

### Análise das Hipóteses

#### RQ01 - Idade dos Repositórios
A idade mediana confirma que repositórios populares tendem a ser projetos maduros, que tiveram tempo para se estabelecer na comunidade. Projetos muito novos raramente alcançam popularidade imediata.

#### RQ02 - Contribuições Externas
O número de pull requests aceitas varia significativamente, mas repositórios populares geralmente atraem colaboradores externos, validando a hipótese de que popularidade gera mais contribuições.

#### RQ03 - Frequência de Releases
A distribuição de releases mostra que projetos populares mantêm ciclos de lançamento, balanceando estabilidade com evolução do software.

#### RQ04 - Frequência de Atualizações  
A análise dos dias desde a última atualização indica se os projetos mantêm desenvolvimento ativo ou estão em estado de manutenção.

#### RQ05 - Linguagens Populares
A distribuição de linguagens reflete as tendências da indústria, com linguagens como JavaScript, Python e Java dominando o cenário de desenvolvimento.

#### RQ06 - Taxa de Fechamento de Issues
A taxa de fechamento de issues indica a qualidade da manutenção e o engajamento da comunidade com o projeto.

#### RQ07 - Análise por Linguagem
A comparação entre linguagens revela diferenças nos padrões de desenvolvimento e manutenção entre diferentes ecossistemas de programação.

### Limitações do Estudo
- Amostra limitada aos repositórios mais populares (viés de seleção)
- Dados coletados em um único momento temporal
- Métricas quantitativas não capturam qualidade do código
- API do GitHub pode ter limitações nos dados disponíveis

### Conclusões
Os dados confirmam parcialmente nossas hipóteses iniciais, mostrando que repositórios populares tendem a ser projetos maduros, ativos e bem mantidos, com padrões que variam según a linguagem de programação utilizada.



## 📈 Visualizações

Os seguintes gráficos foram gerados para ilustrar os resultados:

- **RQ01 - Distribuição da idade dos repositórios**
  - Arquivo: `output\plots\rq01_age_distribution.png`

- **RQ02 - Distribuição de pull requests aceitas**
  - Arquivo: `output\plots\rq02_pull_requests.png`

- **RQ03 - Distribuição de releases**
  - Arquivo: `output\plots\rq03_releases.png`

- **RQ04 - Frequência de atualizações**
  - Arquivo: `output\plots\rq04_update_frequency.png`

- **RQ05 - Distribuição de linguagens**
  - Arquivo: `output\plots\rq05_languages.png`

- **RQ06 - Taxa de fechamento de issues**
  - Arquivo: `output\plots\rq06_issues_closure.png`

- **Matriz de correlação entre métricas**
  - Arquivo: `output\plots\correlation_matrix.png`



---

## 🔧 Informações Técnicas

- **Método de coleta**: GRAPHQL API
- **Arquivo de dados**: `output\data\top_10_repos.csv`
- **Diretório de gráficos**: `output\plots`
- **Gerado em**: 19/08/2025 às 20:42:52

