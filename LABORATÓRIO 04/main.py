"""
LABORATÓRIO 04 — Pipeline de Coleta e Exportação para BI
"""
from __future__ import annotations
import argparse
import sys
from src.config.config import Config
from src.pipelines.bi_pipeline import BIPipeline


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Lab04 — Coleta de dados do GitHub e exportação para BI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_collect = sub.add_parser("collect", help="Coleta dados brutos (RAW)")
    p_collect.add_argument("--language", default=Config.language)
    p_collect.add_argument("--min-stars", type=int, default=Config.min_stars)
    p_collect.add_argument("--top", type=int, default=Config.top)
    p_collect.add_argument("--since", default=Config.since)

    p_export = sub.add_parser("export", help="Exporta tabelas normalizadas para BI")

    p_analyze = sub.add_parser("analyze", help="Gera métricas agregadas (metrics_repo.csv)")

    p_report = sub.add_parser("report", help="Gera um resumo descritivo simples e pronto para BI")
    p_report.add_argument("--out", default=str((Config.__dict__.get('__annotations__') and '') or 'output'))

    return p.parse_args()


def main():
    cfg = Config()
    cfg.ensure_dirs()

    if not cfg.has_token:
        print("[ERRO] GITHUB_TOKEN não configurado. Defina no ambiente ou em um arquivo .env.")
        sys.exit(1)

    args = parse_args()
    pipe = BIPipeline(cfg)

    if args.cmd == "collect":
        results = pipe.collect(args.language, args.min_stars, args.top, args.since)
        print("Arquivos RAW gerados:")
        for k, v in results.items():
            print(f"- {k}: {v}")

    elif args.cmd == "export":
        outs = pipe.export()
        print("Arquivos BI gerados:")
        for k, v in outs.items():
            print(f"- {k}: {v}")

    elif args.cmd == "analyze":
        from src.modules.aggregator import Aggregator
        agg = Aggregator()
        out = agg.compute()
        print(f"Métricas agregadas geradas: {out}")

    elif args.cmd == "report":
        from src.modules.aggregator import Aggregator
        from src.modules.report_generator import ReportGenerator
        agg = Aggregator()
        metrics_path = agg.compute()
        rep = ReportGenerator()
        md_path = rep.generate()
        print(f"Métricas agregadas: {metrics_path}")
        print(f"Relatório S01: {md_path}")


if __name__ == "__main__":
    main()
