import pandas as pd
import streamlit as st
from utils import month_translator

@st.cache_data
def grab_csv_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

#================================
#--- 01 VISÃO GERAL DE VENDAS ---
#================================
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
    status_df = get_status_count(sales_data).set_index('order_status')['order_id']
    cancel_amt = status_df.get('Cancelado', 0)
    return float(cancel_amt / get_orders_amt(sales_data))

@st.cache_data
def get_day_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DataFrame com as colunas: order_date, income, orders_amt, avg_ticket."""
    sales_data = sales_data.copy()
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 
    day_summary = sales_data.groupby('order_date').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    day_summary['avg_ticket'] = day_summary['income'] / day_summary['orders_amt']
    return day_summary

@st.cache_data
def get_month_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DataFrame com as colunas: order_month, income, orders_amt, avg_ticket, month_name."""
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
def get_quarter_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DataFrame com as colunas: order_quarter, income, orders_amt, avg_ticket."""
    sales_data = sales_data.copy()
    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 
    sales_data['order_quarter'] = sales_data['order_date'].dt.quarter
    quarter_summary = sales_data.groupby('order_quarter').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    quarter_summary['avg_ticket'] = quarter_summary['income'] / quarter_summary['orders_amt']
    return quarter_summary

#===========================================
#--- 02 ANALISE DE PRODUTOS E CATEGORIAS ---
#===========================================

@st.cache_data
def get_product_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DataFrame com as colunas: product_name, total_value, quantity, order_id, avg_ticket."""
    product_metrics = sales_data.groupby('product_name').agg(
        total_value=('total_value', 'sum'),
        quantity=('quantity', 'sum'),
        order_id=('order_id', 'count'),
        unit_price_mean=('unit_price', 'mean'),
        product_category=('product_category', 'unique')
    ).reset_index()
    product_metrics['avg_ticket'] = product_metrics['total_value'] / product_metrics['order_id']
    return product_metrics

@st.cache_data
def get_category_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um DataFrame com as colunas: product_category, total_value, quantity, order_id, avg_ticket."""
    category_metrics = sales_data.groupby('product_category').agg(
        total_value=('total_value', 'sum'),
        quantity=('quantity', 'sum'),
        order_id=('order_id', 'count')
    ).reset_index()
    category_metrics['avg_ticket'] = category_metrics['total_value'] / category_metrics['order_id']
    return category_metrics

#=============================================
#--- 05 DISTRIBUIÇÃO GEOGRÁFICA DAS VENDAS ---
#=============================================

@st.cache_data
def get_region_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    region_metrics = sales_data.groupby('customer_region').agg({
        'total_value': 'sum',
        'order_id': 'count',
        'quantity': 'sum'
    }).reset_index().sort_values(by='customer_region')
    region_metrics['avg_ticket'] = region_metrics['total_value'] / region_metrics['order_id']
    return region_metrics

@st.cache_data
def get_region_category_metrics(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Retorna um df agrupado por (região, categoria) com as colunas: 'order_id'(count), 'quantity'(sum), 'total_value'(sum)"""
    region_category_metrics = sales_data.groupby(['customer_region', 'product_category']).agg(
        order_id=('order_id', 'count'),
        quantity=('quantity', 'sum'),
        total_value=('total_value', 'sum')
    ).reset_index()
    region_category_metrics['avg_ticket'] = region_category_metrics['total_value'] / region_category_metrics['order_id']
    return region_category_metrics

if __name__ == '__main__':
    data = grab_csv_data('data/vendas_linked_ps.csv')
    product_metrics = get_product_metrics(data)
    print(product_metrics.sort_values(by='total_value', ascending=False))
    print(product_metrics['order_id'].sum())
