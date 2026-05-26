import pandas as pd
import streamlit as st
from utils import grab_csv_data, month_translator

@st.cache_data
def get_orders_amt(sales_data: pd.DataFrame) -> int:
    return int(sales_data['order_id'].count())

@st.cache_data
def get_total_income(sales_data: pd.DataFrame) -> float:
    return float(sales_data['total_value'].sum())

@st.cache_data
def get_avg_ticket(sales_data: pd.DataFrame) -> float:
    return float(get_total_income(sales_data) / get_orders_amt(sales_data))

@st.cache_data
def get_status_count(sales_data: pd.DataFrame) -> pd.Series:
    return sales_data.groupby('order_status')['order_id'].count()

@st.cache_data
def get_cancel_rate(sales_data: pd.DataFrame) -> float:
    status_count = get_status_count(sales_data)
    cancel_amt = status_count['Cancelado'] if 'Cancelado' in status_count else 0
    return float(cancel_amt / get_orders_amt(sales_data))

@st.cache_data
def get_day_summary(sales_data: pd.DataFrame) -> pd.DataFrame:
    sales_data = sales_data.copy()
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 
    day_summary = sales_data.groupby('order_date').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    day_summary['avg_ticket'] = day_summary['income'] / day_summary['orders_amt']
    return day_summary

@st.cache_data
def get_month_summary(sales_data: pd.DataFrame) -> pd.DataFrame:
    sales_data = sales_data.copy()
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 
    sales_data['order_month'] = sales_data['order_date'].dt.month
    month_summary = sales_data.groupby('order_month').agg(
        income = ('total_value', 'sum'),
        orders_amt = ('order_id', 'count')
    ).reset_index()
    month_summary['avg_ticket'] = month_summary['income'] / month_summary['orders_amt']
    month_summary['month_name'] = month_summary['order_month'].map(month_translator)
    return month_summary

@st.cache_data
def get_quarter_summary(sales_data: pd.DataFrame) -> pd.DataFrame:
    sales_data = sales_data.copy()
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 
    sales_data['order_quarter'] = sales_data['order_date'].dt.quarter
    quarter_summary = sales_data.groupby('order_quarter').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    quarter_summary['avg_ticket'] = quarter_summary['income'] / quarter_summary['orders_amt']
    return quarter_summary

@st.cache_data
def get_product_rank_income(sales_data: pd.DataFrame) -> pd.DataFrame:
    product_rank_income = sales_data.groupby('product_name')['total_value'].sum().reset_index()
    return product_rank_income.sort_values(by='total_value', ascending=True).head(5)

@st.cache_data
def get_product_rank_volume(sales_data: pd.DataFrame) -> pd.DataFrame:
    product_rank_volume = sales_data.groupby('product_name')['quantity'].sum().reset_index()
    return product_rank_volume.sort_values(by='quantity', ascending=True).head(5)

@st.cache_data
def get_product_rank_avgticket(sales_data: pd.DataFrame) -> pd.DataFrame:
    product_metrics = sales_data.groupby('product_name').agg(
        total_value=('total_value', 'sum'),
        order_id=('order_id', 'count')
    ).reset_index()
    product_metrics['avg_ticket'] = product_metrics['total_value'] / product_metrics['order_id']
    return product_metrics.sort_values(by='avg_ticket', ascending=True).head(5)

@st.cache_data
def get_category_proportion_income(sales_data: pd.DataFrame) -> pd.DataFrame:
    category_proportion_income = sales_data.groupby('product_category')['total_value'].sum().reset_index()
    return category_proportion_income.sort_values(by='total_value', ascending=False)

@st.cache_data
def get_category_proportion_volume(sales_data: pd.DataFrame) -> pd.DataFrame:
    category_proportion_volume = sales_data.groupby('product_category')['quantity'].sum().reset_index()
    return category_proportion_volume.sort_values(by='quantity', ascending=False)

@st.cache_data
def get_category_proportion_avgticket(sales_data: pd.DataFrame) -> pd.DataFrame:
    category_metrics = sales_data.groupby('product_category').agg(
        total_value=('total_value', 'sum'),
        order_id=('order_id', 'count')
    ).reset_index()
    category_metrics['avg_ticket'] = category_metrics['total_value'] / category_metrics['order_id']
    return category_metrics.sort_values(by='avg_ticket', ascending=False)

if __name__ == '__main__':
    data = grab_csv_data('data/vendas_linked_ps.csv')
    print(get_orders_amt(data))
