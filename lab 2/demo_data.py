#!/usr/bin/env python3
"""
EXEMPLO DE EXECUÇÃO SEM TOKEN
Demonstra a estrutura de dados que o programa geraria
"""

import pandas as pd
import os
from pathlib import Path

def create_example_data():
    """Cria dados de exemplo que demonstram a estrutura esperada."""
    
    # Criar diretórios
    output_dir = Path("output/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Dados de exemplo para demonstração
    example_repos = [
        {
            'name': 'spring-projects/spring-boot',
            'url': 'https://github.com/spring-projects/spring-boot',
            'language': 'Java',
            'description': 'Spring Boot makes it easy to create stand-alone applications',
            'created_at': '2013-12-05T16:25:46Z',
            'updated_at': '2024-01-15T10:30:00Z',
            'stars': 74800,
            'forks': 40200,
            'watchers': 74800,
            'contributors': 850,
            'releases': 245,
            'age_years': 11.2,
            'loc_total': 485000,
            'loc_comments_total': 95000,
            'classes_count': 3200,
            'methods_count': 18500,
            'cbo_avg': 8.5,
            'cbo_max': 45,
            'dit_avg': 2.3,
            'dit_max': 8,
            'lcom_avg': 12.7,
            'lcom_max': 89,
            'wmc_avg': 15.2,
            'noc_avg': 1.8,
            'cc_avg': 3.4,
            'clone_url': 'https://github.com/spring-projects/spring-boot.git'
        },
        {
            'name': 'elastic/elasticsearch',
            'url': 'https://github.com/elastic/elasticsearch', 
            'language': 'Java',
            'description': 'Free and Open, Distributed, RESTful Search Engine',
            'created_at': '2010-02-08T13:20:56Z',
            'updated_at': '2024-01-15T08:45:00Z',
            'stars': 69500,
            'forks': 24300,
            'watchers': 69500,
            'contributors': 1850,
            'releases': 180,
            'age_years': 14.9,
            'loc_total': 892000,
            'loc_comments_total': 178000,
            'classes_count': 5100,
            'methods_count': 35200,
            'cbo_avg': 12.8,
            'cbo_max': 78,
            'dit_avg': 3.1,
            'dit_max': 12,
            'lcom_avg': 18.4,
            'lcom_max': 145,
            'wmc_avg': 22.1,
            'noc_avg': 2.4,
            'cc_avg': 4.8,
            'clone_url': 'https://github.com/elastic/elasticsearch.git'
        },
        {
            'name': 'apache/kafka',
            'url': 'https://github.com/apache/kafka',
            'language': 'Java', 
            'description': 'Mirror of Apache Kafka',
            'created_at': '2012-10-19T16:50:30Z',
            'updated_at': '2024-01-15T12:15:00Z',
            'stars': 28200,
            'forks': 13800,
            'watchers': 28200,
            'contributors': 920,
            'releases': 85,
            'age_years': 12.2,
            'loc_total': 654000,
            'loc_comments_total': 124000,
            'classes_count': 2100,
            'methods_count': 18900,
            'cbo_avg': 9.7,
            'cbo_max': 52,
            'dit_avg': 2.8,
            'dit_max': 9,
            'lcom_avg': 15.3,
            'lcom_max': 98,
            'wmc_avg': 18.6,
            'noc_avg': 2.1,
            'cc_avg': 4.2,
            'clone_url': 'https://github.com/apache/kafka.git'
        }
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(example_repos)
    
    # Salvar lista de repositórios
    repos_list = df[['name', 'stars', 'forks', 'language', 'description', 'url', 'clone_url', 'created_at', 'updated_at']].copy()
    repos_list.insert(0, 'rank', range(1, len(repos_list) + 1))
    repos_list.to_csv(output_dir / "top_1000_java_repos_list.csv", index=False)
    
    # Salvar métricas completas
    df.to_csv(output_dir / "test_single_repo.csv", index=False)
    
    print("📊 EXEMPLO DE DADOS GERADOS")
    print("=" * 50)
    print(f"✅ Arquivos criados:")
    print(f"   • {output_dir}/top_1000_java_repos_list.csv")
    print(f"   • {output_dir}/test_single_repo.csv")
    
    print(f"\n📈 RESUMO DOS DADOS:")
    print(f"   • Repositórios analisados: {len(example_repos)}")
    print(f"   • Estrelas médias: {df['stars'].mean():.0f}")
    print(f"   • Idade média: {df['age_years'].mean():.1f} anos")
    print(f"   • LOC médio: {df['loc_total'].mean():.0f}")
    print(f"   • CBO médio: {df['cbo_avg'].mean():.2f}")
    print(f"   • DIT médio: {df['dit_avg'].mean():.2f}")
    print(f"   • LCOM médio: {df['lcom_avg'].mean():.2f}")
    
    print(f"\n📋 COLUNAS DISPONÍVEIS PARA ANÁLISE:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    print(f"\n🔍 PRÉVIA DOS DADOS:")
    print(df[['name', 'stars', 'age_years', 'loc_total', 'cbo_avg', 'dit_avg', 'lcom_avg']].head())
    
    return df

if __name__ == "__main__":
    print("🧪 DEMO - Estrutura de Dados do Lab 02")
    print("=" * 50)
    print("Este script demonstra a estrutura de dados que será")
    print("coletada pelo programa principal quando configurado.")
    print()
    
    df = create_example_data()
    
    print("\n🚀 PARA EXECUTAR COM DADOS REAIS:")
    print("   1. Configure seu token GitHub no arquivo src/.env")
    print("   2. Execute: cd src && python main.py")
    print("   3. Para todos os 1.000 repos: python main.py --full")
