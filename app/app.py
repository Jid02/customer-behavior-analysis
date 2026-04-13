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
st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==============================
# 📌 LOAD DATA (DEPLOYMENT SAFE)
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_data.csv")

df = pd.read_csv(DATA_PATH)

# ==============================
# 🎨 CUSTOM STYLING (PREMIUM UI)
# ==============================
st.markdown("""
<style>
.main {
    background-color: #ADD8E6;
}
h1, h2, h3 {
    color: #FFFFFF;
}
.stMetric {
    background-color: #ADD8E6;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 📌 HEADER
# ==============================
st.title("📊 Customer Intelligence Dashboard")

st.markdown("""
Analyze customer behavior, spending patterns, and key business insights in a simple and interactive way.
""")

st.divider()

# ==============================
# 📌 SIDEBAR FILTERS
# ==============================
st.sidebar.markdown("## 🎯 Filters")

gender = st.sidebar.selectbox("Gender", ["All"] + list(df['Gender'].unique()))
category = st.sidebar.selectbox("Category", ["All"] + list(df['Category'].unique()))

filtered_df = df.copy()

if gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == gender]

if category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category]

# ==============================
# 📌 KPI SECTION
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${filtered_df['Purchase Amount (USD)'].sum():,.0f}")
col2.metric("📊 Avg Purchase", f"${filtered_df['Purchase Amount (USD)'].mean():.2f}")
col3.metric("👥 Customers", filtered_df.shape[0])

st.divider()

# ==============================
# 📌 TABS FOR CLEAN UI
# ==============================
tab1, tab2 = st.tabs(["📊 Overview", "📈 Insights"])

# ==============================
# 📊 OVERVIEW TAB
# ==============================
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Age Distribution")
        fig1 = px.histogram(filtered_df, x="Age")
        st.plotly_chart(fig1, use_container_width=True, key="age")

    with col2:
        st.subheader("👥 Gender vs Spending")
        fig2 = px.box(filtered_df, x="Gender", y="Purchase Amount (USD)")
        st.plotly_chart(fig2, use_container_width=True, key="gender")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛍️ Category Distribution")
        cat_data = filtered_df['Category'].value_counts().reset_index()
        cat_data.columns = ['Category', 'Count']
        fig3 = px.bar(cat_data, x="Category", y="Count")
        st.plotly_chart(fig3, use_container_width=True, key="category")

    with col2:
        st.subheader("💸 Discount Impact")
        fig4 = px.box(filtered_df, x="Discount Applied", y="Purchase Amount (USD)")
        st.plotly_chart(fig4, use_container_width=True, key="discount")

# ==============================
# 📈 INSIGHTS TAB
# ==============================
with tab2:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Customer Type vs Spending")
        fig5 = px.box(filtered_df, x="Customer_Type", y="Purchase Amount (USD)")
        st.plotly_chart(fig5, use_container_width=True, key="customer")

    with col2:
        st.subheader("📅 Seasonal Sales")
        season_data = filtered_df.groupby("Season")["Purchase Amount (USD)"].sum().reset_index()
        fig6 = px.bar(season_data, x="Season", y="Purchase Amount (USD)")
        st.plotly_chart(fig6, use_container_width=True, key="season")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💳 Payment Methods")
        pay_data = filtered_df['Payment Method'].value_counts().reset_index()
        pay_data.columns = ['Payment Method', 'Count']
        fig7 = px.pie(pay_data, names="Payment Method", values="Count")
        st.plotly_chart(fig7, use_container_width=True, key="payment")

    with col2:
        st.subheader("🔁 Purchase Frequency")
        freq_data = filtered_df['Frequency of Purchases'].value_counts().reset_index()
        freq_data.columns = ['Frequency', 'Count']
        fig8 = px.bar(freq_data, x="Frequency", y="Count")
        st.plotly_chart(fig8, use_container_width=True, key="freq")

# ==============================
# 💡 KEY INSIGHTS SECTION
# ==============================
st.divider()

st.markdown("## 💡 Key Insights")

st.success("Customers aged 25–40 contribute the highest revenue")
st.info("Discounts positively influence purchase behavior")
st.warning("Certain product categories dominate sales trends")

# ==============================
# 📥 DOWNLOAD BUTTON
# ==============================
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv"
)

# ==============================
# 📌 FOOTER
# ==============================
st.markdown("---")
st.markdown("Made with ❤️ by Jidnyasa Pawar")
