import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard: GraphQL vs REST", layout="wide", page_icon="🧪")

# --- CABEÇALHO ---
st.title("🧪 Análise Experimental: GraphQL vs REST")
st.markdown("---")

# --- SIDEBAR & UPLOAD (REGRA DE BLOQUEIO) ---
st.sidebar.header("📂 Configuração")
uploaded_file = st.sidebar.file_uploader("1. Anexe o CSV do experimento", type=["csv"])

# Lógica de Bloqueio: Se não tiver arquivo, para tudo aqui.
if uploaded_file is None:
    st.info("👆 Por favor, faça o upload do arquivo `resultados_experimento_final.csv` na barra lateral para iniciar a análise.")
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=100) # Logo decorativo opcional
    st.stop() # <--- COMANDO MÁGICO: Para a execução do script aqui.

# --- CARREGAMENTO E PROCESSAMENTO ---
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

df = load_data(uploaded_file)

# --- FILTROS LATERAIS ---
st.sidebar.header("2. Filtros de Dados")

# Filtro de Validade
mostrar_aquecimento = st.sidebar.checkbox("Incluir dados de Aquecimento (False)?", value=False)
if not mostrar_aquecimento:
    df = df[df['valido'] == True]

# Filtro de Cenários
todos_cenarios = df['cenario'].unique()
cenarios_sel = st.sidebar.multiselect("Filtrar Cenários", todos_cenarios, default=todos_cenarios)

# Filtro de Tecnologias
todas_tecs = df['tecnologia'].unique()
tecs_sel = st.sidebar.multiselect("Filtrar Tecnologias", todas_tecs, default=todas_tecs)

# Aplicação dos Filtros
df_filtered = df[
    (df['cenario'].isin(cenarios_sel)) & 
    (df['tecnologia'].isin(tecs_sel))
]

if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# --- CÁLCULO ESTATÍSTICO (INTERVALO DE CONFIANÇA) ---
def calcular_estatisticas(dataframe, metrica):
    # Agrupa e calcula média e erro padrão
    stats_df = dataframe.groupby(['cenario', 'tecnologia'])[metrica].agg(['mean', 'count', 'std']).reset_index()
    
    # Calcula Intervalo de Confiança de 95% (IC)
    # Fórmula: 1.96 * (std / sqrt(n))
    stats_df['ci95_hi'] = stats_df['mean'] + 1.96 * (stats_df['std'] / np.sqrt(stats_df['count']))
    stats_df['ci95_lo'] = stats_df['mean'] - 1.96 * (stats_df['std'] / np.sqrt(stats_df['count']))
    stats_df['error_bar'] = stats_df['ci95_hi'] - stats_df['mean'] # Tamanho da barra de erro para o Plotly
    
    return stats_df

# --- DASHBOARD VISUAL ---

# 1. KPIs DE RESUMO
st.subheader("📊 Visão Geral de Performance")
cols = st.columns(4)

media_tempo_rest = df_filtered[df_filtered['tecnologia']=='REST']['tempo_ms'].mean()
media_tempo_graph = df_filtered[df_filtered['tecnologia']=='GraphQL']['tempo_ms'].mean()
media_tam_rest = df_filtered[df_filtered['tecnologia']=='REST']['tamanho_bytes'].mean()
media_tam_graph = df_filtered[df_filtered['tecnologia']=='GraphQL']['tamanho_bytes'].mean()

if not np.isnan(media_tempo_rest) and not np.isnan(media_tempo_graph):
    speedup = media_tempo_rest / media_tempo_graph
    reduction = media_tam_rest / media_tam_graph
    
    cols[0].metric("Tempo Médio Global", f"{df_filtered['tempo_ms'].mean():.0f} ms")
    cols[1].metric("Tamanho Médio Global", f"{df_filtered['tamanho_bytes'].mean()/1024:.1f} KB")
    cols[2].metric("Aceleração (Speedup)", f"{speedup:.1f}x", "GraphQL mais rápido" if speedup > 1 else "REST mais rápido")
    cols[3].metric("Redução de Dados", f"{reduction:.1f}x", "GraphQL mais leve" if reduction > 1 else "REST mais leve")

