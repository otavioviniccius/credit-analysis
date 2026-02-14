# src/credit/schema.py
from __future__ import annotations
from pydantic import BaseModel, Field, conint, confloat

class ClientInput(BaseModel):
    idade: conint(ge=18, le=100)
    estado_civil: str
    escolaridade: str
    profissao: str
    tempo_emprego_meses: conint(ge=0, le=600)

    renda_mensal: confloat(gt=0)
    gastos_mensais: confloat(ge=0)
    dividas_ativas: confloat(ge=0)
    score_credito: conint(ge=300, le=900)
    historico_inadimplencia: conint(ge=0, le=1)

    atrasos_anteriores: conint(ge=0, le=60)
    pct_renda_comprometida: confloat(ge=0)

class CreditOutput(BaseModel):
    status: str
    limite: float
    pd_inadimplencia: float = Field(..., ge=0, le=1)
    motivo: str
