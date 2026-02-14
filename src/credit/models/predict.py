# src/credit/models/predict.py
from __future__ import annotations
import joblib
import pandas as pd
from credit.features.build import add_features
from credit.models.train import NUM_COLS, CAT_COLS

class CreditModel:
    def __init__(self, model_path: str = "data/models/credit_model.joblib"):
        self.pipe = joblib.load(model_path)

    def predict_pd(self, payload: dict) -> float:
        df = pd.DataFrame([payload])
        df = add_features(df)
        X = df[NUM_COLS + CAT_COLS]
        return float(self.pipe.predict_proba(X)[:, 1][0])
