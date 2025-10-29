from __future__ import annotations
from typing import Any, Dict, List
import csv
from ..config.config import Config, RAW_DIR
from .github_client import GitHubClient

class PullsCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def collect_pulls(self, owner: str, repo: str, state: str = "closed", max_pages: int = 5) -> List[Dict[str, Any]]:
        url = f"{self.config.api_base}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "sort": "updated", "direction": "desc"}
        pulls: List[Dict[str, Any]] = []
        for page in self.client.get_paged(url, params=params, per_page=100, max_pages=max_pages):
            for pr in page:
                pulls.append({
                    "repo_full_name": f"{owner}/{repo}",
                    "id": pr.get("id"),
                    "number": pr.get("number"),
                    "state": pr.get("state"),
                    "title": pr.get("title"),
                    "user_login": (pr.get("user") or {}).get("login"),
                    "created_at": pr.get("created_at"),
                    "updated_at": pr.get("updated_at"),
                    "closed_at": pr.get("closed_at"),
                    "merged_at": pr.get("merged_at"),
                    "additions": pr.get("additions"),
                    "deletions": pr.get("deletions"),
                    "changed_files": pr.get("changed_files"),
                })
        return pulls

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
