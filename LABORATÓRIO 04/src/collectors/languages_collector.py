from __future__ import annotations
from typing import Any, Dict, List
import csv
from ..config.config import Config, RAW_DIR
from .github_client import GitHubClient

class LanguagesCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def collect_languages(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        url = f"{self.config.api_base}/repos/{owner}/{repo}/languages"
        resp = self.client.get(url)
        lang_map = resp.json() or {}
        rows: List[Dict[str, Any]] = []
        for lang, bytes_count in lang_map.items():
            rows.append({
                "repo_full_name": f"{owner}/{repo}",
                "language": lang,
                "bytes": bytes_count,
            })
        return rows

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
