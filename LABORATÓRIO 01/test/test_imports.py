# tests/test_imports.py

def test_import_graphql_collector():
    """Verifica se a classe GraphQLDataCollector pode ser importada sem erros."""
    from src.collectors.graphql_collector import GraphQLDataCollector
    # O teste passa se a linha acima não levantar uma exceção.


def test_import_rest_collector():
    """Verifica se a classe RestDataCollector pode ser importada sem erros."""
    from src.collectors.rest_collector import RestDataCollector


def test_import_data_analyzer():
    """Verifica se a classe DataAnalyzer pode ser importada sem erros."""
    from src.modules.data_analyzer import DataAnalyzer


def test_import_data_visualizer():
    """Verifica se a classe DataVisualizer pode ser importada sem erros."""
    from src.modules.data_visualizer import DataVisualizer


def test_import_report_generator():
    """Verifica se a classe ReportGenerator pode ser importada sem erros."""
    from src.modules.report_generator import ReportGenerator