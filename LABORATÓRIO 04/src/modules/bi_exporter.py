from __future__ import annotations
from typing import Dict, List
from pathlib import Path
import csv
from ..config.config import BI_DIR, RAW_DIR

class BIExporter:
    """
    Converte dados crus (RAW) em tabelas normalizadas para BI.
    Espera arquivos CSV em RAW_DIR: repositories.csv, issues_*.csv, pulls_*.csv, releases_*.csv, commits_*.csv
    """

    def __init__(self) -> None:
        BI_DIR.mkdir(exist_ok=True, parents=True)

    def export(self) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        # Repositórios (principal)
        repo_file = RAW_DIR / "repositories.csv"
        if repo_file.exists():
            # repositories
            outputs["repositories"] = self._copy(repo_file, "repositories.csv")
            # owners
            owners = {}
            rows = self._read_dicts(repo_file)
            for r in rows:
                login = r.get("owner_login")
                if login:
                    owners[login] = {"login": login, "type": r.get("owner_type")}
            if owners:
                self._write_dicts(list(owners.values()), BI_DIR / "owners.csv")
                outputs["owners"] = str(BI_DIR / "owners.csv")
            # topics
            topics_rows: List[Dict[str, str]] = []
            for r in rows:
                topics = r.get("topics") or ""
                if topics:
                    for t in str(topics).split(","):
                        t = t.strip()
                        if t:
                            topics_rows.append({"repo_full_name": r.get("full_name"), "topic": t})
            if topics_rows:
                self._write_dicts(topics_rows, BI_DIR / "topics.csv")
                outputs["topics"] = str(BI_DIR / "topics.csv")

        # Concat issues/pulls/releases/commits
        outputs.update(self._merge_pattern("issues_", "issues.csv"))
        outputs.update(self._merge_pattern("pulls_", "pulls.csv"))
        outputs.update(self._merge_pattern("releases_", "releases.csv"))
        outputs.update(self._merge_pattern("commits_", "commits_weekly.csv"))
        outputs.update(self._merge_pattern("languages_", "languages.csv"))
        return outputs

    def _merge_pattern(self, prefix: str, outname: str) -> Dict[str, str]:
        files = sorted(RAW_DIR.glob(f"{prefix}*.csv"))
        if not files:
            return {}
        # Concatenar manualmente e remover duplicatas simples por tuplas
        seen = set()
        out_path = BI_DIR / outname
        header_written = False
        with out_path.open("w", encoding="utf-8", newline="") as f_out:
            writer = None
            for f in files:
                for i, row in enumerate(self._read_dicts(f)):
                    key = tuple(sorted(row.items()))
                    if key in seen:
                        continue
                    seen.add(key)
                    if writer is None:
                        writer = csv.DictWriter(f_out, fieldnames=list(row.keys()))
                        writer.writeheader()
                        header_written = True
                    writer.writerow(row)
        return {outname.split(".")[0]: str(out_path)}

    def _copy(self, src: Path, name: str) -> str:
        dst = BI_DIR / name
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return str(dst)

    def _read_dicts(self, path: Path | str) -> List[Dict[str, str]]:
        p = Path(path)
        if not p.exists() or p.stat().st_size == 0:
            return []
        with p.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _write_dicts(self, rows: List[Dict[str, str]], path: Path) -> None:
        if not rows:
            path.write_text("")
            return
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
