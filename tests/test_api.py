from fastapi.testclient import TestClient
from credit.api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_decision_endpoint():
    payload = {
        "idade": 28,
        "estado_civil": "solteiro",
        "escolaridade": "superior",
        "profissao": "clt",
        "tempo_emprego_meses": 36,
        "renda_mensal": 6500,
        "gastos_mensais": 2800,
        "dividas_ativas": 12000,
        "score_credito": 680,
        "historico_inadimplencia": 0,
        "atrasos_anteriores": 1,
        "pct_renda_comprometida": 2800/6500,
    }
    r = client.post("/credit/decision", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "status" in body and "limite" in body and "pd_inadimplencia" in body
