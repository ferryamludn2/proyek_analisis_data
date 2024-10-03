import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

orders = pd.read_csv('data/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')

st.title("E-commerce Data Analysis")
st.subheader("Sample Data from Each Dataset")
st.write("Orders Dataset")
st.dataframe(orders.head())
st.write("Order Items Dataset")
st.dataframe(order_items.head())
st.write("Payments Dataset")
st.dataframe(payments.head())
st.write("Products Dataset")
st.dataframe(products.head())

st.subheader("Missing Values Check")
st.write("Orders Dataset")
st.write(orders.isnull().sum())
st.write("Order Items Dataset")
st.write(order_items.isnull().sum())
st.write("Payments Dataset")
st.write(payments.isnull().sum())
st.write("Products Dataset")
st.write(products.isnull().sum())

orders = orders.dropna()
order_items = order_items.dropna()
payments = payments.dropna()
products = products.dropna()

st.subheader("Orders Dataset Columns")
st.write(orders.columns)

st.subheader("Distribution of Orders by Order Status")
plt.figure(figsize=(12, 6))
status_distribution = orders['order_status'].value_counts()
status_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of Orders by Order Status')
plt.xlabel('Order Status')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
st.pyplot(plt)

merged_data = order_items.merge(products, on='product_id').merge(orders, on='order_id')

avg_order_value = merged_data.groupby('product_category_name')['price'].mean().sort_values()

st.subheader("Average Order Value by Product Category")
plt.figure(figsize=(12, 8))
sns.barplot(x=avg_order_value, y=avg_order_value.index, palette='viridis')
plt.title('Average Order Value by Product Category', fontsize=16, fontweight='bold')
plt.xlabel('Average Value (R$)', fontsize=14)
plt.ylabel('Product Category', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
for index, value in enumerate(avg_order_value):
    plt.text(value, index, f'{value:.2f}', va='center', fontsize=10, color='black')
plt.tight_layout()
st.pyplot(plt)

monthly_revenue = merged_data.groupby('order_id').agg({'price': 'sum'}).reset_index()
monthly_revenue = monthly_revenue.merge(orders[['order_id', 'order_approved_at']], on='order_id')
monthly_revenue['order_approved_at'] = pd.to_datetime(monthly_revenue['order_approved_at'])
monthly_revenue.set_index('order_approved_at', inplace=True)
monthly_revenue = monthly_revenue.resample('M').sum()

st.subheader("Monthly Revenue")
plt.figure(figsize=(12, 6))
monthly_revenue['price'].plot(color='orange')
plt.title('Monthly Revenue')
plt.xlabel('Date')
plt.ylabel('Revenue (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)

payment_methods = payments['payment_type'].value_counts()

st.subheader("Most Common Payment Methods")
plt.figure(figsize=(12, 6))
purple_palette = ['#6A0EAB', '#8A2BE2', '#9370DB', '#BA55D3', '#DA70D6']  
payment_methods.plot(kind='bar', color=purple_palette)
plt.title('Most Common Payment Methods', fontsize=16, fontweight='bold', color='#333333')
plt.xlabel('Payment Method', fontsize=14, fontweight='bold', color='#333333')
plt.ylabel('Number of Payments', fontsize=14, fontweight='bold', color='#333333')
plt.xticks(rotation=45, ha='right', fontsize=12)
max_payment_method = payment_methods.idxmax()
max_payment_value = payment_methods.max()
plt.bar(max_payment_method, max_payment_value, color='orange')
plt.text(x=max_payment_method, y=max_payment_value + 5, s=f'{max_payment_value}', ha='center', fontsize=12, color='black', fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(plt)
