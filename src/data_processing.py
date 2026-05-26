import pandas as pd
import streamlit as st
from utils import grab_csv_data, month_translator

# Tabela de tradução de meses (dicionário)

@st.cache_data
def sales_data_process(data_filepath) -> dict:
    """
    Processa a tabela de dados e retorna os atributos relevantes:
        sales_data
        orders_amt
        total_income
        avg_ticket
        status_count
        cancel_rate
        day_summary
        month_summary
        quarter_summary

    IMPORTANTE: Considera que os pedidos sejam todos feitos em um único ano.
    
    """
    sales_data = grab_csv_data(data_filepath)

    # === VISÃO GERAL DE PEDIDOS ===

    orders_amt = sales_data['order_id'].count() # Calcula quantidade de pedidos

    total_income = sales_data['total_value'].sum() # Calcula receita total

    avg_ticket = total_income / orders_amt # Calcula ticket médio

    status_count = sales_data.groupby('order_status')['order_id'].count() # Series com quantidade de cada status

    cancel_rate = status_count['Cancelado'] / orders_amt # Calcula taxa de cancelamento

    # --- Cria as tabelas sobre tempo (receitas por mês, pedidos por dias, etc.)

    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 

    # Faz tabela agrupada por dia. Colunas: income | orders_amt | avg_ticket
    day_summary = sales_data.groupby('order_date').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    day_summary['avg_ticket'] = day_summary['income'] / day_summary['orders_amt']

    # Faz tabela agrupada por mês. Colunas: income | orders_amt | avg_ticket
    sales_data['order_month'] = sales_data['order_date'].dt.month
    month_summary = sales_data.groupby('order_month').agg(
        income = ('total_value', 'sum'),
        orders_amt = ('order_id', 'count')
    ).reset_index()
    month_summary['avg_ticket'] = month_summary['income'] / month_summary['orders_amt']
    month_summary['month_name'] = month_summary['order_month'].map(month_translator)

    # Faz tabela agrupada por trimestre. Colunas: income | orders_amt | avg_ticket
    sales_data['order_quarter'] = sales_data['order_date'].dt.quarter
    quarter_summary = sales_data.groupby('order_quarter').agg(
        income=('total_value', 'sum'),
        orders_amt=('order_id', 'count')
    ).reset_index()
    quarter_summary['avg_ticket'] = quarter_summary['income'] / quarter_summary['orders_amt']

    # === PAINEL 02: TABELAS PARA ANÁLISE DE PRODUTOS E CATEGORIAS ===

    product_rank_income = sales_data.groupby('product_name')['total_value'].sum().reset_index()
    product_rank_income = product_rank_income.sort_values(by='total_value', ascending=True).head(5)

    product_rank_orders_amt = sales_data.groupby('product_name')['order_id'].count().reset_index()
    product_rank_orders_amt = product_rank_orders_amt.sort_values(by='order_id', ascending=True).head(5)

    product_metrics = sales_data.groupby('product_name').agg(
        total_value=('total_value', 'sum'),
        order_id=('order_id', 'count')
    ).reset_index()
    product_metrics['avg_ticket'] = product_metrics['total_value'] / product_metrics['order_id']
    product_rank_avgticket = product_metrics.sort_values(by='avg_ticket', ascending=True).head(5)

    category_proportion_income = sales_data.groupby('product_category')['total_value'].sum().reset_index()
    category_proportion_income = category_proportion_income.sort_values(by='total_value', ascending=False)

    category_proportion_orders_amt = sales_data.groupby('product_category')['order_id'].count().reset_index()
    category_proportion_orders_amt = category_proportion_orders_amt.sort_values(by='order_id', ascending=False)

    category_metrics = sales_data.groupby('product_category').agg(
        total_value=('total_value', 'sum'),
        order_id=('order_id', 'count')
    ).reset_index()
    category_metrics['avg_ticket'] = category_metrics['total_value'] / category_metrics['order_id']
    category_proportion_avgticket = category_metrics.sort_values(by='avg_ticket', ascending=False)

    variable_dict = {
        'sales_data': sales_data,
        'orders_amt': orders_amt,
        'total_income': total_income,
        'avg_ticket': avg_ticket,
        'status_count': status_count,
        'cancel_rate': cancel_rate,
        'day_summary': day_summary,
        'month_summary': month_summary,
        'quarter_summary': quarter_summary,
        'product_rank_income': product_rank_income,
        'product_rank_orders_amt': product_rank_orders_amt,
        'product_rank_avgticket': product_rank_avgticket,
        'category_proportion_income': category_proportion_income,
        'category_proportion_orders_amt': category_proportion_orders_amt,
        'category_proportion_avgticket': category_proportion_avgticket,
    }
    return variable_dict

if __name__ == '__main__':
    data = sales_data_process('data/vendas_linked_ps.csv')
    print(data)