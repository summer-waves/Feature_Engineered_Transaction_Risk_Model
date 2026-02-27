import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def add_risk_score(feat: pd.DataFrame) -> pd.DataFrame:
    cols_to_scale = [
        "txn_count",
        "total_amount",
        "amount_volatility",
        "fraud_rate",
    ]
    cols_to_scale = [c for c in cols_to_scale if c in feat.columns]

    scaler = MinMaxScaler()
    feat_scaled = feat.copy()
    feat_scaled[cols_to_scale] = scaler.fit_transform(feat[cols_to_scale])

    weights = {
        "txn_count": 0.2,
        "total_amount": 0.2,
        "amount_volatility": 0.3,
        "fraud_rate": 0.3,
    }

    feat_scaled["risk_score"] = sum(
        feat_scaled[col] * w for col, w in weights.items() if col in feat_scaled.columns
    )

    return feat_scaled