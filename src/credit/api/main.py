# src/credit/api/main.py
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from credit.schema import ClientInput, CreditOutput
from credit.models.predict import CreditModel
from credit.policy.decision import decide
from credit.policy.limit import compute_limit

app = FastAPI(title="Credit Approval API", version="1.0.0")
model = CreditModel()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/credit/decision", response_model=CreditOutput)
def credit_decision(client: ClientInput):
    data = client.model_dump()

    # consistência mínima (regra “anti-lixo”)
    if data["gastos_mensais"] > data["renda_mensal"] * 2.5:
        raise HTTPException(status_code=422, detail="gastos_mensais muito acima da renda_mensal")

    pd = model.predict_pd(data)
    decision = decide(
        pd=pd,
        score_credito=data["score_credito"],
        pct_comp=data["pct_renda_comprometida"],
        atrasos=data["atrasos_anteriores"],
        ja_inadimplente=data["historico_inadimplencia"],
    )
    limit = compute_limit(
        renda_mensal=data["renda_mensal"],
        pd=pd,
        pct_comp=data["pct_renda_comprometida"],
        tempo_emprego_meses=data["tempo_emprego_meses"],
        status=decision.status,
    )

    return CreditOutput(
        status=decision.status,
        limite=limit,
        pd_inadimplencia=pd,
        motivo=decision.reason
    )
