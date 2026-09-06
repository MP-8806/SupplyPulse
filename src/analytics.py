import pandas as pd

def load_data(base_path="data"):
    orders = pd.read_csv(f"{base_path}/orders.csv", parse_dates=["order_date","promised_date","delivery_date"])
    inventory = pd.read_csv(f"{base_path}/inventory.csv")
    orders["on_time"] = orders["delivery_date"] <= orders["promised_date"]
    orders["in_full"] = orders["delivered_qty"] >= orders["ordered_qty"]
    orders["otif"] = orders["on_time"] & orders["in_full"]
    orders["lead_time_days"] = (orders["delivery_date"] - orders["order_date"]).dt.days
    orders["fill_rate"] = orders["delivered_qty"] / orders["ordered_qty"]
    return orders, inventory

def kpis(orders, inventory):
    return {
        "OTIF %": round(orders["otif"].mean()*100, 1),
        "Fill Rate %": round(orders["fill_rate"].mean()*100, 1),
        "Avg Lead Time": round(orders["lead_time_days"].mean(), 1),
        "At-Risk SKUs": int((inventory["current_stock"] < inventory["reorder_point"]).sum())
    }

def exceptions(orders, inventory):
    late = orders[~orders["on_time"]].copy()
    short = orders[~orders["in_full"]].copy()
    low = inventory[inventory["current_stock"] < inventory["reorder_point"]].copy()
    late["exception"] = "Late Delivery"
    short["exception"] = "Short Delivery"
    return late, short, low
