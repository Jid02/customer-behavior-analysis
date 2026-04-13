# IMPORT LIBRARIES

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_data, filter_data, calculate_kpis
#PAGE CONFIG (WIDE LAYOUT)

st.set_page_config(page_title="Customer Intelligence Dashboard", layout="wide")

#load data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_data.csv")

df = load_data(DATA_PATH)

#TITLE
st.title("📊 Customer Behavior Intelligence Dashboard")

# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")

gender = st.sidebar.selectbox("Select Gender", ["All"] + list(df['Gender'].unique()))
category = st.sidebar.selectbox("Select Category", ["All"] + list(df['Category'].unique()))

# Apply filters
filtered_df = filter_data(df, gender, category)

#KPI
total_revenue, avg_purchase, total_customers = calculate_kpis(filtered_df)

#TABS (CLEAN UI)
tab1, tab2 = st.tabs(["📊 Overview", "📈 Advanced Analysis"])

# TAB 1: OVERVIEW

with tab1:

    # -------- ROW 1 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age Distribution")
        fig = px.histogram(filtered_df, x="Age", nbins=20, title="Age Distribution")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Gender vs Spending")
        fig = px.box(filtered_df, x="Gender", y="Purchase Amount (USD)",
                     title="Gender vs Spending")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    # -------- ROW 2 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Category Sales")
        cat_data = filtered_df['Category'].value_counts().reset_index()
        cat_data.columns = ['Category', 'Count']
        fig = px.bar(cat_data, x='Category', y='Count', title="Category Distribution")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Discount Impact")
        fig = px.box(filtered_df, x="Discount Applied",
                     y="Purchase Amount (USD)",
                     title="Discount Impact")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

# TAB 2: ADVANCED ANALYSIS
with tab2:

    # -------- ROW 1 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Type vs Spending")
        fig = px.box(filtered_df, x="Customer_Type",
                     y="Purchase Amount (USD)",
                     title="Customer Type Analysis")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Seasonal Sales")
        season_data = filtered_df.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
        fig = px.bar(season_data, x="Season", y="Purchase Amount (USD)",
                     title="Seasonal Sales")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    # -------- ROW 2 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Payment Method Preference")
        pay_data = filtered_df['Payment Method'].value_counts().reset_index()
        pay_data.columns = ['Payment Method', 'Count']
        fig = px.pie(pay_data, names='Payment Method', values='Count',
                     title="Payment Method Distribution")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Purchase Frequency Analysis")
        freq_data = filtered_df['Frequency of Purchases'].value_counts().reset_index()
        freq_data.columns = ['Frequency', 'Count']
        fig = px.bar(freq_data, x='Frequency', y='Count',
                     title="Purchase Frequency")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🔍 Enlarge Chart"):
            st.plotly_chart(fig, use_container_width=True)

# DOWNLOAD BUTTON
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
