from __future__ import annotations
from typing import Any, Dict, List
import csv
from ..config.config import Config, RAW_DIR
from .github_client import GitHubClient

class IssuesCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def collect_issues(self, owner: str, repo: str, state: str = "all", max_pages: int = 5) -> List[Dict[str, Any]]:
        url = f"{self.config.api_base}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        issues: List[Dict[str, Any]] = []
        for page in self.client.get_paged(url, params=params, per_page=100, max_pages=max_pages):
            for it in page:
                if "pull_request" in it:
                    continue  # ignora PRs da listagem de issues
                issues.append({
                    "repo_full_name": f"{owner}/{repo}",
                    "id": it.get("id"),
                    "number": it.get("number"),
                    "title": it.get("title"),
                    "state": it.get("state"),
                    "comments": it.get("comments"),
                    "created_at": it.get("created_at"),
                    "updated_at": it.get("updated_at"),
                    "closed_at": it.get("closed_at"),
                    "user_login": (it.get("user") or {}).get("login"),
                    "labels": ",".join([l.get("name") for l in it.get("labels", []) if l.get("name")]),
                })
        return issues

    def save(self, items: List[Dict[str, Any]], filename: str) -> str:
        self.config.ensure_dirs()
        out = RAW_DIR / filename
        if not items:
            out.write_text("")
            return str(out)
        with out.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(items[0].keys()))
            writer.writeheader()
            writer.writerows(items)
        return str(out)
