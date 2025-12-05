# 🧪 Laboratório 05 - Experimento: GraphQL vs REST API

## 📋 Descrição

Este laboratório implementa um experimento controlado para comparar a performance entre APIs GraphQL e REST, focando em métricas de tempo de resposta, volume de dados transferidos e número de requisições HTTP.

## 🎯 Objetivos

- Comparar performance de GraphQL vs REST em cenários realistas
- Avaliar o problema N+1 em requisições REST
- Analisar eficiência no tráfego de dados
- Validar hipóteses com testes estatísticos

## 📁 Estrutura do Projeto

```
LABORATÓRIO 05/
│
├── experiment/
│   ├── main.py           # Script principal do experimento
│   └── dashboard.py      # Dashboard interativo (Streamlit)
│
├── data/
│   └── resultados_experimento_final.csv  # Dados coletados
│
├── docs/                 # Documentação adicional
│
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd "LABORATÓRIO 05"

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração

Edite o arquivo `experiment/main.py` e configure seu token do GitHub:

```python
GITHUB_TOKEN = "seu_token_aqui"
```

### 3. Execução do Experimento

```bash
cd experiment
python main.py
```

O experimento irá:
- Executar 30 rodadas de testes (5 de aquecimento + 25 válidas)
- Testar 3 cenários diferentes
- Comparar GraphQL vs REST em cada cenário
- Gerar CSV com os resultados na pasta `data/`
- Criar arquivo de log detalhado
- Gerar relatório JSON com estatísticas

### 4. Visualização dos Resultados

Execute o dashboard interativo:

```bash
cd experiment
streamlit run dashboard.py
```

O dashboard oferece:
- 📊 KPIs e métricas resumidas
- ⏱️ Gráficos de tempo com intervalo de confiança
- 📦 Análise de volume de dados
- 🔄 Comparação do problema N+1
- 📈 Boxplots de estabilidade
- 📊 Teste T de Student para significância estatística
- 🔗 Matriz de correlação entre métricas
- 📥 Download de dados filtrados

## 🧪 Cenários de Teste

### Cenário 1: Consulta Escalar
Busca informações básicas de uma organização (nome, descrição, website, localização).

### Cenário 2: Listagem Simples
Lista os 50 primeiros repositórios com nome e número de estrelas.

### Cenário 3: Dashboard Complexa (N+1)
Busca 5 repositórios com suas issues e linguagens de programação.
- **REST**: Requer múltiplas requisições (problema N+1)
- **GraphQL**: Uma única requisição com todos os dados

## 📊 Métricas Coletadas

- **tempo_ms**: Tempo de resposta em milissegundos
- **tamanho_bytes**: Volume de dados transferidos
- **n_requests**: Número de requisições HTTP realizadas
- **valido**: Se a medição deve ser considerada (exclui aquecimento)

## 📈 Análise Estatística

O experimento inclui:
- **Média e Desvio Padrão**: Tendência central e dispersão
- **Intervalo de Confiança (95%)**: Margem de erro das médias
- **Teste T de Student**: Verifica significância estatística (p-value < 0.05)
- **Correlação**: Relacionamento entre métricas

## 🔧 Configurações Avançadas

No arquivo `main.py`, você pode ajustar:

```python
NUM_EXECUCOES = 30         # Total de rodadas
DESCARTAR_PRIMEIROS = 5    # Rodadas de aquecimento
INTERVALO_ENTRE_RODADAS = 2 # Pausa entre testes (segundos)
ORG_NAME = "facebook"      # Organização do GitHub a testar
```

## 📝 Logs e Relatórios

O experimento gera automaticamente:
- `experimento_YYYYMMDD_HHMMSS.log` - Log detalhado da execução
- `relatorio_YYYYMMDD_HHMMSS.json` - Estatísticas em formato JSON
- `resultados_experimento_final.csv` - Dados brutos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Requests**: Cliente HTTP com retry automático
- **Pandas**: Manipulação e análise de dados
- **Streamlit**: Dashboard interativo
- **Plotly**: Visualizações interativas
- **SciPy**: Testes estatísticos

## 📚 Referências

- [GitHub REST API v3](https://docs.github.com/en/rest)
- [GitHub GraphQL API v4](https://docs.github.com/en/graphql)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)

## 👥 Autor

Desenvolvido para a disciplina de Laboratório de Experimentação de Software.

## 📄 Licença

Este projeto é disponibilizado para fins educacionais.

---

**Data de Última Atualização**: Dezembro de 2025
