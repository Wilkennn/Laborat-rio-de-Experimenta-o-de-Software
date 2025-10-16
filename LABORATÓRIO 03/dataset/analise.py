import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico_densidade_zoom():
    """
    Carrega os dados e gera um gráfico de densidade 2D (KDE Plot) para
    visualizar a relação entre a duração da revisão e o número de comentários,
    com foco (zoom) na área de maior concentração de dados.
    """
    # --- 1. Carregamento e Preparação dos Dados ---
    print("Iniciando a geração do gráfico de densidade...")
    try:
        df = pd.read_csv('dataset_final_v2.csv', sep=';')
        print("Arquivo 'dataset_final_v2.csv' carregado com sucesso.")
    except FileNotFoundError:
        print("ERRO: Arquivo 'dataset_final_v2.csv' não encontrado.")
        return

    # --- 2. Filtragem dos Dados para o "Zoom" ---

    # Para visualizar melhor a área de maior densidade, vamos focar nos 95%
    # dos dados com os menores valores, removendo os outliers mais extremos.
    p95_duration = df['review_duration_hours'].quantile(0.95)
    p95_comments = df['comments_count'].quantile(0.95)
    
    df_filtered = df[
        (df['review_duration_hours'] <= p95_duration) & 
        (df['comments_count'] <= p95_comments)
    ]

    # --- 3. Geração do Gráfico ---
    
    # Usamos sns.jointplot com kind='kde' para criar o gráfico de densidade.
    # O argumento `fill=True` preenche as áreas de contorno, criando o "mapa de calor".
    g = sns.jointplot(
        data=df_filtered, 
        x='review_duration_hours', 
        y='comments_count', 
        kind="kde",
        fill=True, 
        cmap="viridis", # Um mapa de cores popular e acessível
        height=8,
        space=0
    )
    
    # Ajustes de títulos e labels para maior clareza
    g.fig.suptitle('Densidade da Relação entre Duração da Revisão e Comentários (Foco nos 95% dos Dados)', y=1.02, fontsize=14)
    g.set_axis_labels('Duração da Revisão (Horas)', 'Número de Comentários', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('grafico_densidade_duracao_comentarios.png', dpi=300)
    plt.close()

    print("\nGráfico de densidade salvo com sucesso como 'grafico_densidade_duracao_comentarios.png'.")


if __name__ == '__main__':
    gerar_grafico_densidade_zoom()