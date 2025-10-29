"""
Configurações do Lab04 — Dataset para BI a partir do GitHub
"""
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis do .env se existir; se não houver, tenta .env.example
def _load_env_files():
    # 1) .env no diretório do Lab 04 ou acima
    load_dotenv()
    # 2) fallback: .env.example no root do lab
    root = Path(__file__).resolve().parents[2]
    example = root / ".env.example"
    if not os.getenv("GITHUB_TOKEN") and example.exists():
        load_dotenv(dotenv_path=example, override=False)

_load_env_files()

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output"
DATA_DIR = OUTPUT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
BI_DIR = DATA_DIR / "bi"
PLOTS_DIR = OUTPUT_DIR / "plots"

@dataclass
class Config:
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    api_base: str = "https://api.github.com"
    sleep_seconds: float = 1.1  # conservador
    max_retries: int = 3
    retry_backoff: float = 2.0
    user_agent: str = "Lab04-BI/0.1"

    # filtros default para coleta
    language: str = "java"
    min_stars: int = 1000
    since: Optional[str] = None  # ISO yyyy-mm-dd
    top: int = 200

    def ensure_dirs(self) -> None:
        OUTPUT_DIR.mkdir(exist_ok=True)
        DATA_DIR.mkdir(exist_ok=True)
        RAW_DIR.mkdir(exist_ok=True)
        BI_DIR.mkdir(exist_ok=True)
        PLOTS_DIR.mkdir(exist_ok=True)
        # Arquivo .gitkeep para facilitar versionamento vazio
        for d in (RAW_DIR, BI_DIR, PLOTS_DIR):
            (d / ".gitkeep").touch(exist_ok=True)

    @property
    def has_token(self) -> bool:
        return bool(self.github_token)
