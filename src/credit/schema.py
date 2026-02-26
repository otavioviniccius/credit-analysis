# src/credit/schema.py
from __future__ import annotations
import typing
from pydantic import BaseModel, Field, conint, confloat

class ClientInput(BaseModel):
    idade: typing.Annotated[int, Field(ge=18, le=100)]
    estado_civil: str
    escolaridade: str
    profissao: str
    tempo_emprego_meses: typing.Annotated[int, Field(ge=0, le=600)]

    renda_mensal: typing.Annotated[float, Field(gt=0)]
    gastos_mensais: typing.Annotated[float, Field(ge=0)]
    dividas_ativas: typing.Annotated[float, Field(ge=0)]
    score_credito: typing.Annotated[int, Field(ge=300, le=900)]
    historico_inadimplencia: typing.Annotated[int, Field(ge=0, le=1)]

    atrasos_anteriores: typing.Annotated[int, Field(ge=0, le=60)]
    pct_renda_comprometida: typing.Annotated[float, Field(ge=0)]

class CreditOutput(BaseModel):
    status: str
    limite: float
