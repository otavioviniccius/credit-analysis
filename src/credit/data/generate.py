from __future__ import annotations
import numpy as np
import pandas as pd


def _clip(a, lo=None, hi=None):
    if lo is not None:
        a = np.maximum(a, lo)
    if hi is not None:
        a = np.minimum(a, hi)
    return a



def generate_synthetic(n: int = 50_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    
    idade = rng.integers(18, 75, size=n)
    estado_civil = rng.choice(["solteiro", "casado", "divorciado", "viuvo"], size=n, p=[0.45, 0.42, 0.10, 0.03])
    escolaridade = rng.choice(["fundamental", "medio", "superior", "pos"], size=n, p=[0.12, 0.45, 0.33, 0.10])
    profissao = rng.choice(["clt", "pj", "autonomo", "estudante", "desempregado"], size=n, p=[0.55, 0.15, 0.18, 0.07, 0.05])
    
    tempo_emprego_meses = rng.gamma(shape=2.0, scale=24.0, size=n)
    tempo_emprego_meses = _clip(tempo_emprego_meses, 0, 480).astype(int)
    
    renda_mensal = rng.lognormal(mean=8.3, sigma=0.55, size=n)
    renda_mensal = _clip(renda_mensal, 900, 80_000)
    
    gastos_base = renda_mensal * rng.uniform(0.35, 0.95, size=n)
    gastos_mensais = _clip(gastos_base + rng.normal(0, 300, size=n), 0 , None)
    
    prop_divida = 1 / (1 + np.exp(-(0.8*(gastos_mensais/renda_mensal) - 0.6)))
    tem_divida = rng.binomial(1, _clip(prop_divida, 0.05, 0.85))
    dividas_ativas = tem_divida * rng.lognormal(mean=7.6, sigma=0.9, size=n)
    dividas_ativas = _clip(dividas_ativas, 0 , 250_000)
    
    atrasos_anteriores = rng.poisson(lam=_clip(2.5*tem_divida + 1.5*(gastos_mensais/renda_mensal), 0.1, 6), size=n)
    atrasos_anteriores = _clip(atrasos_anteriores, 0, 24).astype(int)
    
    pct_renda_comprometida = _clip(gastos_mensais / renda_mensal, 0, 2.5)
    
    score_credito = (
        780
        - 22 *atrasos_anteriores
        - 0.0009 * dividas_ativas
        - 140 * (pct_renda_comprometida > 0.85).astype(int)
        + 0.18 * tempo_emprego_meses
        + rng.normal(0, 40, size=n)
    )
    score_credito = _clip(score_credito, 300, 900).astype(int)
    
    historico_inadimplencia = (atrasos_anteriores >= 5).astype(int)
    
    logit = (
        + 3.2 * (pct_renda_comprometida - 0.55)
        + 0.9 * np.log1p(dividas_ativas) / 10
        + 0.25 * atrasos_anteriores
        - 0.006 * (score_credito - 600)
        - 0.003 * tempo_emprego_meses
        + 0.8 * (profissao == "desempregado").astype(int)
        + 0.4 * (profissao == "autonomo").astype(int)
        + rng.normal(0, 0.35, size=n)
    )
    pd_inad = 1 / (1 + np.exp(-logit))
    inadimplente = rng.binomial(1, _clip(pd_inad, 0.01, 0.95))

    df = pd.DataFrame({
        "idade": idade,
        "estado_civil": estado_civil,
        "escolaridade": escolaridade,
        "profissao": profissao,
        "tempo_emprego_meses": tempo_emprego_meses,
        "renda_mensal": renda_mensal.round(2),
        "gastos_mensais": gastos_mensais.round(2),
        "dividas_ativas": dividas_ativas.round(2),
        "score_credito": score_credito,
        "historico_inadimplencia": historico_inadimplencia,
        "atrasos_anteriores": atrasos_anteriores,
        "pct_renda_comprometida": pct_renda_comprometida.round(4),
        "inadimplente": inadimplente,
    })
    return df
