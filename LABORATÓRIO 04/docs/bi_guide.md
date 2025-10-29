# Guia de Conexão ao BI (Power BI / Tableau / Looker Studio)

Os CSVs normalizados ficam em `output/data/bi/`:
- `repositories.csv` (tabela fato principal)
- `owners.csv` (dimensão de donos)
- `topics.csv` (tópicos por repositório)
- `issues.csv` (amostras de issues)
- `pulls.csv` (amostras de PRs fechados)
- `releases.csv` (releases)
- `commits_weekly.csv` (série semanal de commits)
 - `languages.csv` (bytes por linguagem em cada repo)
 - `metrics_repo.csv` (métricas agregadas por repo para RQs)

## Power BI Desktop
1. Obtenha Dados > Texto/CSV > selecione todos arquivos de `output/data/bi/`
2. Para cada tabela, defina tipos de dados (Data/Hora, Número, Texto) quando necessário
3. Relacionamentos sugeridos:
   - repositories.full_name (chave) → topics.repo_full_name, issues.repo_full_name, pulls.repo_full_name, releases.repo_full_name, commits_weekly.repo_full_name
   - owners.login ↔ repositories.owner_login (1:N)
  - languages.repo_full_name ↔ repositories.full_name (1:N)
  - metrics_repo.repo_full_name ↔ repositories.full_name (1:1)
4. Medidas úteis (DAX):
   - Total de Stars = SUM(repositories[stargazers_count])
   - Média Stars = AVERAGE(repositories[stargazers_count])
   - PRs por Repo = COUNTROWS(RELATEDTABLE(pulls))
   - Issues por Repo = COUNTROWS(RELATEDTABLE(issues))
   - Commits (últimas 12 semanas) = CALCULATE(SUM(commits_weekly[total_commits]), LASTDATE(commits_weekly[week_start_iso]))

## Layout sugerido
- Página 1: Caracterização do dataset
  - Cards: #Repos, Stars totais, Forks totais, Média stars, #Issues, #PRs
  - Barras: Top 20 repos por stars
  - Treemap: Tópicos mais frequentes
  - Pizza: Licenças
  - Linha: Commits totais por semana (soma entre repositórios)
- Página 2: RQ1 (exemplo) — "Repositórios com mais releases têm mais popularidade?"
  - Scatter: metrics_repo[releases_count] vs metrics_repo[stargazers_count] (cor por language)
  - Filtros: linguagem, período (pushed_at)
- Página 3: RQ2 (exemplo) — "Mais PRs fechados correlacionam com mais issues?"
  - Barras lado a lado: metrics_repo[pulls_closed_count] vs metrics_repo[issues_count] por repo

> Ajuste as RQs conforme seu GQM. Esta base permite vários recortes por linguagem, período, popularidade e atividade.
