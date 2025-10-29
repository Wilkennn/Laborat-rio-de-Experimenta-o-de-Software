from __future__ import annotations
from typing import Dict, List
from pathlib import Path
import csv
from datetime import datetime
from ..config.config import RAW_DIR, OUTPUT_DIR, BI_DIR

class ReportGenerator:
    """
    Gera um relatório Markdown com caracterização do dataset (S01).
    """

    def _read_dicts(self, path: Path) -> List[Dict[str, str]]:
        if not path.exists() or path.stat().st_size == 0:
            return []
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def generate(self) -> str:
        repos = self._read_dicts(RAW_DIR / "repositories.csv")
        issues = []
        pulls = []
        releases = []
        commits = []
        for p in RAW_DIR.glob("issues_*.csv"): issues.extend(self._read_dicts(p))
        for p in RAW_DIR.glob("pulls_*.csv"): pulls.extend(self._read_dicts(p))
        for p in RAW_DIR.glob("releases_*.csv"): releases.extend(self._read_dicts(p))
        for p in RAW_DIR.glob("commits_*.csv"): commits.extend(self._read_dicts(p))

        # Contagens e top-N
        def to_int(x):
            try: return int(x)
            except Exception: return 0
        stars = sorted([(r.get("full_name"), to_int(r.get("stargazers_count"))) for r in repos], key=lambda x: x[1], reverse=True)
        forks = sorted([(r.get("full_name"), to_int(r.get("forks_count"))) for r in repos], key=lambda x: x[1], reverse=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = OUTPUT_DIR / f"relatorio_lab04_s01_{ts}.md"
        lines: List[str] = []
        lines.append("# LABORATÓRIO 04 — Caracterização do Dataset (S01)\n")
        lines.append(f"Gerado em: {ts}\n")
        lines.append("## Resumo\n")
        lines.append(f"- Repositórios: {len(repos)}")
        lines.append(f"- Issues (amostra): {len(issues)}")
        lines.append(f"- Pull Requests (amostra): {len(pulls)}")
        lines.append(f"- Releases: {len(releases)}")
        lines.append(f"- Semanas de commits (soma linhas): {len(commits)}\n")

        lines.append("## Top 20 repositórios por stars\n")
        for name, s in stars[:20]:
            lines.append(f"- {name}: {s}")
        lines.append("")

        lines.append("## Top 20 repositórios por forks\n")
        for name, s in forks[:20]:
            lines.append(f"- {name}: {s}")
        lines.append("")

        # Métricas agregadas existentes
        metrics_file = BI_DIR / "metrics_repo.csv"
        if metrics_file.exists() and metrics_file.stat().st_size > 0:
            lines.append("## Métricas agregadas por repositório\n")
            lines.append(f"Arquivo: {metrics_file}\n")
            lines.append("Colunas principais: stargazers_count, forks_count, issues_count, pulls_closed_count, pulls_merged_count, releases_count, commits_52w_total, age_days, days_since_last_push\n")

        out.write_text("\n".join(lines), encoding="utf-8")
        return str(out)
