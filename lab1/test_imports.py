#!/usr/bin/env python3
# Script de teste das importações

print("=== TESTE DE IMPORTAÇÕES ===")

try:
    from src.collectors.graphql_collector import GraphQLDataCollector
    print("✅ GraphQLDataCollector")
except Exception as e:
    print(f"❌ GraphQLDataCollector: {e}")

try:
    from src.collectors.rest_collector import RestDataCollector
    print("✅ RestDataCollector")
except Exception as e:
    print(f"❌ RestDataCollector: {e}")

try:
    from src.modules.data_analyzer import DataAnalyzer
    print("✅ DataAnalyzer")
except Exception as e:
    print(f"❌ DataAnalyzer: {e}")

try:
    from src.modules.data_visualizer import DataVisualizer
    print("✅ DataVisualizer")
except Exception as e:
    print(f"❌ DataVisualizer: {e}")

try:
    from src.modules.report_generator import ReportGenerator
    print("✅ ReportGenerator")
except Exception as e:
    print(f"❌ ReportGenerator: {e}")

print("\n=== TESTE COMPLETO ===")
