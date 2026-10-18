
import pandas as pd

df = pd.read_csv("sales_data.csv")

df["Revenue"] = df["Quantity"] * df["Price"]

print(df)
print("Total Revenue:", df["Revenue"].sum())
print(df[["Product", "Quantity", "Price", "Revenue"]])

print(df.groupby("Product")["Quantity"].sum().sort_values(ascending=False))

print(df.groupby("Product")["Revenue"].sum().sort_values(ascending=False))

total_revenue = df["Revenue"].sum()
total_orders = len(df)

average_revenue = total_revenue / total_orders

print("Total Orders:", total_orders)
print("Average Revenue per Order:", average_revenue)

import matplotlib.pyplot as plt

revenue_by_product = df.groupby("Product")["Revenue"].sum()

revenue_by_product.plot(kind="bar")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Product-wise Quantity Chart

quantity_by_product = df.groupby("Product")["Quantity"].sum()

quantity_by_product.plot(kind="bar")

plt.title("Quantity Sold by Product")
plt.xlabel("Product")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Revenue Contribution Pie Chart

revenue_by_product = df.groupby("Product")["Revenue"].sum()

revenue_by_product.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Revenue Contribution by Product")
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


