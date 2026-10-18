
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sales Data Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analytics Dashboard")
st.write("Analyze sales performance and discover business insights.")

df = pd.read_csv("sales_data.csv")

df["Revenue"] = df["Quantity"] * df["Price"]

# Key metrics
total_revenue = df["Revenue"].sum()
total_orders = len(df)
average_revenue = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Revenue", f"₹{average_revenue:,.2f}")

st.divider()

st.subheader("Sales Data")
st.dataframe(df, use_container_width=True)

# Product analysis
revenue_by_product = df.groupby("Product")["Revenue"].sum()
quantity_by_product = df.groupby("Product")["Quantity"].sum()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")
    st.bar_chart(revenue_by_product)

with col2:
    st.subheader("Quantity Sold by Product")
    st.bar_chart(quantity_by_product)



st.subheader("Revenue Contribution")

# Sort products from highest revenue to lowest
revenue_by_product = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

BG_COLOR = "#0B1F3A"
TEXT_COLOR = "#FFFFFF"

fig, ax = plt.subplots(figsize=(5, 3))
fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

colors = [
    "#38BDF8", "#A78BFA", "#34D399",
    "#FBBF24", "#FB7185", "#F97316",
    "#2DD4BF", "#818CF8", "#F472B6",
    "#A3E635"
]

wedges, _ = ax.pie(
    revenue_by_product,
    startangle=90,
    radius=0.42,
    colors=[
        colors[i % len(colors)]
        for i in range(len(revenue_by_product))
    ],
    wedgeprops={
        "edgecolor": BG_COLOR,
        "linewidth": 2
    }
)

total = revenue_by_product.sum()

legend_labels = [
    f"{product}: {value / total * 100:.1f}%"
    for product, value in revenue_by_product.items()
] if total > 0 else list(revenue_by_product.index)

legend = ax.legend(
    wedges,
    legend_labels,
    title="Revenue (Highest to Lowest)",
    loc="center left",
    bbox_to_anchor=(0.85, 0.5),
    frameon=False,
    fontsize=8,
    labelspacing=0.8
)

legend.get_title().set_color("#38BDF8")

for txt in legend.get_texts():
    txt.set_color(TEXT_COLOR)

ax.set_title(
    "Revenue Contribution by Product",
    color=TEXT_COLOR,
    fontsize=11,
    fontweight="bold"
)

ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.5)

st.pyplot(fig, use_container_width=False)
plt.close(fig)

# Show exact ranking in a table too
st.subheader("Product Revenue Ranking")

ranking = revenue_by_product.rename("Total Revenue").reset_index()
ranking.index = ranking.index + 1
ranking.index.name = "Rank"

st.dataframe(ranking, use_container_width=True)



# Business insights
st.subheader("💡 Business Insights")

if not df.empty:
    st.write(
        "**Best-selling product:**",
        quantity_by_product.idxmax()
    )
    st.write(
        "**Highest-revenue product:**",
        revenue_by_product.idxmax()
    )
    st.write(
        "**Lowest-revenue product:**",
        revenue_by_product.idxmin()
    )
