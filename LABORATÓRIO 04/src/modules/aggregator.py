from __future__ import annotations
from typing import Dict, List, Tuple
from pathlib import Path
import csv
from datetime import datetime, timezone
from ..config.config import RAW_DIR, BI_DIR

class Aggregator:
    """
    Gera métricas agregadas por repositório para apoiar as RQs no BI.
    Entrada: CSVs em RAW_DIR (repositories.csv, issues_*.csv, pulls_*.csv, releases_*.csv, commits_*.csv)
    Saída: BI_DIR/metrics_repo.csv
    """

    def _read_dicts(self, path: Path) -> List[Dict[str, str]]:
        if not path.exists() or path.stat().st_size == 0:
            return []
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _glob_merge(self, pattern: str) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        for f in RAW_DIR.glob(pattern):
            rows.extend(self._read_dicts(f))
        return rows

    def compute(self) -> str:
        repos = self._read_dicts(RAW_DIR / "repositories.csv")
        issues = self._glob_merge("issues_*.csv")
        pulls = self._glob_merge("pulls_*.csv")
        releases = self._glob_merge("releases_*.csv")
        commits = self._glob_merge("commits_*.csv")

        # Index por repo
        def group_count(rows: List[Dict[str, str]], key: str) -> Dict[str, int]:
            out: Dict[str, int] = {}
            for r in rows:
                k = r.get(key)
                if not k:
                    continue
                out[k] = out.get(k, 0) + 1
            return out

        issues_by_repo = group_count(issues, "repo_full_name")
        pulls_by_repo = group_count(pulls, "repo_full_name")
        releases_by_repo = group_count(releases, "repo_full_name")

        # pulls merged
        merged_by_repo: Dict[str, int] = {}
        for pr in pulls:
            repo = pr.get("repo_full_name")
            if not repo:
                continue
            merged = 1 if (pr.get("merged_at") and len(pr.get("merged_at")) > 0) else 0
            merged_by_repo[repo] = merged_by_repo.get(repo, 0) + merged

        # commits últimas 52 semanas (soma total)
        commits_total_by_repo: Dict[str, int] = {}
        for c in commits:
            repo = c.get("repo_full_name")
            if not repo:
                continue
            try:
                total = int(c.get("total_commits") or 0)
            except Exception:
                total = 0
            commits_total_by_repo[repo] = commits_total_by_repo.get(repo, 0) + total

        # agora monta tabela agregada
        now = datetime.now(timezone.utc)
        rows_out: List[Dict[str, str]] = []
        for r in repos:
            repo = r.get("full_name")
            if not repo:
                continue
            created_at = r.get("created_at")
            pushed_at = r.get("pushed_at")
            def parse_iso(s: str) -> datetime | None:
                if not s:
                    return None
                try:
                    # GitHub usa ISO com Z
                    if s.endswith("Z"):
                        s = s.replace("Z", "+00:00")
                    return datetime.fromisoformat(s)
                except Exception:
                    return None
            dt_created = parse_iso(created_at)
            dt_pushed = parse_iso(pushed_at)
            age_days = (now - dt_created).days if dt_created else None
            days_since_push = (now - dt_pushed).days if dt_pushed else None

            def to_int(x):
                try: return int(x)
                except Exception: return 0

            rows_out.append({
                "repo_full_name": repo,
                "owner_login": r.get("owner_login"),
                "language": r.get("language"),
                "license": r.get("license"),
                "stargazers_count": to_int(r.get("stargazers_count")),
                "forks_count": to_int(r.get("forks_count")),
                "open_issues_count": to_int(r.get("open_issues_count")),
                "issues_count": issues_by_repo.get(repo, 0),
                "pulls_closed_count": pulls_by_repo.get(repo, 0),
                "pulls_merged_count": merged_by_repo.get(repo, 0),
                "releases_count": releases_by_repo.get(repo, 0),
                "commits_52w_total": commits_total_by_repo.get(repo, 0),
                "age_days": age_days if age_days is not None else "",
                "days_since_last_push": days_since_push if days_since_push is not None else "",
            })

        out_path = BI_DIR / "metrics_repo.csv"
        if not rows_out:
            out_path.write_text("")
            return str(out_path)
        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
            writer.writeheader()
            writer.writerows(rows_out)
        return str(out_path)
