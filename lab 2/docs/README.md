# 📊 Análise de Qualidade de Repositórios Java

**Laboratório de Experimentação de Software - Lab 02**

## 🎯 Objetivo

Analisar aspectos da qualidade de repositórios Java do GitHub, correlacionando características do processo de desenvolvimento com métricas de produto calculadas através da ferramenta CK.

## 🔬 Questões de Pesquisa

- **RQ01:** Qual a relação entre a **popularidade** dos repositórios e suas características de qualidade?
- **RQ02:** Qual a relação entre a **maturidade** dos repositórios e suas características de qualidade?
- **RQ03:** Qual a relação entre a **atividade** dos repositórios e suas características de qualidade?
- **RQ04:** Qual a relação entre o **tamanho** dos repositórios e suas características de qualidade?

## 📏 Métricas Definidas

### 📈 Métricas de Processo
- **Popularidade:** Número de estrelas
- **Tamanho:** Linhas de código (LOC) e comentários
- **Atividade:** Número de releases
- **Maturidade:** Idade em anos do repositório

### 🔍 Métricas de Qualidade (CK Tool)
- **CBO:** Coupling Between Objects
- **DIT:** Depth Inheritance Tree
- **LCOM:** Lack of Cohesion of Methods

## 📋 Sprint 1 (Lab02S01) - Status: ✅ Implementado

### Requisitos Atendidos:
- ✅ **Lista dos 1.000 repositórios Java** mais populares
- ✅ **Script de Automação** para clone e coleta de métricas
- ✅ **Arquivo CSV** com resultado das medições

### Arquivos Gerados:
- `output/data/top_1000_java_repos_list.csv` - Lista completa dos repositórios
- `output/data/top_1000_java_repos.csv` - Métricas detalhadas (modo completo)
- `output/data/test_single_repo.csv` - Teste com 1 repositório

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Java** instalado (para ferramenta CK)
3. **Git** instalado
4. **Ferramenta CK compilada**

### Configuração Inicial

1. **Clone e configure a ferramenta CK:**
```bash
git clone https://github.com/mauricioaniche/ck
cd ck
mvn clean package
```

2. **Configure o token do GitHub:**
   - Acesse: https://github.com/settings/tokens
   - Crie um Personal Access Token (classic)
   - Edite `src/.env` e substitua `your_github_token_here` pelo seu token

3. **Instale as dependências Python:**
```bash
pip install -r requirements.txt
```

### Execução

```bash
cd src

# Modo de teste (1 repositório)
python main.py

# Modo completo (1.000 repositórios) 
python main.py --full

# Modo completo com caminho personalizado para CK
python main.py --full "C:\caminho\para\ck.jar"

# Ajuda
python main.py --help
```

## 📊 Estrutura dos Dados Coletados

### Campos no CSV de Saída:

| Campo | Descrição | Tipo |
|-------|-----------|------|
| `name` | Nome completo do repositório | string |
| `url` | URL do repositório | string |
| `stars` | Número de estrelas | int |
| `forks` | Número de forks | int |
| `contributors` | Número de contribuidores | int |
| `releases` | Número de releases | int |
| `age_years` | Idade em anos | float |
| `loc_total` | Total de linhas de código | int |
| `loc_comments_total` | Total de linhas de comentários | int |
| `classes_count` | Número de classes | int |
| `methods_count` | Número de métodos | int |
| `cbo_avg` | CBO médio | float |
| `dit_avg` | DIT médio | float |
| `lcom_avg` | LCOM médio | float |

## 🏗️ Estrutura do Projeto

```
lab 2/
├── src/
│   ├── main.py                 # Ponto de entrada principal
│   ├── .env                    # Configurações de ambiente
│   ├── config/
│   │   └── config.py          # Configurações do projeto
│   └── collectors/
│       └── rest_collector.py  # Coletor principal de dados
├── output/
│   └── data/                  # Arquivos CSV gerados
├── docs/
│   └── README.md              # Este arquivo
├── temp_repos/                # Diretório temporário (auto-criado)
└── requirements.txt           # Dependências Python
```

## 🔄 Processo de Coleta

1. **Busca via API:** Coleta lista dos top 1.000 repositórios Java mais populares
2. **Clone temporário:** Clona cada repositório localmente (shallow clone)
3. **Análise CK:** Executa ferramenta CK para extrair métricas de qualidade
4. **Coleta de metadados:** Busca informações adicionais via API (releases, contribuidores, etc.)
5. **Limpeza:** Remove arquivos temporários
6. **Export:** Salva tudo em CSV estruturado

## 📈 Próximos Passos (Sprint 2)

- [ ] Análise estatística completa
- [ ] Testes de correlação (Pearson/Spearman)
- [ ] Visualizações e gráficos
- [ ] Relatório final com hipóteses
- [ ] Apresentação dos resultados

## 🛠️ Solução de Problemas

### Erro de Token GitHub
```
❌ Token do GitHub não configurado corretamente
```
**Solução:** Configure o token no arquivo `.env`

### Erro da Ferramenta CK
```
❌ Ferramenta CK não encontrada
```
**Solução:** Verifique o caminho para o JAR da ferramenta CK

### Erro de Rate Limit
```
🚫 Limite de rate da API atingido
```
**Solução:** O programa aguarda automaticamente. Use um token pessoal para limites maiores.

### Timeout de Clone
```
⏱️ Timeout na coleta - repositório muito grande
```
**Solução:** Normal para repositórios grandes. O programa continua com o próximo.

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de Solução de Problemas
2. Consulte os logs de execução do programa
3. Execute em modo de teste primeiro: `python main.py`

## 📜 Licença

Projeto acadêmico para fins educacionais - Laboratório de Experimentação de Software.