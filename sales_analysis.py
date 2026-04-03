import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("sales_data.csv")

# Quick look at the data
print("First 5 rows:")
print(df.head())

print("\nDataset size:", df.shape)
print("\nNull values:\n", df.isnull().sum())
print("\nBasic stats:\n", df.describe())

# Convert Date to proper format and extract month info
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# ---- KEY NUMBERS ----

total_revenue = df["Total_Sales"].sum()
avg_order = np.mean(df["Total_Sales"])

print(f"\nTotal Revenue: ₹{total_revenue:,}")
print(f"Average Order Value: ₹{avg_order:,.2f}")
print(f"Best Product (by quantity): {df.groupby('Product')['Quantity'].sum().idxmax()}")
print(f"Highest Revenue Product: {df.groupby('Product')['Total_Sales'].sum().idxmax()}")
print(f"Top Salesperson: {df.groupby('Salesperson')['Total_Sales'].sum().idxmax()}")
print(f"Best Region: {df.groupby('Region')['Total_Sales'].sum().idxmax()}")

print("\nCategory wise Revenue:\n", df.groupby("Category")["Total_Sales"].sum())
print("\nMonth wise Revenue:\n", df.groupby("Month_Name")["Total_Sales"].sum())

# ---- DASHBOARD ----

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle("Sales Data Analysis Dashboard", fontsize=20, fontweight="bold", y=0.98)

# Graph 1 - Monthly Sales Trend
month_order = ["January", "February", "March", "April", "May", "June"]
monthly_sales = df.groupby("Month_Name")["Total_Sales"].sum().reindex(month_order)

axes[0, 0].plot(monthly_sales.index, monthly_sales.values, marker="o", color="steelblue", linewidth=2.5, markersize=8)
axes[0, 0].set_title("Monthly Sales Trend", fontsize=14, fontweight="bold")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Total Sales (₹)")
axes[0, 0].tick_params(axis="x", rotation=45)
for i, val in enumerate(monthly_sales.values):
    axes[0, 0].annotate(f"₹{val//1000}K", (monthly_sales.index[i], val), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)

# Graph 2 - Product wise Revenue
product_revenue = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
sns.barplot(x=product_revenue.index, y=product_revenue.values, ax=axes[0, 1], palette="Blues_d")
axes[0, 1].set_title("Product Wise Revenue", fontsize=14, fontweight="bold")
axes[0, 1].set_xlabel("Product")
axes[0, 1].set_ylabel("Total Sales (₹)")
axes[0, 1].tick_params(axis="x", rotation=45)

# Graph 3 - Category Split (Pie Chart)
category_revenue = df.groupby("Category")["Total_Sales"].sum()
axes[1, 0].pie(category_revenue.values, labels=category_revenue.index, autopct="%1.1f%%",
               colors=["#4C72B0", "#DD8452"], startangle=90, textprops={"fontsize": 12})
axes[1, 0].set_title("Category Wise Revenue Split", fontsize=14, fontweight="bold")

# Graph 4 - Region wise Sales
region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
sns.barplot(x=region_sales.index, y=region_sales.values, ax=axes[1, 1], palette="Greens_d")
axes[1, 1].set_title("Region Wise Sales", fontsize=14, fontweight="bold")
axes[1, 1].set_xlabel("Region")
axes[1, 1].set_ylabel("Total Sales (₹)")

# Graph 5 - Salesperson Performance
sales_person = df.groupby("Salesperson")["Total_Sales"].sum().sort_values(ascending=False)
sns.barplot(x=sales_person.index, y=sales_person.values, ax=axes[2, 0], palette="Oranges_d")
axes[2, 0].set_title("Salesperson Performance", fontsize=14, fontweight="bold")
axes[2, 0].set_xlabel("Salesperson")
axes[2, 0].set_ylabel("Total Sales (₹)")

# Graph 6 - Top Products by Quantity
top_qty = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(5)
sns.barplot(x=top_qty.index, y=top_qty.values, ax=axes[2, 1], palette="Purples_d")
axes[2, 1].set_title("Top Products by Quantity Sold", fontsize=14, fontweight="bold")
axes[2, 1].set_xlabel("Product")
axes[2, 1].set_ylabel("Total Quantity")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nDashboard saved as sales_dashboard.png")

# ---- FINAL SUMMARY ----

print("\n" + "="*50)
print("         FINAL SALES SUMMARY REPORT")
print("="*50)
print(f"  Total Orders       : {len(df)}")
print(f"  Total Revenue      : ₹{df['Total_Sales'].sum():,}")
print(f"  Avg Order Value    : ₹{np.mean(df['Total_Sales']):,.2f}")
print(f"  Max Single Order   : ₹{df['Total_Sales'].max():,}")
print(f"  Min Single Order   : ₹{df['Total_Sales'].min():,}")
print(f"  Top Product        : {df.groupby('Product')['Total_Sales'].sum().idxmax()}")
print(f"  Top Region         : {df.groupby('Region')['Total_Sales'].sum().idxmax()}")
print(f"  Top Salesperson    : {df.groupby('Salesperson')['Total_Sales'].sum().idxmax()}")
print("="*50)