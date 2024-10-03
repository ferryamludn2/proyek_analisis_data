import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load datasets
orders = pd.read_csv('../data/olist_orders_dataset.csv')
order_items = pd.read_csv('../data/olist_order_items_dataset.csv')
payments = pd.read_csv('../data/olist_order_payments_dataset.csv')
products = pd.read_csv('../data/olist_products_dataset.csv')

# Display sample data
st.title('Data Analysis Dashboard')
st.text("E-Commerce Public Dataset ")
st.text("by Ferry Amaludin")
st.subheader('Sample Data from Orders')
st.write(orders.head())

# Check for missing values
st.subheader('Missing Values in Datasets')
st.write(orders.isnull().sum())
st.write(order_items.isnull().sum())
st.write(payments.isnull().sum())
st.write(products.isnull().sum())

# Drop missing values
orders.dropna(inplace=True)
order_items.dropna(inplace=True)
payments.dropna(inplace=True)
products.dropna(inplace=True)

# Visualize order status distribution
st.subheader('Order Status Distribution')
plt.figure(figsize=(12, 6))
status_distribution = orders['order_status'].value_counts()
status_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribusi Pesanan Menurut Status Pesanan')
plt.xlabel('Status Pesanan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Merge data
merged_data = order_items.merge(products, on='product_id').merge(orders, on='order_id')

# Calculate average order value by product category
avg_order_value = merged_data.groupby('product_category_name')['price'].mean().sort_values()

# Visualize average order value by product category
st.subheader('Nilai Pesanan Rata-rata Berdasarkan Kategori Produk')
plt.figure(figsize=(12, 8))
sns.barplot(x=avg_order_value, y=avg_order_value.index, palette='viridis')
plt.title('Nilai Pesanan Rata-rata Berdasarkan Kategori Produk', fontsize=16, fontweight='bold')
plt.xlabel('Nilai Rata-rata (R$)', fontsize=14)
plt.ylabel('Kategori Produk', fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
for index, value in enumerate(avg_order_value):
    plt.text(value, index, f'{value:.2f}', va='center', fontsize=10, color='black')
plt.tight_layout()
st.pyplot(plt)

# Monthly revenue calculation
monthly_revenue = merged_data.groupby('order_id').agg({'price': 'sum'}).reset_index()
monthly_revenue = monthly_revenue.merge(orders[['order_id', 'order_approved_at']], on='order_id')
monthly_revenue['order_approved_at'] = pd.to_datetime(monthly_revenue['order_approved_at'])
monthly_revenue.set_index('order_approved_at', inplace=True)
monthly_revenue = monthly_revenue.resample('M').sum()

# Visualize monthly revenue
st.subheader('Pendapatan Bulanan')
plt.figure(figsize=(12, 6))
monthly_revenue['price'].plot(color='orange')
plt.title('Pendapatan Bulanan', fontsize=16, fontweight='bold')
plt.xlabel('Tanggal', fontsize=14)
plt.ylabel('Pendapatan (R$)', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)

# Payment methods visualization
st.subheader('Metode Pembayaran Paling Umum')
payment_methods = payments['payment_type'].value_counts()
plt.figure(figsize=(12, 6))
purple_palette = ['#6A0EAB', '#8A2BE2', '#9370DB', '#BA55D3', '#DA70D6']
payment_methods.plot(kind='bar', color=purple_palette)
plt.title('Metode Pembayaran Paling Umum', fontsize=16, fontweight='bold', color='#333333')
plt.xlabel('Metode Pembayaran', fontsize=14, fontweight='bold', color='#333333')
plt.ylabel('Jumlah Pembayaran', fontsize=14, fontweight='bold', color='#333333')
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.tight_layout()
st.pyplot(plt)

# RFM Analysis
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['last_purchase_date'] = orders['order_approved_at'].max() - orders['order_approved_at']
orders['recency'] = orders['last_purchase_date'].dt.days
frequency = orders['customer_id'].value_counts()

monetary = merged_data.groupby('customer_id')['price'].sum()

# Create RFM DataFrame
rfm = pd.DataFrame({
    'recency': orders.groupby('customer_id')['recency'].min(),
    'frequency': frequency,
    'monetary': monetary
}).reset_index()

# Display RFM DataFrame
st.subheader('RFM DataFrame')
st.write(rfm.head())
