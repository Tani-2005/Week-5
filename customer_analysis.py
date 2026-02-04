import pandas as pd
import matplotlib.pyplot as plt
import os

# --- STEP 1: DIRECTORY SETUP ---
output_dir = 'visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- STEP 2: DATA LOADING & CLEANING ---
# Using the files provided
sales_df = pd.read_csv('sales_data.csv')
customer_df = pd.read_csv('customer_data.csv')

# FIX: Added 'r' before strings to handle the regex \d properly (Raw Strings)
sales_df['join_id'] = sales_df['Customer_ID'].str.extract(r'(\d+)').astype(int)
customer_df['join_id'] = customer_df['CustomerID'].str.extract(r'(\d+)').astype(int)

# Datetime Transformation
sales_df['Date'] = pd.to_datetime(sales_df['Date'])
sales_df['Month'] = sales_df['Date'].dt.month_name()
sales_df['Month_Num'] = sales_df['Date'].dt.month
sales_df['Year'] = sales_df['Date'].dt.year

# --- STEP 3: MERGING & AGGREGATION ---
df = pd.merge(sales_df, customer_df, on='join_id', how='inner')

# Calculate Aggregations
top_customers = df.groupby('CustomerID')['Total_Sales'].sum().sort_values(ascending=False).head(10)
monthly_revenue = df.groupby(['Year', 'Month_Num', 'Month'])['Total_Sales'].sum().reset_index().sort_values(['Year', 'Month_Num'])

# --- STEP 4: ADVANCED SUMMARIZATION ---
pivot_summary = df.pivot_table(index='Region', columns='Product', values='Total_Sales', aggfunc='sum', fill_value=0)

# --- STEP 5: VISUALIZATION EXPORT ---

# 1. Top Customers Plot
plt.figure(figsize=(10, 6))
top_customers.plot(kind='barh', color='skyblue')
plt.title('Top 10 Customers by Total Sales')
plt.xlabel('Total Revenue ($)')
plt.ylabel('Customer ID')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/top_customers.png')
plt.close()

# 2. Monthly Sales Plot
plt.figure(figsize=(10, 6))
plt.plot(monthly_revenue['Month'], monthly_revenue['Total_Sales'], marker='o', linestyle='-', color='green', linewidth=2)
plt.title('Monthly Sales Performance')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(f'{output_dir}/monthly_sales.png')
plt.close()

# 3. Region & Product Sales (Stacked Bar)
pivot_summary.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Sales by Region and Product Category')
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{output_dir}/region_product_sales.png')
plt.close()

# --- STEP 6: SUMMARY REPORT ---
print("✅ Project Analysis Complete (Warnings Resolved).")
print(f"📁 Visualizations saved to: /{output_dir}")
print("-" * 40)
print(f"TOTAL REVENUE:       ${df['Total_Sales'].sum():,}")
print(f"TOTAL CUSTOMERS:     {df['CustomerID'].nunique()}")
print(f"AVG ORDER VALUE:     ${df['Total_Sales'].mean():,.2f}")
print(f"TOP CUSTOMER:        {top_customers.index[0]} (${top_customers.iloc[0]:,})")
print("-" * 40)