st.divider()

# 2. GRÁFICOS COM BARRA DE ERRO (RELEVÂNCIA ESTATÍSTICA)
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Tempo de Resposta (com IC 95%)")
    stats_tempo = calcular_estatisticas(df_filtered, 'tempo_ms')
    
    fig_tempo = px.bar(
        stats_tempo, 
        x="cenario", 
        y="mean", 
        color="tecnologia",
        error_y="error_bar", # <--- AQUI ESTÁ O INTERVALO DE RELEVÂNCIA
        barmode="group",
        title="Média de Tempo + Intervalo de Confiança",
        labels={"mean": "Tempo (ms)", "error_bar": "IC 95%"},
        color_discrete_map={"REST": "#EF553B", "GraphQL": "#00CC96"},
        text_auto='.0f'
    )
    fig_tempo.update_layout(legend_title="Tecnologia")
    st.plotly_chart(fig_tempo, use_container_width=True)
    st.caption("ℹ️ As linhas pretas indicam o Intervalo de Confiança (95%). Se as barras de erro não se sobrepõem, a diferença é estatisticamente significativa.")

with col2:
    st.subheader("📦 Volume de Dados (Logarítmico)")
    stats_tam = calcular_estatisticas(df_filtered, 'tamanho_bytes')
    
    fig_tam = px.bar(
        stats_tam, 
        x="cenario", 
        y="mean", 
        color="tecnologia",
        error_y="error_bar",
        barmode="group",
        log_y=True, # Logarítmico para ver a diferença gigante
        title="Tamanho do Payload (Escala Log)",
        labels={"mean": "Bytes (Log)", "cenario": "Cenário"},
        color_discrete_map={"REST": "#EF553B", "GraphQL": "#00CC96"},
        text_auto='.2s'
    )
    st.plotly_chart(fig_tam, use_container_width=True)

# 3. ANÁLISE DE REQUISIÇÕES E DISTRIBUIÇÃO
col3, col4 = st.columns(2)

with col3:
    st.subheader("🔄 Custo de Comunicação (N+1)")
    # Simples agrupamento pois requests costumam ser constantes
    req_stats = df_filtered.groupby(['cenario', 'tecnologia'])['n_requests'].mean().reset_index()
    
    fig_req = px.bar(
        req_stats,
        x="cenario",
        y="n_requests",
        color="tecnologia",
        barmode="group",
        title="Número de Requisições HTTP (Round-Trips)",
        labels={"n_requests": "Qtde Requisições"},
        color_discrete_map={"REST": "#EF553B", "GraphQL": "#00CC96"},
        text_auto=True
    )
    st.plotly_chart(fig_req, use_container_width=True)

with col4:
    st.subheader("📈 Estabilidade (Boxplot)")
    fig_box = px.box(
        df_filtered, 
        x="cenario", 
        y="tempo_ms", 
        color="tecnologia", 
        title="Dispersão e Outliers",
        color_discrete_map={"REST": "#EF553B", "GraphQL": "#00CC96"}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# 4. TABELA DETALHADA
st.divider()
with st.expander("🧮 Ver Tabela Estatística Detalhada (Média, Desvio Padrão, IC)"):
    st.markdown("Esta tabela resume os dados estatísticos. O **IC 95%** indica a faixa onde a média real provavelmente se encontra.")
    
    # Prepara uma tabela bonita
    resumo = stats_tempo.copy()
    resumo = resumo[['cenario', 'tecnologia', 'count', 'mean', 'std', 'ci95_lo', 'ci95_hi']]
    resumo.columns = ['Cenário', 'Tecnologia', 'Amostras', 'Média (ms)', 'Desvio Padrão', 'IC Mín', 'IC Máx']
    
    st.dataframe(resumo.style.format({
        'Média (ms)': '{:.2f}',
        'Desvio Padrão': '{:.2f}',
        'IC Mín': '{:.2f}',
        'IC Máx': '{:.2f}'
    }), use_container_width=True)

    # Download
    csv_download = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV Filtrado", csv_download, "dados_filtrados.csv", "text/csv")