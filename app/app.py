# ==============================
# 📌 IMPORTS
# ==============================
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================
# 📌 PAGE CONFIG
# ==============================
st.set_page_config(page_title="Customer Dashboard", layout="wide")

# ==============================
# 📌 LOAD DATA (FIXED PATH)
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_data.csv")

df = pd.read_csv(DATA_PATH)

# ==============================
# 📌 TITLE
# ==============================
st.title("📊 Customer Behavior Dashboard")

# ==============================
# 📌 SIDEBAR FILTERS
# ==============================
st.sidebar.header("Filters")

gender = st.sidebar.selectbox("Gender", ["All"] + list(df['Gender'].unique()))
category = st.sidebar.selectbox("Category", ["All"] + list(df['Category'].unique()))

# Apply filters
filtered_df = df.copy()

if gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == gender]

if category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category]

# ==============================
# 📌 KPI SECTION
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${filtered_df['Purchase Amount (USD)'].sum():,.0f}")
col2.metric("Avg Purchase", f"${filtered_df['Purchase Amount (USD)'].mean():.2f}")
col3.metric("Customers", filtered_df.shape[0])

# ==============================
# 📊 CHARTS (2 PER ROW)
# ==============================

# -------- ROW 1 --------
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(filtered_df, x="Age", title="Age Distribution")
    st.plotly_chart(fig1, use_container_width=True, key="age")

with col2:
    fig2 = px.box(filtered_df, x="Gender", y="Purchase Amount (USD)", title="Gender vs Spending")
    st.plotly_chart(fig2, use_container_width=True, key="gender")

# -------- ROW 2 --------
col1, col2 = st.columns(2)

with col1:
    cat_data = filtered_df['Category'].value_counts().reset_index()
    cat_data.columns = ['Category', 'Count']
    fig3 = px.bar(cat_data, x="Category", y="Count", title="Category Distribution")
    st.plotly_chart(fig3, use_container_width=True, key="category")

with col2:
    fig4 = px.box(filtered_df, x="Discount Applied", y="Purchase Amount (USD)", title="Discount Impact")
    st.plotly_chart(fig4, use_container_width=True, key="discount")

# -------- ROW 3 --------
col1, col2 = st.columns(2)

with col1:
    fig5 = px.box(filtered_df, x="Customer_Type", y="Purchase Amount (USD)", title="Customer Type vs Spending")
    st.plotly_chart(fig5, use_container_width=True, key="customer")

with col2:
    season_data = filtered_df.groupby("Season")["Purchase Amount (USD)"].sum().reset_index()
    fig6 = px.bar(season_data, x="Season", y="Purchase Amount (USD)", title="Seasonal Sales")
    st.plotly_chart(fig6, use_container_width=True, key="season")

# ==============================
# 📥 DOWNLOAD BUTTON
# ==============================
st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)
