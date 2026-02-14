# src/credit/policy/limit.py
from __future__ import annotations
import math

def compute_limit(
    renda_mensal: float,
    pd: float,
    pct_comp: float,
    tempo_emprego_meses: int,
    status: str,
) -> float:
    if status == "NEGADO":
        return 0.0

    base = 0.25 * renda_mensal  # 25% da renda
    risco_mult = max(0.25, 1.0 - pd)  # nunca zera totalmente
    comp_mult = 1.0 if pct_comp <= 0.65 else max(0.35, 1.0 - (pct_comp - 0.65) * 1.4)

    estabilidade_mult = 1.0 if tempo_emprego_meses >= 24 else 0.85
    if status == "RESTRITO":
        estabilidade_mult *= 0.85

    limit = base * risco_mult * comp_mult * estabilidade_mult

    # limites operacionais (exemplo)
    limit = max(limit, 300.0)          # mínimo
    limit = min(limit, 50_000.0)       # teto
    return float(math.floor(limit / 50) * 50)  # arredonda para múltiplos de 50
