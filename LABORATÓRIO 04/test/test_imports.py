def test_imports():
    import src.config.config as c
    import src.collectors.github_client as g
    import src.collectors.repositories_collector as r
    import src.collectors.issues_collector as i
    import src.collectors.pulls_collector as p
    import src.collectors.releases_collector as rel
    import src.collectors.commits_collector as com
    import src.modules.bi_exporter as be
    import src.pipelines.bi_pipeline as bp

    assert c is not None and g is not None and r is not None
