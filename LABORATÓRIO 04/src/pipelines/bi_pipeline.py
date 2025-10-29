from __future__ import annotations
from typing import List, Dict
from pathlib import Path
from ..config.config import Config, RAW_DIR
from ..collectors.repositories_collector import RepositoriesCollector
from ..collectors.issues_collector import IssuesCollector
from ..collectors.pulls_collector import PullsCollector
from ..collectors.releases_collector import ReleasesCollector
from ..collectors.commits_collector import CommitsCollector
from ..modules.bi_exporter import BIExporter
from ..collectors.languages_collector import LanguagesCollector

class BIPipeline:
    def __init__(self, config: Config):
        self.config = config
        self.repos = RepositoriesCollector(config)
        self.issues = IssuesCollector(config)
        self.pulls = PullsCollector(config)
        self.releases = ReleasesCollector(config)
        self.commits = CommitsCollector(config)
        self.exporter = BIExporter()
        self.languages = LanguagesCollector(config)

    def collect(self, language: str, min_stars: int, top: int, since: str | None = None) -> Dict[str, str]:
        self.config.ensure_dirs()
        repos = self.repos.search_repositories(language, min_stars, top, since)
        repo_path = self.repos.save(repos, "repositories.csv")

        # Para cada repo, coleta amostras (limitadas por páginas) para S01
        results: Dict[str, str] = {"repositories": repo_path}
        for r in repos:
            owner = r["owner_login"]
            name = r["name"]
            slug = f"{owner}_{name}"
            # Issues
            iss = self.issues.collect_issues(owner, name, state="all", max_pages=2)
            if iss:
                results[f"issues_{slug}"] = self.issues.save(iss, f"issues_{slug}.csv")
            # Pulls
            prs = self.pulls.collect_pulls(owner, name, state="closed", max_pages=2)
            if prs:
                results[f"pulls_{slug}"] = self.pulls.save(prs, f"pulls_{slug}.csv")
            # Releases
            rels = self.releases.collect_releases(owner, name, max_pages=2)
            if rels:
                results[f"releases_{slug}"] = self.releases.save(rels, f"releases_{slug}.csv")
            # Commits weekly
            com = self.commits.collect_commit_activity(owner, name)
            if com:
                results[f"commits_{slug}"] = self.commits.save(com, f"commits_{slug}.csv")
            # Languages
            langs = self.languages.collect_languages(owner, name)
            if langs:
                results[f"languages_{slug}"] = self.languages.save(langs, f"languages_{slug}.csv")
        return results

    def export(self) -> Dict[str, str]:
        return self.exporter.export()
