import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Carregamento e Preparação dos Dados ---

# Carrega o dataset a partir do arquivo CSV
try:
    df = pd.read_csv('dataset_final_v2.csv', sep=';')
    print("Arquivo 'dataset_final_v2.csv' carregado com sucesso.")
except FileNotFoundError:
    print("Erro: Arquivo 'dataset_final_v2.csv' não encontrado. Coloque o arquivo no mesmo diretório do script.")
    exit()

# Converte a coluna booleana 'merged' para uma coluna de texto 'status' para melhor visualização nos gráficos
df['status'] = df['merged'].apply(lambda x: 'MERGED' if x else 'CLOSED')

# Função auxiliar para remover outliers visuais nos boxplots
# Isso ajuda a visualizar melhor a distribuição dos dados centrais
def remove_outliers(df, column):
    """Filtra o dataframe para remover outliers de uma coluna específica para visualização."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# --- 2. Geração dos Gráficos ---

# Define um estilo visual agradável para todos os gráficos
sns.set(style="whitegrid")

# Cria uma cópia do dataframe para usar nos plots sem outliers, preservando o original
df_plot = df.copy()

# ==============================================================================
# GRÁFICO PARA RQ 01: Relação entre o TAMANHO dos PRs e o feedback final
# ==============================================================================
print("Gerando gráfico para RQ01...")
plt.figure(figsize=(18, 6))
plt.suptitle('RQ 01: Relação entre o Tamanho do PR e o Status Final (Sem Outliers Visuais)', fontsize=16)

# Subplot 1: Linhas Adicionadas
plt.subplot(1, 3, 1)
df_temp_add = remove_outliers(df_plot, 'additions')
sns.boxplot(x='status', y='additions', data=df_temp_add, palette="pastel")
plt.title('Status vs. Linhas Adicionadas')
plt.xlabel('Status do PR')
plt.ylabel('Linhas Adicionadas')

# Subplot 2: Linhas Removidas
plt.subplot(1, 3, 2)
df_temp_del = remove_outliers(df_plot, 'deletions')
sns.boxplot(x='status', y='deletions', data=df_temp_del, palette="pastel")
plt.title('Status vs. Linhas Removidas')
plt.xlabel('Status do PR')
plt.ylabel('Linhas Removidas')

# Subplot 3: Arquivos Modificados
plt.subplot(1, 3, 3)
df_temp_files = remove_outliers(df_plot, 'changed_files')
sns.boxplot(x='status', y='changed_files', data=df_temp_files, palette="pastel")
plt.title('Status vs. Arquivos Modificados')
plt.xlabel('Status do PR')
plt.ylabel('Arquivos Modificados')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('grafico_rq01_tamanho_status.png', dpi=300)
plt.clf() # Limpa a figura para o próximo gráfico

# ==============================================================================
# GRÁFICO PARA RQ 02: Relação entre o TEMPO DE ANÁLISE e o feedback final
# ==============================================================================
print("Gerando gráfico para RQ02...")
plt.figure(figsize=(8, 6))
df_temp_time = remove_outliers(df_plot, 'review_duration_hours')
sns.boxplot(x='status', y='review_duration_hours', data=df_temp_time, palette="pastel")
plt.title('RQ 02: Relação entre o Tempo de Análise e o Status Final (Sem Outliers Visuais)')
plt.xlabel('Status do PR')
plt.ylabel('Duração da Revisão (horas)')
plt.savefig('grafico_rq02_tempo_status.png', dpi=300)
plt.clf()

# ==============================================================================
# GRÁFICO PARA RQ 03: Relação entre a DESCRIÇÃO e o feedback final
# ==============================================================================
print("Gerando gráfico para RQ03...")
plt.figure(figsize=(8, 6))
df_temp_desc = remove_outliers(df_plot, 'description_length')
sns.boxplot(x='status', y='description_length', data=df_temp_desc, palette="pastel")
plt.title('RQ 03: Relação entre o Tamanho da Descrição e o Status Final (Sem Outliers Visuais)')
plt.xlabel('Status do PR')
plt.ylabel('Tamanho da Descrição (caracteres)')
plt.savefig('grafico_rq03_descricao_status.png', dpi=300)
plt.clf()

# ==============================================================================
# GRÁFICO PARA RQ 04: Relação entre as INTERAÇÕES e o feedback final
# ==============================================================================
print("Gerando gráfico para RQ04...")
plt.figure(figsize=(14, 6))
plt.suptitle('RQ 04: Relação entre as Interações no PR e o Status Final (Sem Outliers Visuais)', fontsize=16)

# Subplot 1: Número de Participantes
plt.subplot(1, 2, 1)
df_temp_part = remove_outliers(df_plot, 'participants_count')
sns.boxplot(x='status', y='participants_count', data=df_temp_part, palette="pastel")
plt.title('Status vs. Número de Participantes')
plt.xlabel('Status do PR')
plt.ylabel('Número de Participantes')

# Subplot 2: Número de Comentários
plt.subplot(1, 2, 2)
df_temp_comm = remove_outliers(df_plot, 'comments_count')
sns.boxplot(x='status', y='comments_count', data=df_temp_comm, palette="pastel")
plt.title('Status vs. Número de Comentários')
plt.xlabel('Status do PR')
plt.ylabel('Número de Comentários')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('grafico_rq04_interacoes_status.png', dpi=300)
plt.clf()

# ==============================================================================
# GRÁFICO PARA RQs 05-08: Matriz de Correlação
# ==============================================================================
print("Gerando Matriz de Correlação para RQs 05-08...")
# Seleciona apenas as colunas numéricas de interesse
metricas = ['additions', 'deletions', 'changed_files', 'review_duration_hours', 'description_length', 'participants_count', 'comments_count']
df_corr = df[metricas]

# Calcula a matriz de correlação de Spearman, mais robusta a outliers e relações não-lineares
correlation_matrix = df_corr.corr(method='spearman')

# Plota a matriz de correlação como um heatmap
plt.figure(figsize=(12, 9))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Matriz de Correlação de Spearman entre as Métricas dos PRs', fontsize=16)
plt.xticks(rotation=45, ha='right') # Rotaciona os labels do eixo X para melhor leitura
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('grafico_correlacao_metricas.png', dpi=300)
plt.clf()

print("\nAnálise concluída! Todos os gráficos foram salvos no diretório.")