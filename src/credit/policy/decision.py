# src/credit/policy/decision.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DecisionResult:
    status: str  # "APROVADO" | "RESTRITO" | "NEGADO"
    pd: float
    reason: str

def decide(pd: float, score_credito: int, pct_comp: float, atrasos: int, ja_inadimplente: int) -> DecisionResult:
    # Hard rules (negação)
    if pd >= 0.55:
        return DecisionResult("NEGADO", pd, "Risco elevado (PD >= 0.55)")
    if ja_inadimplente == 1 and atrasos >= 6:
        return DecisionResult("NEGADO", pd, "Histórico de inadimplência com muitos atrasos")
    if pct_comp > 0.95 and score_credito < 560:
        return DecisionResult("NEGADO", pd, "Comprometimento de renda crítico + score baixo")

    # Restrição
    if 0.35 <= pd < 0.55:
        return DecisionResult("RESTRITO", pd, "Risco moderado (0.35 <= PD < 0.55)")
    if score_credito < 550 or pct_comp > 0.85:
        return DecisionResult("RESTRITO", pd, "Score/comprometimento sugere limite conservador")

    return DecisionResult("APROVADO", pd, "Risco baixo e perfil consistente")
