
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset
df = pd.read_csv("sales_data.csv")

# Calculate Revenue
df["Revenue"] = df["Quantity"] * df["Price"]

print(df)
print("Total Revenue:", df["Revenue"].sum())
print(df[["Product", "Quantity", "Price", "Revenue"]])

# Product-wise Analysis
quantity_by_product = df.groupby("Product")["Quantity"].sum().sort_values(
    ascending=False
)

revenue_by_product = df.groupby("Product")["Revenue"].sum().sort_values(
    ascending=False
)

print("\nQuantity Sold by Product:")
print(quantity_by_product)

print("\nRevenue by Product:")
print(revenue_by_product)

# Overall Statistics
total_revenue = df["Revenue"].sum()
total_orders = len(df)
average_revenue = total_revenue / total_orders if total_orders else 0

print("\nTotal Orders:", total_orders)
print("Average Revenue per Order:", average_revenue)

# Chart 1: Revenue by Product
plt.figure(figsize=(10, 6), dpi=150)

revenue_by_product.plot(
    kind="bar",
    color="steelblue",
    edgecolor="black"
)

plt.title("Revenue by Product", fontsize=16, pad=15)
plt.xlabel("Product", fontsize=12)
plt.ylabel("Revenue (₹)", fontsize=12)
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# Chart 2: Quantity Sold by Product
plt.figure(figsize=(10, 6), dpi=150)

quantity_by_product.plot(
    kind="bar",
    color="seagreen",
    edgecolor="black"
)

plt.title("Quantity Sold by Product", fontsize=16, pad=15)
plt.xlabel("Product", fontsize=12)
plt.ylabel("Total Quantity Sold", fontsize=12)
plt.xticks(rotation=30, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# Chart 3: Revenue Contribution Pie Chart
plt.figure(figsize=(9, 7), dpi=150)

revenue_by_product.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    textprops={"fontsize": 12},
    wedgeprops={"edgecolor": "white", "linewidth": 1}
)

plt.title(
    "Revenue Contribution by Product",
    fontsize=16,
    pad=20
)

plt.ylabel("")
plt.tight_layout()
plt.show()

# Business Insights
total_revenue = df["Revenue"].sum()

best_selling_product = df.groupby("Product")["Quantity"].sum().idxmax()
highest_revenue_product = df.groupby("Product")["Revenue"].sum().idxmax()
lowest_revenue_product = df.groupby("Product")["Revenue"].sum().idxmin()

print("\n--- BUSINESS INSIGHTS ---")
print("Total Revenue:", total_revenue)
print("Best Selling Product:", best_selling_product)
print("Highest Revenue Product:", highest_revenue_product)
print("Lowest Revenue Product:", lowest_revenue_product)
