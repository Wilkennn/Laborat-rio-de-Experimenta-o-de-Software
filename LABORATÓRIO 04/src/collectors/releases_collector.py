from __future__ import annotations
from typing import Any, Dict, List
import csv
from ..config.config import Config, RAW_DIR
from .github_client import GitHubClient

class ReleasesCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def collect_releases(self, owner: str, repo: str, max_pages: int = 5) -> List[Dict[str, Any]]:
        url = f"{self.config.api_base}/repos/{owner}/{repo}/releases"
        releases: List[Dict[str, Any]] = []
        for page in self.client.get_paged(url, params=None, per_page=100, max_pages=max_pages):
            for r in page:
                releases.append({
                    "repo_full_name": f"{owner}/{repo}",
                    "id": r.get("id"),
                    "tag_name": r.get("tag_name"),
                    "name": r.get("name"),
                    "draft": r.get("draft"),
                    "prerelease": r.get("prerelease"),
                    "created_at": r.get("created_at"),
                    "published_at": r.get("published_at"),
                })
        return releases

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
