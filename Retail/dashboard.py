import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# แสดงหัวข้อ
st.title("Retail Sales Dashboard")
st.write("วิเคราะห์ข้อมูลยอดขายร้านค้า")

# ให้ผู้ใช้เลือกไฟล์ CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # โหลดข้อมูลจากไฟล์ที่ผู้ใช้เลือก
    data = pd.read_csv(uploaded_file)

    # เพิ่มคอลัมน์ Revenue
    data['Revenue'] = data['Quantity'] * data['Total Amount']
    data['Month'] = pd.to_datetime(data['Date']).dt.month
    data['Year'] = pd.to_datetime(data['Date']).dt.year

    # สินค้าที่ขายดีที่สุด
    top_products = data.groupby('Product Category')['Revenue'].sum().sort_values(ascending=False)

    # ยอดขายรายเดือน
    monthly_sales = data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()

    # แสดงตารางข้อมูล
    st.subheader("ข้อมูลทั้งหมด")
    st.dataframe(data)

    # สินค้าที่ขายดีที่สุด
    st.subheader("สินค้าที่ขายดีที่สุด")
    st.bar_chart(top_products.head(10))

    # กราฟยอดขายรายเดือน
    st.subheader("ยอดขายรายเดือน")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x='Month', y='Revenue', hue='Year', marker='o', ax=ax)
    ax.set_title("Monthly Revenue")
    st.pyplot(fig)
else:
    st.warning("กรุณาอัปโหลดไฟล์ CSV เพื่อดูข้อมูล")
