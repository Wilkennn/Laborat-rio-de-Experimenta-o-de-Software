# Lab 02 - Análise de Qualidade de Repositórios Java

Análise automatizada de repositórios Java do GitHub para responder questões de pesquisa sobre qualidade de código.

## Uso

```bash
# Análise completa (100+ repositórios da API GitHub)
python main.py

# Modo teste (1 repositório)
python main.py --test

# Ajuda
python main.py --help
```

## Requisitos

```bash
pip install pandas matplotlib seaborn requests numpy
```

## Configuração

Edite o arquivo `.env` e adicione seu token GitHub:
```
GITHUB_TOKEN=seu_token_aqui
```

## Saídas

- `output/data/` - Dados CSV coletados
- `output/plots/` - Gráficos de análise
- `output/relatorio_qualidade_java_*.md` - Relatório final
- `output/analysis_results.json` - Resultados em JSON

## Questões de Pesquisa

- **RQ01**: Relação entre popularidade e qualidade
- **RQ02**: Relação entre maturidade e qualidade  
- **RQ03**: Relação entre atividade e qualidade
- **RQ04**: Relação entre tamanho e qualidade

## Métricas de Qualidade

- CBO (Coupling Between Objects)
- DIT (Depth of Inheritance Tree)
- LCOM (Lack of Cohesion of Methods)
- WMC (Weighted Methods per Class)
- CC (Cyclomatic Complexity)
