# SupplyPulse — Supply Chain KPI & Exception Monitor

A lightweight supply-excellence analytics project that monitors orders, shipments and inventory, calculates operational KPIs, and flags exceptions requiring attention.

## Features
- OTIF (On-Time In-Full) calculation
- Average delivery lead time
- Fill rate and inventory health
- Supplier performance summary
- Automated exception detection
- Interactive Streamlit dashboard
- Synthetic operational dataset for reproducible demonstration

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python src/generate_data.py
streamlit run src/app.py
```

## KPIs
- **OTIF:** orders delivered on/before promised date and with full quantity
- **Fill Rate:** delivered quantity / ordered quantity
- **Average Lead Time:** delivery date - order date
- **Inventory Coverage:** current stock / average daily demand

This project uses synthetic data and is intended for portfolio/demo purposes.
