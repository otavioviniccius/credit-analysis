from __future__ import annotations

import joblib
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

from credit.features.build import add_features

NUM_COLS = [
    "idade", "tempo_emprego_meses", "renda_mensal", "gastos_mensais",
    "dividas_ativas", "score_credito", "atrasos_anteriores",
    "pct_renda_comprometida", "comprometimento_renda",
    "estabilidade_profissional", "score_risco_interno",
    "tem_divida", "ja_inadimplente",
]
CAT_COLS = ["estado_civil", "escolaridade", "profissao"]

def train(df: pd.DataFrame, out_dir: str = "data/models") -> dict:
    df = add_features(df)

    X = df[NUM_COLS + CAT_COLS]
    y = df["inadimplente"].astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    num_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    pre = ColumnTransformer(transformers=[
        ("num", num_pipe, NUM_COLS),
        ("cat", cat_pipe, CAT_COLS),
    ])

    model = LogisticRegression(max_iter=200, class_weight="balanced")

    pipe = Pipeline(steps=[
        ("pre", pre),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, proba)

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, f"{out_dir}/credit_model.joblib")

    # threshold inicial (você ajusta depois por política)
    meta = {"roc_auc_val": float(auc), "threshold": 0.35}
    with open(f"{out_dir}/meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return meta
