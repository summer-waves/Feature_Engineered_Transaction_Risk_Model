import pandas as pd

def build_origin_account_features(df: pd.DataFrame) -> pd.DataFrame:
    group_col = "nameOrig"
    agg = df.groupby(group_col).agg(
        txn_count=("amount", "count"),
        total_amount=("amount", "sum"),
        avg_amount=("amount", "mean"),
        std_amount=("amount", "std"),
        max_amount=("amount", "max"),
        min_amount=("amount", "min"),
        payment_ratio=("type", lambda x: (x == "PAYMENT").mean()),
        transfer_ratio=("type", lambda x: (x == "TRANSFER").mean()),
        cashout_ratio=("type", lambda x: (x == "CASH_OUT").mean()),
        debit_ratio=("type", lambda x: (x == "DEBIT").mean()),
        fraud_rate=("isFraud", "mean"),
    )
    agg["amount_volatility"] = agg["std_amount"] / agg["avg_amount"]
    return agg