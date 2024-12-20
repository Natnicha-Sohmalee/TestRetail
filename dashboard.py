import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# แสดงหัวข้อ
st.title("Retail Sales Dashboard")
st.write("วิเคราะห์ข้อมูลยอดขายร้านค้า")

# โหลดข้อมูลจากไฟล์ CSV (อ่านไฟล์ที่ชื่อ 'sales_data.csv' ที่อยู่ในโฟลเดอร์เดียวกับไฟล์ .py นี้)
try:
    # กำหนดชื่อไฟล์ CSV ที่ต้องการอ่าน
    FILE_NAME = 'output_sales_data.csv'  # เปลี่ยนชื่อไฟล์ได้ตามต้องการ
    data = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    st.error(f"ไม่พบไฟล์ '{FILE_NAME}'. กรุณาตรวจสอบชื่อไฟล์และที่ตั้งไฟล์")
    st.stop()
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
    st.stop()

# ตรวจสอบและเตรียมข้อมูล
try:
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year

    # ตรวจสอบว่ามีคอลัมน์ที่ต้องการหรือไม่
    required_columns = ['Date', 'Quantity', 'Total Amount', 'Product Category']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"ไฟล์ CSV ขาดคอลัมน์ที่จำเป็น: {', '.join(missing_columns)}")
        st.stop()

    # เพิ่มคอลัมน์ Revenue
    data['Revenue'] = data['Quantity'] * data['Total Amount']

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดขณะประมวลผลข้อมูล: {e}")
    st.stop()

# วิเคราะห์ข้อมูล
try:
    # สินค้าที่ขายดีที่สุด
    top_products = data.groupby('Product Category')['Revenue'].sum().sort_values(ascending=False)

    # ยอดขายรายเดือน
    monthly_sales = data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()

    # แสดงตารางข้อมูล
    st.subheader("📋 ข้อมูลทั้งหมด")
    st.dataframe(data)

    # แสดงกราฟสินค้าที่ขายดีที่สุด
    st.subheader("🔥 สินค้าที่ขายดีที่สุด")
    st.bar_chart(top_products.head(10))

    # แสดงกราฟยอดขายรายเดือน
    st.subheader("📈 ยอดขายรายเดือน")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x='Month', y='Revenue', hue='Year', marker='o', ax=ax)
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    st.pyplot(fig)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดขณะวิเคราะห์ข้อมูล: {e}")
