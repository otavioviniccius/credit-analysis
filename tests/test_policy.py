from credit.policy.decision import decide
from credit.policy.limit import compute_limit

def test_denied_high_pd():
    d = decide(pd=0.8, score_credito=700, pct_comp=0.4, atrasos=0, ja_inadimplente=0)
    assert d.status == "NEGADO"

def test_restricted_mid_pd():
    d = decide(pd=0.45, score_credito=650, pct_comp=0.5, atrasos=1, ja_inadimplente=0)
    assert d.status == "RESTRITO"

def test_limit_zero_when_denied():
    limit = compute_limit(renda_mensal=5000, pd=0.8, pct_comp=0.4, tempo_emprego_meses=36, status="NEGADO")
    assert limit == 0.0

def test_limit_positive_when_approved():
    limit = compute_limit(renda_mensal=5000, pd=0.1, pct_comp=0.5, tempo_emprego_meses=36, status="APROVADO")
    assert limit > 0
