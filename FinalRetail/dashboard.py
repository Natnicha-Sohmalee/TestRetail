import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

# ---- การอ่านข้อมูลจาก CSV ----
data = pd.read_csv('sales_data.csv')

# ---- การตั้งค่าและแสดงชื่อหัวข้อ Dashboard ----
st.title('Sales Dashboard')

# ---- ข้อมูลสรุปการขาย (KPI) ----
st.header("Key Performance Indicators (KPI)")
total_sales = data['Total Amount'].sum()
avg_sales = data['Total Amount'].mean()
max_sales = data['Total Amount'].max()
min_sales = data['Total Amount'].min()

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Average Sales", f"${avg_sales:,.2f}")
st.metric("Max Sales", f"${max_sales:,.2f}")

# ---- การแสดงข้อมูลสรุป (Summary Statistics) ----
st.header('Sales Summary')
st.write(f"Total Sales: ${total_sales:,.2f}")
st.write(f"Average Sales: ${avg_sales:,.2f}")
st.write(f"Max Sales: ${max_sales:,.2f}")
st.write(f"Min Sales: ${min_sales:,.2f}")

# ---- การแปลงข้อมูลและการจัดเรียง ----
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.sort_values(by='Date')
data['Year_Month'] = data['Date'].dt.to_period('M')
data['Year_Month'] = data['Year_Month'].dt.to_timestamp()

# ---- ตัวเลือกกรองข้อมูล ----
selected_year = st.selectbox('Select Year', data['Date'].dt.year.unique())
filtered_data = data[data['Date'].dt.year == selected_year]
st.write(filtered_data)

# ---- แสดงข้อมูลตารางดิบ (Raw Data Table) ----
st.header("Raw Data Table")
st.write(data)  # แสดงข้อมูลทั้งหมด

# ---- การแสดงข้อมูลยอดขายรายเดือน ----
monthly_sales2 = data.groupby(['Year_Month'])['Total Amount'].sum().reset_index()

st.header("Monthly Total Amount")
st.write(monthly_sales2)

# ---- การแสดงกราฟ Sales Trend by Month ----
fig_sales_trend = px.line(monthly_sales2, x='Year_Month', y='Total Amount', title='Sales Trend by Month', markers=True)
st.header("Sales Trend by Month (Interactive Line Chart)")
st.plotly_chart(fig_sales_trend, key="sales_trend_line_chart")

# ---- Best Selling Products (สินค้าที่ขายดีที่สุด) ----
best_selling_products = data.groupby('Product Category')['Quantity'].sum().sort_values(ascending=False)

st.header("Best Selling Products")
st.write(best_selling_products)

# ---- การแสดงกราฟ Best Selling Products ----
# 1. Seaborn Bar Plot
fig_seaborn, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=best_selling_products.index, y=best_selling_products.values, ax=ax, palette='Blues_d')
ax.set_title('Best Selling Products')
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Quantity Sold')
ax.tick_params(axis='x', rotation=45)

# Convert Seaborn figure to base64 for embedding in Streamlit
img_stream_seaborn = BytesIO()
fig_seaborn.savefig(img_stream_seaborn, format='png')
img_stream_seaborn.seek(0)
img_base64_seaborn = base64.b64encode(img_stream_seaborn.getvalue()).decode()

st.header("Best Selling Products (Seaborn Bar Plot)")
st.image(img_stream_seaborn, caption='Best Selling Products (Seaborn Bar Plot)', use_container_width=True)

# 2. Plotly Pie Chart
fig_pie = px.pie(names=best_selling_products.index, values=best_selling_products.values, title='Best Selling Products', color=best_selling_products.index)
st.header("Best Selling Products (Pie Chart)")
st.plotly_chart(fig_pie, key="best_selling_pie_chart")

# ---- การแสดง Sales Amount Distribution ----
fig_dist, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data['Total Amount'], kde=True, color='green', ax=ax)
ax.set_title('Sales Amount Distribution')
ax.set_xlabel('Total Amount')
ax.set_ylabel('Frequency')

# Convert Seaborn distribution figure to base64 for embedding in Streamlit
img_stream_dist = BytesIO()
fig_dist.savefig(img_stream_dist, format='png')
img_stream_dist.seek(0)
img_base64_dist = base64.b64encode(img_stream_dist.getvalue()).decode()

st.header("Sales Amount Distribution (Seaborn Histogram)")
st.image(img_stream_dist, caption='Sales Amount Distribution (Seaborn)', use_container_width=True)

# ---- การดาวน์โหลดรายงาน CSV ----
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(monthly_sales2)
st.download_button("Download Monthly Sales Data", csv_data, file_name="monthly_sales.csv", mime="text/csv")

# ---- การแสดงกราฟ Scatter Plot ----
fig_scatter = px.scatter(data, x='Quantity', y='Total Amount', title='Quantity vs Sales Amount')
st.plotly_chart(fig_scatter)

# ---- การแสดง Heatmap ----
# สร้าง pivot table โดยใช้ Product Category เป็นแถว และ Year-Month เป็นคอลัมน์
pivot_data = data.pivot_table(index='Product Category', columns='Year_Month', values='Total Amount', aggfunc='sum')
pivot_data = pivot_data.fillna(0)

fig_heatmap, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pivot_data, annot=True, cmap='YlGnBu', fmt='.1f', ax=ax, linewidths=.5)
ax.set_title('Sales Heatmap by Product Category and Year-Month')

st.pyplot(fig_heatmap)

# ---- การแสดงข้อมูลตามช่วงเวลา (Date Range Filter) ----
start_date = pd.to_datetime(st.date_input('Start Date', min_value=data['Date'].min(), max_value=data['Date'].max()))
end_date = pd.to_datetime(st.date_input('End Date', min_value=start_date, max_value=data['Date'].max()))

# กรองข้อมูลตามวันที่
filtered_data_by_date = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
st.write(filtered_data_by_date)

# ---- การแสดง Box Plot หรือ Violin Plot ----
fig_box, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x=data['Product Category'], y=data['Total Amount'], ax=ax)
ax.set_title('Sales Distribution by Product Category')
st.pyplot(fig_box)

# ---- การกรองข้อมูลตามหมวดหมู่สินค้า ----
selected_category = st.selectbox('Select Product Category', data['Product Category'].unique())
filtered_category_data = data[data['Product Category'] == selected_category]
st.write(filtered_category_data)

# ---- การแสดงข้อมูลการแบ่งกลุ่มตาม Gender ----
gender_segmentation = data.groupby('Gender')['Total Amount'].sum().reset_index()
fig_segmentation = px.pie(gender_segmentation, names='Gender', values='Total Amount', title='Sales by Gender')
st.plotly_chart(fig_segmentation)
