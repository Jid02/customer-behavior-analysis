
import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df


#FILTER FUNCTION

def filter_data(df, gender, category):
    filtered_df = df.copy()

    if gender != "All":
        filtered_df = filtered_df[filtered_df['Gender'] == gender]

    if category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category]

    return filtered_df

#KPI CALCULATIONS

def calculate_kpis(df):
    total_revenue = df['Purchase Amount (USD)'].sum()
    avg_purchase = df['Purchase Amount (USD)'].mean()
    total_customers = df.shape[0]

    return total_revenue, avg_purchase, total_customers