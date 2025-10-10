"""
Script para demonstrar o funcionamento completo do LAB03S03
Executa análise com dados simulados para demonstração
"""
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_realistic_dataset():
    """Cria um dataset realista para demonstração"""
    print("🔬 Gerando dataset realista para demonstração...")
    
    # Configurações para dados realistas
    np.random.seed(42)
    n_samples = 500  # 500 PRs simulados
    
    # Simula diferentes tipos de PRs
    pr_types = ['hotfix', 'feature', 'bugfix', 'refactor', 'docs']
    pr_type_weights = [0.1, 0.4, 0.3, 0.15, 0.05]
    
    # Simula repositórios populares
    repos = [
        'microsoft/vscode', 'facebook/react', 'google/tensorflow',
        'torvalds/linux', 'apache/spark', 'kubernetes/kubernetes',
        'nodejs/node', 'python/cpython', 'golang/go', 'rust-lang/rust'
    ]
    
    data = []
    
    for i in range(n_samples):
        # Tipo de PR afeta as características
        pr_type = np.random.choice(pr_types, p=pr_type_weights)
        
        # Tamanho baseado no tipo
        if pr_type == 'hotfix':
            files_changed = np.random.poisson(2) + 1
            additions = np.random.lognormal(2, 0.5)
            deletions = np.random.lognormal(1.5, 0.5)
        elif pr_type == 'feature':
            files_changed = np.random.poisson(8) + 1
            additions = np.random.lognormal(4, 0.8)
            deletions = np.random.lognormal(2.5, 0.6)
        elif pr_type == 'docs':
            files_changed = np.random.poisson(3) + 1
            additions = np.random.lognormal(3, 0.4)
            deletions = np.random.lognormal(2, 0.4)
        else:  # bugfix, refactor
            files_changed = np.random.poisson(5) + 1
            additions = np.random.lognormal(3.5, 0.7)
            deletions = np.random.lognormal(3, 0.6)
        
        # Tempo de análise baseado na complexidade
        complexity_factor = (files_changed * 0.3 + np.log(additions + 1) * 0.7)
        base_hours = max(1.5, np.random.lognormal(1, 1) * complexity_factor)
        analysis_time_hours = base_hours
        
        # Número de revisões baseado na complexidade e tipo
        if pr_type == 'hotfix':
            reviews_count = max(1, np.random.poisson(1.5))
        elif pr_type == 'feature':
            reviews_count = max(1, np.random.poisson(3))
        else:
            reviews_count = max(1, np.random.poisson(2))
        
        # Participantes baseado nas revisões
        participants_count = reviews_count + np.random.poisson(1) + 1  # +1 para o autor
        
        # Comentários baseado na complexidade
        comments_base = max(0, np.random.poisson(analysis_time_hours / 24 * 2))
        total_comments = comments_base + np.random.poisson(reviews_count * 1.5)
        
        # Descrição - features têm descrições mais longas
        if pr_type == 'feature':
            desc_length = max(50, np.random.lognormal(5, 0.8))
        elif pr_type == 'docs':
            desc_length = max(30, np.random.lognormal(4.5, 0.6))
        else:
            desc_length = max(0, np.random.lognormal(4, 1))
        
        # Status final - hotfixes têm maior taxa de aprovação
        if pr_type == 'hotfix':
            merged = np.random.choice([True, False], p=[0.9, 0.1])
        elif pr_type == 'feature':
            merged = np.random.choice([True, False], p=[0.75, 0.25])
        else:
            merged = np.random.choice([True, False], p=[0.8, 0.2])
        
        # Datas realistas
        created_days_ago = np.random.randint(1, 365)
        created_at = (datetime.now() - timedelta(days=created_days_ago)).isoformat()
        
        pr_data = {
            'id': f'PR_{i+1}',
            'number': i + 1,
            'title': f'{pr_type.title()} PR #{i+1}',
            'body': 'A' * int(desc_length),  # Simula descrição
            'state': 'closed',
            'merged': merged,
            'created_at': created_at,
            'final_status': 'MERGED' if merged else 'CLOSED',
            'repo_full_name': np.random.choice(repos),
            
            # Métricas de tamanho
            'files_changed': int(files_changed),
            'additions': int(max(0, additions)),
            'deletions': int(max(0, deletions)),
            'total_changes': int(max(0, additions + deletions)),
            
            # Métricas de tempo
            'analysis_time_hours': float(analysis_time_hours),
            'analysis_time_days': float(analysis_time_hours / 24),
            
            # Métricas de descrição
            'description_length': int(desc_length),
            'has_description': desc_length > 10,
            
            # Métricas de interação
            'participants_count': int(participants_count),
            'total_comments': int(total_comments),
            'comments_count': int(total_comments // 2),
            'review_comments_count': int(total_comments - total_comments // 2),
            'reviews_count': int(reviews_count),
            
            # Metadata
            'pr_type': pr_type
        }
        
        data.append(pr_data)
    
    return pd.DataFrame(data)

def run_complete_analysis():
    """Executa análise completa com dados simulados"""
    print("🚀 LABORATÓRIO 03 - DEMONSTRAÇÃO COMPLETA LAB03S03")
    print("=" * 60)
    
    try:
        # Importa módulos
        from src.modules.statistical_analyzer import StatisticalAnalyzer
        from src.modules.data_visualizer import DataVisualizer
        from src.modules.report_generator import ReportGenerator
        
        # Gera dataset realista
        df = create_realistic_dataset()
        print(f"✅ Dataset criado: {len(df)} PRs simulados")
        print(f"   - Repositórios: {df['repo_full_name'].nunique()}")
        print(f"   - Taxa de merge: {(df['merged'].sum() / len(df) * 100):.1f}%")
        print(f"   - Período: {df['created_at'].min()[:10]} a {df['created_at'].max()[:10]}")
        
        # Salva dataset para referência
        output_file = f"output/data/demo_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(output_file, index=False)
        print(f"   - Dataset salvo em: {output_file}")
        
        # Análise estatística
        print("\\n📊 Executando análise estatística das 8 questões de pesquisa...")
        analyzer = StatisticalAnalyzer()
        analysis_results = analyzer.analyze_research_questions(df)
        
        # Mostra alguns resultados
        dataset_info = analysis_results.get('dataset_info', {})
        print(f"   ✓ {dataset_info.get('total_prs', 0)} PRs analisados")
        print(f"   ✓ Taxa de aprovação: {dataset_info.get('merge_rate', 0):.1f}%")
        
        # Visualizações
        print("\\n📈 Gerando visualizações...")
        visualizer = DataVisualizer()
        plot_files = visualizer.create_all_visualizations(df, analysis_results)
        print(f"   ✓ {len(plot_files)} visualizações geradas")
        
        # Lista alguns plots criados
        for plot_name, plot_path in list(plot_files.items())[:3]:
            print(f"     - {plot_name}: {os.path.basename(plot_path)}")
        if len(plot_files) > 3:
            print(f"     - ... e mais {len(plot_files) - 3} visualizações")
        
        # Relatório final
        print("\\n📝 Gerando relatório final...")
        report_gen = ReportGenerator()
        report_path = report_gen.generate_final_report(df, analysis_results, plot_files)
        print(f"   ✓ Relatório gerado: {os.path.basename(report_path)}")
        
        # Resumo dos resultados
        print("\\n🎯 RESUMO DOS RESULTADOS:")
        print("-" * 40)
        
        # RQ01-RQ04 (Feedback)
        feedback_results = analysis_results.get('rq_a_feedback', {})
        rq01 = feedback_results.get('rq01_size_vs_feedback', {})
        if rq01:
            print("📋 GRUPO A - Feedback Final:")
            for metric, test in rq01.get('statistical_tests', {}).items():
                sig = "Sim" if test.get('significant') else "Não"
                p_val = test.get('p_value', 1.0)
                print(f"   RQ01 ({metric}): Significante = {sig} (p={p_val:.3f})")
        
        # RQ05-RQ08 (Revisões)
        reviews_results = analysis_results.get('rq_b_reviews', {})
        rq05 = reviews_results.get('rq05_size_vs_reviews', {})
        if rq05:
            print("\\n📋 GRUPO B - Número de Revisões:")
            for metric, corr in rq05.get('correlations', {}).items():
                spearman = corr.get('spearman', {})
                rho = spearman.get('correlation', 0)
                sig = "Sim" if spearman.get('significant') else "Não"
                print(f"   RQ05 ({metric}): ρ = {rho:.3f}, Significante = {sig}")
        
        print("\\n🏆 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("📂 Arquivos gerados:")
        print(f"   - Dataset: {output_file}")
        print(f"   - Relatório: {report_path}")
        print(f"   - Visualizações: output/plots/ ({len(plot_files)} arquivos)")
        print("\\n🎉 LAB03S03 está 100% funcional e pronto para dados reais!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_complete_analysis()
    if success:
        print("\\n✨ Para usar com dados reais do GitHub:")
        print("   1. Configure seu token no arquivo .env")
        print("   2. Execute: python main.py --quick-test")
    else:
        sys.exit(1)