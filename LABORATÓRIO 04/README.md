# LABORATÓRIO 04 — Dashboard de BI com dados reais do GitHub

Este laboratório foca em preparar um dataset sólido e normalizado para ser consumido por uma ferramenta de BI (Power BI, Tableau ou Looker Studio), a partir de mineração real de dados do GitHub.

Componentes entregues:
- Pipeline de coleta e exportação para BI
- CSV/JSON normalizados em `output/data`
- Guia de conexão com Power BI/Tableau em `docs/bi_guide.md`
- Script CLI para executar as sprints (S01, S02, S03)

Requisitos mínimos:
- Python 3.10+
- Um token válido do GitHub em variável de ambiente `GITHUB_TOKEN` (ou arquivo `.env`)

## Sprints

- S01: Caracterização do dataset (página 1 do dashboard)
  - Coleta de repositórios, metadados, donos, linguagens, tópicos
  - Estatísticas descritivas exportadas (contagens, médias)
- S02: Visualizações para RQ1 e RQ2
  - Você parametriza suas RQs no BI usando as tabelas geradas; exemplos no guia
- S03: Dashboard final + artigo atualizado
  - Exporte os gráficos do BI em PDF/PNG e inclua no artigo da TIS 6

## Como executar

1) Configure o token do GitHub (Windows PowerShell):

```powershell
# Opcional: salvar no .env
Set-Content -Path ".env" -Value "GITHUB_TOKEN=SEU_TOKEN_AQUI"
# Ou exportar só na sessão atual
$env:GITHUB_TOKEN = "SEU_TOKEN_AQUI"
```

2) Instale dependências:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3) Execute a S01 (caracterização):

```powershell
python main.py collect --language java --top 200 --min-stars 1000 --since 2019-01-01 --out output/data
python main.py export --out output/data
python main.py report --out output
```

Os CSVs para BI estarão em `output/data/bi/`.

4) Abra o Power BI e conecte-se aos arquivos CSV conforme `docs/bi_guide.md`.

## Estrutura gerada
- `src/collectors`: clientes e coletores para repositórios, issues, PRs, commits, releases
- `src/modules/bi_exporter.py`: normalização e exportação de tabelas
- `src/pipelines/bi_pipeline.py`: orquestração
- `output/data`: dados crus e normalizados

## Observações importantes
- A API do GitHub impõe limites de requisição. O pipeline usa um rate limit conservador e pausa automaticamente.
- Alguns endpoints de estatísticas (ex.: commits semanais) podem demorar a serem gerados pelo GitHub. O código faz polling com backoff.
- Para conjuntos grandes, a execução pode levar horas. Você pode reexecutar com os mesmos parâmetros; o coletor persiste arquivos incrementais.

## Próximos passos sugeridos
- Ajustar os filtros no `collect` (linguagem, estrelas, datas) para combinar com suas RQs
- Publicar o Power BI no serviço e agendar atualização com os CSVs em um local acessível
