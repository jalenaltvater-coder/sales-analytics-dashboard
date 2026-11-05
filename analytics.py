import pandas as pd

REQUIRED = {"date", "region", "category", "product", "quantity", "unit_price", "unit_cost"}

def prepare_sales(data: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    df = data.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ("quantity", "unit_price", "unit_cost"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "quantity", "unit_price", "unit_cost"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] >= 0) & (df["unit_cost"] >= 0)]
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["profit"] = df["quantity"] * (df["unit_price"] - df["unit_cost"])
    return df

def metrics(df: pd.DataFrame) -> dict:
    revenue = float(df["revenue"].sum())
    profit = float(df["profit"].sum())
    return {"revenue": revenue, "profit": profit, "units": int(df["quantity"].sum()),
            "margin": profit / revenue * 100 if revenue else 0.0}
