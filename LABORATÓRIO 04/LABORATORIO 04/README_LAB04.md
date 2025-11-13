# LABORATÓRIO 04 - Visualização de Dados com BI

## Estrutura dos Dados

Esta pasta contém todos os datasets necessários para criar o dashboard de BI do projeto TI6.

### 📁 Pasta `dados/`

#### Caracterização do Dataset (Sprint 01):

1. **valid_repositories.csv**
   - Lista dos repositórios válidos selecionados para o estudo
   - Use para caracterizar os objetos de estudo

2. **RQ4_KLOC.csv**
   - Dados sobre linhas de código (KLOC) dos repositórios
   - Útil para caracterização de tamanho dos projetos

#### Questões de Pesquisa (Sprint 02 e 03):

3. **rq1_volume_keycloak_results.csv**
   - Resultados da análise de volume (RQ1)
   - Contém métricas de volume por release

4. **Analise_TestSmells_Releases_Repos.csv**
   - Análise consolidada de test smells por releases e repositórios
   - Visão geral para RQ2

5. **Pasta rq2_out/**
   - `Output_TestSmellDetection_*.csv`: Detecção detalhada de test smells
   - `test_files_keycloak_*_block1.csv`: Arquivos de teste analisados por release
   - `log_keycloak_*_block1.txt`: Logs de execução por release

## Como Usar no BI

### Power BI / Tableau / Google Data Studio

1. **Sprint 01 - Caracterização do Dataset:**
   - Importe: `valid_repositories.csv` e `RQ4_KLOC.csv`
   - Crie visualizações mostrando características dos repositórios estudados

2. **Sprint 02 - RQs 1 e 2:**
   - RQ1: Importe `rq1_volume_keycloak_results.csv`
   - RQ2: Importe `Analise_TestSmells_Releases_Repos.csv` e arquivos relevantes de `rq2_out/`

3. **Sprint 03 - Dashboard Final:**
   - Consolide todas as visualizações
   - Garanta que o dashboard seja auto-explicativo
   - Apresente cada RQ com suas visualizações

## Dicas

- Escolha visualizações adequadas para cada tipo de dado
- Use medidas de tendência central apropriadas (média, mediana)
- Deixe os eixos e labels claros
- Conte uma história com os dados
