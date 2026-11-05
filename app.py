from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from analytics import prepare_sales, metrics

st.set_page_config(page_title="Sales Insights", layout="wide")
st.title("Sales Insights Dashboard")
st.caption("Explore revenue, profit and product performance using sample or uploaded CSV data.")
upload = st.file_uploader("Upload sales CSV", type="csv")
try:
    raw = pd.read_csv(upload if upload is not None else Path(__file__).parent / "data" / "sample_sales.csv")
    sales = prepare_sales(raw)
except (ValueError, pd.errors.ParserError) as exc:
    st.error(str(exc))
    st.stop()
regions = st.multiselect("Regions", sorted(sales.region.unique()), default=sorted(sales.region.unique()))
categories = st.multiselect("Categories", sorted(sales.category.unique()), default=sorted(sales.category.unique()))
filtered = sales[sales.region.isin(regions) & sales.category.isin(categories)]
if filtered.empty:
    st.info("No sales match these filters.")
    st.stop()
k = metrics(filtered)
a,b,c,d = st.columns(4)
a.metric("Revenue", f"${k['revenue']:,.2f}")
b.metric("Profit", f"${k['profit']:,.2f}")
c.metric("Units sold", f"{k['units']:,}")
d.metric("Profit margin", f"{k['margin']:.1f}%")
monthly = filtered.assign(month=filtered.date.dt.to_period('M').astype(str)).groupby('month', as_index=False)[['revenue','profit']].sum()
st.plotly_chart(px.line(monthly, x='month', y=['revenue','profit'], markers=True, title='Monthly performance'), use_container_width=True)
left,right = st.columns(2)
with left:
    by_category = filtered.groupby('category', as_index=False).revenue.sum()
    st.plotly_chart(px.bar(by_category, x='category', y='revenue', title='Revenue by category'), use_container_width=True)
with right:
    by_product = filtered.groupby('product', as_index=False).revenue.sum().sort_values('revenue', ascending=False).head(10)
    st.plotly_chart(px.bar(by_product, x='product', y='revenue', title='Top products'), use_container_width=True)
st.subheader('Filtered records')
st.dataframe(filtered, use_container_width=True)
st.download_button('Export filtered data', filtered.to_csv(index=False), file_name='filtered_sales.csv', mime='text/csv')
