import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_analise_visual_completa():
    """
    Carrega os dados e gera um conjunto completo de gráficos de boxplot
    com eixos ajustados (zoom) e anotações de mediana para responder
    claramente a todas as RQs (01 a 04).
    """
    # --- 1. Carregamento e Preparação dos Dados ---
    print("Iniciando a geração da análise visual completa...")
    try:
        df = pd.read_csv('dataset_final_v2.csv', sep=';')
        print("Arquivo 'dataset_final_v2.csv' carregado com sucesso.")
    except FileNotFoundError:
        print("ERRO: Arquivo 'dataset_final_v2.csv' não encontrado.")
        return

    df['status'] = df['merged'].apply(lambda x: 'MERGED' if x else 'CLOSED')
    df['total_lines_changed'] = df['additions'] + df['deletions']
    
    sns.set_style("whitegrid")
    palette = {"MERGED": "#2ca02c", "CLOSED": "#d62728"}

    # --- Função auxiliar para anotação ---
    def annotate_medians(ax, data, metric, unit=''):
        medians = data.groupby(['status'])[metric].median()
        for xtick, status in enumerate(['MERGED', 'CLOSED']):
            median_val = medians.loc[status]
            ax.text(xtick, median_val, f" Mediana:\n {median_val:.1f}{unit}", 
                    horizontalalignment='left', size='medium', color='black', weight='semibold',
                    bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

    # --- 2. Geração de Gráficos para a RQ01 (Tamanho) ---
    print("Gerando gráficos para a RQ01 (Tamanho do PR)...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('RQ01: Relação entre o Tamanho do PR e o Status Final (Com Zoom)', fontsize=20)
    size_metrics = {
        'changed_files': (axes[0, 0], 'Número de Arquivos Alterados', ''),
        'total_lines_changed': (axes[0, 1], 'Total de Linhas Alteradas', ''),
        'additions': (axes[1, 0], 'Apenas Linhas Adicionadas', ''),
        'deletions': (axes[1, 1], 'Apenas Linhas Removidas', '')
    }
    for metric, (ax, title, unit) in size_metrics.items():
        sns.boxplot(ax=ax, x='status', y=metric, data=df, palette=palette, order=['MERGED', 'CLOSED'], hue='status', legend=False)
        ax.set_title(title, fontsize=14)
        ax.set_xlabel('Status do PR', fontsize=12)
        ax.set_ylabel(f'Contagem{unit}', fontsize=12)
        upper_limit = df[metric].quantile(0.95)
        ax.set_ylim(0, upper_limit * 1.05)
        annotate_medians(ax, df, metric)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('grafico_completo_RQ01_tamanho.png', dpi=300)
    plt.close()

    # --- 3. Geração de Gráfico para a RQ02 (Tempo) ---
    print("Gerando gráfico para a RQ02 (Tempo de Análise)...")
    plt.figure(figsize=(10, 7))
    ax = sns.boxplot(x='status', y='review_duration_hours', data=df, palette=palette, order=['MERGED', 'CLOSED'], hue='status', legend=False)
    ax.set_title('RQ02: Relação entre o Tempo de Análise e o Status Final (Com Zoom)', fontsize=18, pad=20)
    ax.set_xlabel('Status do PR', fontsize=14)
    ax.set_ylabel('Tempo de Análise (Horas)', fontsize=14)
    upper_limit_time = df['review_duration_hours'].quantile(0.95)
    ax.set_ylim(0, upper_limit_time * 1.05)
    annotate_medians(ax, df, 'review_duration_hours', unit='h')
    plt.tight_layout()
    plt.savefig('grafico_completo_RQ02_tempo.png', dpi=300)
    plt.close()
    
    # --- 4. Geração de Gráficos para RQ03 e RQ04 (Descrição e Interações) ---
    print("Gerando gráficos para RQ03 (Descrição) e RQ04 (Interações)...")
    fig, axes = plt.subplots(1, 3, figsize=(24, 8))
    fig.suptitle('RQs 03 & 04: Descrição e Interações vs. Status Final (Com Zoom)', fontsize=20)
    
    # Gráfico RQ03: Tamanho da Descrição
    sns.boxplot(ax=axes[0], x='status', y='description_length', data=df, palette=palette, order=['MERGED', 'CLOSED'], hue='status', legend=False)
    axes[0].set_title('RQ03: Tamanho da Descrição', fontsize=14)
    axes[0].set_xlabel('Status do PR', fontsize=12)
    axes[0].set_ylabel('Contagem de Caracteres', fontsize=12)
    upper_limit_desc = df['description_length'].quantile(0.95)
    axes[0].set_ylim(0, upper_limit_desc * 1.05)
    annotate_medians(axes[0], df, 'description_length', unit=' chars')
    
    # Gráfico RQ04: Número de Participantes
    sns.boxplot(ax=axes[1], x='status', y='participants_count', data=df, palette=palette, order=['MERGED', 'CLOSED'], hue='status', legend=False)
    axes[1].set_title('RQ04: Número de Participantes', fontsize=14)
    axes[1].set_xlabel('Status do PR', fontsize=12)
    axes[1].set_ylabel('Contagem de Participantes', fontsize=12)
    upper_limit_part = df['participants_count'].quantile(0.95)
    axes[1].set_ylim(0, upper_limit_part * 1.05)
    annotate_medians(axes[1], df, 'participants_count')

    # Gráfico RQ04: Número de Comentários
    sns.boxplot(ax=axes[2], x='status', y='comments_count', data=df, palette=palette, order=['MERGED', 'CLOSED'], hue='status', legend=False)
    axes[2].set_title('RQ04: Número de Comentários', fontsize=14)
    axes[2].set_xlabel('Status do PR', fontsize=12)
    axes[2].set_ylabel('Contagem de Comentários', fontsize=12)
    upper_limit_comm = df['comments_count'].quantile(0.95)
    axes[2].set_ylim(0, upper_limit_comm * 1.05)
    annotate_medians(axes[2], df, 'comments_count')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('grafico_completo_RQ03_RQ04.png', dpi=300)
    plt.close()

    print("\nAnálise concluída! Todos os gráficos foram gerados e salvos.")

if __name__ == '__main__':
    gerar_analise_visual_completa()