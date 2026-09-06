import streamlit as st
import plotly.express as px
from analytics import load_data, kpis, exceptions

st.set_page_config(page_title="SupplyPulse", layout="wide")
st.title("📦 SupplyPulse")
st.caption("Supply Excellence KPI & Exception Monitor")

orders, inventory = load_data()
supplier_filter = st.sidebar.multiselect("Supplier", sorted(orders.supplier.unique()), default=sorted(orders.supplier.unique()))
orders = orders[orders.supplier.isin(supplier_filter)]

m = kpis(orders, inventory)
cols = st.columns(4)
for c, (name, value) in zip(cols, m.items()):
    c.metric(name, value)

st.divider()
left, right = st.columns(2)
with left:
    supplier = orders.groupby("supplier", as_index=False).agg(
        OTIF=("otif","mean"), Fill_Rate=("fill_rate","mean"), Orders=("order_id","count")
    )
    supplier["OTIF"] *= 100
    supplier["Fill_Rate"] *= 100
    st.subheader("Supplier Performance")
    st.dataframe(supplier.sort_values("OTIF"), use_container_width=True)
with right:
    st.subheader("Lead Time Distribution")
    st.plotly_chart(px.histogram(orders, x="lead_time_days", nbins=15, title="Delivery Lead Time (days)"), use_container_width=True)

late, short, low = exceptions(orders, inventory)
st.subheader("⚠️ Exceptions")
tabs = st.tabs(["Late Deliveries", "Short Deliveries", "Low Inventory"])
with tabs[0]: st.dataframe(late[["order_id","supplier","product","promised_date","delivery_date"]], use_container_width=True)
with tabs[1]: st.dataframe(short[["order_id","supplier","product","ordered_qty","delivered_qty","fill_rate"]], use_container_width=True)
with tabs[2]: st.dataframe(low, use_container_width=True)
