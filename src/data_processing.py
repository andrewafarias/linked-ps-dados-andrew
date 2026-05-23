import pandas as pd
import streamlit as st
from utils import grab_csv_data, month_translator

# Tabela de tradução de meses (dicionário)


def data_process(data_filepath) -> dict:
    """
    Processa a tabela de dados e retorna os atributos relevantes:
        sales_data
        sales_amt
        total_income
        avg_ticket
        status_count
        cancel_rate
        day_summary
        month_summary
        quarter_summary
    
    """
    sales_data = grab_csv_data(data_filepath)

    # === VISÃO GERAL DE VENDAS ===

    sales_amt = sales_data['order_id'].count() # Calcula quantidade de pedidos(vendas)

    total_income = sales_data['total_value'].sum() # Calcula receita total

    avg_ticket = total_income / sales_amt # Calcula ticket médio

    status_count = sales_data.groupby('order_status')['order_id'].count() # Series com quantidade de cada status

    cancel_rate = status_count['Cancelado'] / sales_amt # Calcula taxa de cancelamento

    # --- Cria as tabelas sobre tempo (receitas por mês, vendas por dias, etc.)

    sales_data['order_date'] = pd.to_datetime(sales_data['order_date']) 

    # Faz tabela agrupada por dia. Colunas: day_income | day_sales_amt | day_avg_ticket
    day_summary = sales_data.groupby('order_date').agg(
        day_income=('total_value', 'sum'),
        day_sales_amt=('order_id', 'count')
    ).reset_index()
    day_summary['day_avg_ticket'] = day_summary['day_income'] / day_summary['day_sales_amt']

    # Faz tabela agrupada por mês. Colunas: month_income | month_sales_amt | month_avg_ticket
    sales_data['order_month'] = sales_data['order_date'].dt.month
    month_summary = sales_data.groupby('order_month').agg(
        month_income = ('total_value', 'sum'),
        month_sales_amt = ('order_id', 'count')
    ).reset_index()
    month_summary['month_avg_ticket'] = month_summary['month_income'] / month_summary['month_sales_amt']
    month_summary['month_name'] = month_summary['order_month'].map(month_translator)

    # Faz tabela agrupada por trimestre. Colunas: quarter_income | quarter_sales_amt | quarter_avg_ticket
    sales_data['order_quarter'] = sales_data['order_date'].dt.quarter
    quarter_summary = sales_data.groupby('order_quarter').agg(
        quarter_income=('total_value', 'sum'),
        quarter_sales_amt=('order_id', 'count')
    ).reset_index()
    quarter_summary['quarter_avg_ticket'] = quarter_summary['quarter_income'] / quarter_summary['quarter_sales_amt']

    variable_dict = {
        'sales_data': sales_data,
        'sales_amt': sales_amt,
        'total_income': total_income,
        'avg_ticket': avg_ticket,
        'status_count': status_count,
        'cancel_rate': cancel_rate,
        'day_summary': day_summary,
        'month_summary': month_summary,
        'quarter_summary': quarter_summary,
    }
    return variable_dict

if __name__ == '__main__':
    data = data_process('data/vendas_linked_ps.csv')
    print(data)