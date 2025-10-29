from __future__ import annotations
from typing import Any, Dict, List, Optional
from ..config.config import Config, DATA_DIR, RAW_DIR
import csv
from .github_client import GitHubClient

class RepositoriesCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def search_repositories(self, language: str, min_stars: int, top: int, since: Optional[str] = None) -> List[Dict[str, Any]]:
        q = f"language:{language} stars:>={min_stars}"
        if since:
            q += f" pushed:>={since}"
        url = f"{self.config.api_base}/search/repositories"
        params = {
            "q": q,
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
        }
        repos: List[Dict[str, Any]] = []
        for page_data in self.client.get_paged(url, params=params):
            items = page_data.get("items", [])
            for it in items:
                repos.append(self._map_repo(it))
                if len(repos) >= top:
                    return self._enrich_topics(repos)
        return self._enrich_topics(repos)

    def _map_repo(self, it: Dict[str, Any]) -> Dict[str, Any]:
        owner = it.get("owner", {})
        topics = it.get("topics", []) if isinstance(it.get("topics"), list) else []
        return {
            "id": it.get("id"),
            "name": it.get("name"),
            "full_name": it.get("full_name"),
            "private": it.get("private"),
            "owner_login": owner.get("login"),
            "owner_type": owner.get("type"),
            "html_url": it.get("html_url"),
            "description": it.get("description"),
            "fork": it.get("fork"),
            "created_at": it.get("created_at"),
            "updated_at": it.get("updated_at"),
            "pushed_at": it.get("pushed_at"),
            "homepage": it.get("homepage"),
            "size": it.get("size"),
            "stargazers_count": it.get("stargazers_count"),
            "watchers_count": it.get("watchers_count"),
            "language": it.get("language"),
            "forks_count": it.get("forks_count"),
            "open_issues_count": it.get("open_issues_count"),
            "default_branch": it.get("default_branch"),
            "topics": ",".join(topics),
            "visibility": it.get("visibility"),
            "license": (it.get("license") or {}).get("key"),
        }

    def save(self, repos: List[Dict[str, Any]], filename: str = "repositories.csv") -> str:
        self.config.ensure_dirs()
        out = RAW_DIR / filename
        if not repos:
            out.write_text("")
            return str(out)
        with out.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(repos[0].keys()))
            writer.writeheader()
            writer.writerows(repos)
        return str(out)

    def _enrich_topics(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Para cada repo sem tópicos preenchidos, tenta buscar via API /repos/{owner}/{repo}/topics."""
        for r in repos:
            if r.get("topics"):
                continue
            owner = r.get("owner_login")
            name = r.get("name")
            if not owner or not name:
                continue
            try:
                url = f"{self.config.api_base}/repos/{owner}/{name}/topics"
                resp = self.client.get(url)
                data = resp.json() or {}
                names = data.get("names", [])
                if names:
                    r["topics"] = ",".join(names)
            except Exception:
                # mantém vazio se falhar
                pass
        return repos
