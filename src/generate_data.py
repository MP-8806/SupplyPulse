from pathlib import Path
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

n = 500
suppliers = ["Alpha Components", "Beta Metals", "Gamma Packaging", "Delta Logistics", "Omega Parts"]
products = ["Raw Material A", "Raw Material B", "Packaging X", "Packaging Y", "Component Z"]

order_date = pd.Timestamp("2026-01-01") + pd.to_timedelta(RNG.integers(0, 210, n), unit="D")
promised_days = RNG.integers(3, 11, n)
delay = RNG.choice([0, 0, 0, 1, 2, 3, 5, 8], n, p=[.30,.20,.12,.12,.10,.08,.05,.03])
actual_days = promised_days + delay

ordered = RNG.integers(50, 600, n)
fill_pct = RNG.choice([1.0, 1.0, 1.0, .98, .95, .88, .75], n)
delivered = np.floor(ordered * fill_pct).astype(int)

df = pd.DataFrame({
    "order_id": [f"ORD-{i:04d}" for i in range(1, n+1)],
    "supplier": RNG.choice(suppliers, n),
    "product": RNG.choice(products, n),
    "order_date": order_date,
    "promised_date": order_date + pd.to_timedelta(promised_days, unit="D"),
    "delivery_date": order_date + pd.to_timedelta(actual_days, unit="D"),
    "ordered_qty": ordered,
    "delivered_qty": delivered,
    "unit_cost": np.round(RNG.uniform(8, 150, n), 2),
})
df["status"] = np.where(df["delivered_qty"] >= df["ordered_qty"], "Complete", "Short")
df.to_csv(DATA / "orders.csv", index=False)

inv = pd.DataFrame({
    "product": products,
    "current_stock": RNG.integers(300, 4000, len(products)),
    "avg_daily_demand": RNG.integers(80, 500, len(products)),
    "reorder_point": RNG.integers(250, 1200, len(products))
})
inv.to_csv(DATA / "inventory.csv", index=False)
print("Generated data/orders.csv and data/inventory.csv")
