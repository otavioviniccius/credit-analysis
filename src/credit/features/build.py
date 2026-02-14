import pandas as pd
import numpy as np

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    
    out["comprometimento_renda"] = (out["gastos_mensais"] / out["renda_mensal"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    out["tem_divida"] = (out["dividas_ativas"] > 0).astype(int)
    out["ja_inadimplente"] = out["historico_inadimplencia"].astype(int)
    out["estabilidade_profissional"] = np.log1p(out["tempo_emprego_meses"])  # suaviza

    out["score_risco_interno"] = (
        0.45 * out["comprometimento_renda"]
        + 0.25 * np.log1p(out["dividas_ativas"]) / 12
        + 0.20 * (out["atrasos_anteriores"] / 10)
        +0.10 * out["ja_inadimplente"]
    ).clip(0, 2.5)
    
    return out