from __future__ import annotations
from typing import Any, Dict, List
import time
import csv
from ..config.config import Config, RAW_DIR
from .github_client import GitHubClient

class CommitsCollector:
    def __init__(self, config: Config):
        self.config = config
        self.client = GitHubClient(config)

    def collect_commit_activity(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """
        Usa o endpoint de estatística semanal de commits.
        Pode retornar 202 enquanto o GitHub gera as estatísticas; faremos polling.
        """
        url = f"{self.config.api_base}/repos/{owner}/{repo}/stats/commit_activity"
        for attempt in range(10):
            resp = self.client.session.get(url)
            if resp.status_code == 202:
                time.sleep(3 * (attempt + 1))
                continue
            resp.raise_for_status()
            data = resp.json() or []
            out: List[Dict[str, Any]] = []
            for w in data:
                week = w.get("week")
                iso = None
                if isinstance(week, int):
                    try:
                        import datetime as _dt
                        iso = _dt.datetime.utcfromtimestamp(week).date().isoformat()
                    except Exception:
                        iso = None
                out.append({
                    "repo_full_name": f"{owner}/{repo}",
                    "week_unix": week,
                    "total_commits": w.get("total"),
                    "week_start_iso": iso,
                })
            return out
        return []

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
