import streamlit as st
import plotly.express as px
import pandas as pd
from data_processing import sales_data_process
from utils import currency_format


def main():
    dataset = sales_data_process('data/vendas_linked_ps.csv')
    sales_data: pd.DataFrame = dataset['sales_data']

    st.set_page_config(
        page_title="Andrew - Desafio de Dados",
        page_icon="📊",
        layout="wide"
    )

    st.title("Dashboard de Desempenho de Pedidos")

    # === 01 VISÃO GERAL DE PEDIDOS - TOPO DO DASHBOARD ===

    st.header("Visão Geral")

    # --- Cartões KPI
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card_income = st.container(border=True)
        with card_income:
            st.metric("Faturamento", currency_format(dataset['total_income']))

    with col2:
        card_orders_amt = st.container(border=True)
        with card_orders_amt:
            st.metric("Pedidos", dataset['orders_amt'])
    
    with col3:
        card_avgticket = st.container(border=True)
        with card_avgticket:
            st.metric("Ticket médio", currency_format(dataset['avg_ticket']))

    with col4:
        card_cancelrate = st.container(border=True)
        with card_cancelrate:
            st.metric("Taxa de cancelamento", f"{dataset['cancel_rate']*100:.2f}%")
    
    # --- Gráficos de tendência

    # Seleção de como o usuário quer visualizar os gráficos de tendência (por dia, mês, trimestre)
    granularity = st.radio(
        "Escolha a visão temporal:",
        ["Diário", "Mensal", "Trimestral"],
        horizontal=True,
        key="time_selector"
    )

    period_df = None
    x_ = None
    if granularity == "Diário":
        period_df = dataset['day_summary']
        x_ = 'order_date'
    elif granularity == "Mensal":
        period_df = dataset['month_summary']
        x_ = 'month_name'
    else:
        period_df = dataset['quarter_summary']
        x_ = 'order_quarter'

    fig_period_income = px.line(period_df, x=x_, y='income', title='Evolução do Faturamento')
    fig_period_orders_amt = px.line(period_df, x=x_, y='orders_amt', title='Evolução dos Pedidos')
    fig_period_avgticket = px.line(period_df, x=x_, y='avg_ticket', title='Evolução do Ticket Médio')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_period_income)
        st.plotly_chart(fig_period_avgticket)
    
    with col2:
        st.plotly_chart(fig_period_orders_amt)
    
    # === 02 ANÁLISE POR PRODUTO E CATEGORIA ===

    st.header("Análise de Produtos e Categorias")

    analysis_metric = st.radio(
        'Métrica de análise:',
        ['Faturamento', 'Pedidos', 'Ticket Médio'],
        horizontal=True,
        key='metric_selector'
    )

    # Faz o rank de produtos com maior faturamento
    product_rank_income = sales_data.groupby('product_name')['total_value'].sum().reset_index()
    product_rank_income = product_rank_income.sort_values(by='total_value', ascending=True).head(5)
    fig_product_rank_income = px.bar(
        product_rank_income, 
        x='total_value',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Faturamento'
    )

    # Faz o rank de produtos mais pedidos
    product_rank_orders_amt = sales_data.groupby('product_name')['order_id'].count().reset_index()
    product_rank_orders_amt = product_rank_orders_amt.sort_values(by='order_id', ascending=True).head(5)
    fig_product_rank_orders_amt = px.bar(
        product_rank_orders_amt,
        x='order_id',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos Mais Pedidos'
    )

    # Faz o rank de produtos com maior ticket médio
    product_metrics = sales_data.groupby('product_name').agg({
        'total_value': 'sum',
        'order_id': 'count'
    }).reset_index()
    product_metrics['avg_ticket'] = product_metrics['total_value'] / product_metrics['order_id']
    product_rank_avgticket = product_metrics.sort_values(by='avg_ticket', ascending=True).head(5)
    fig_product_rank_avgticket = px.bar(
        product_rank_avgticket,
        x='avg_ticket',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Ticket Médio'
    )

    # Faz o gráfico de proporção de faturamento por categoria
    category_proportion_income = sales_data.groupby('product_category')['total_value'].sum().reset_index()
    category_proportion_income = category_proportion_income.sort_values(by='total_value', ascending=False)
    fig_category_proportion_income = px.pie(
        category_proportion_income,
        names='product_category',
        values='total_value',
        title='Faturamento por Categoria'
    )
    
    # Faz o o gráfico de proporção de pedidos por categoria
    category_proportion_orders_amt = sales_data.groupby('product_category')['order_id'].count().reset_index()
    category_proportion_orders_amt = category_proportion_orders_amt.sort_values(by='order_id', ascending=False)
    fig_category_proportion_orders_amt = px.pie(
        category_proportion_orders_amt,
        names='product_category',
        values='order_id',
        title='Pedidos por Categoria'
    )

    # Faz o gráfico de proporção de ticket médio por categoria
    category_proportion_avgticket = category_proportion_income # Reaproveita os calculos precedentes para obter ticket médio
    category_proportion_avgticket['avg_ticket'] = category_proportion_avgticket['total_value'] / category_proportion_orders_amt['order_id']
    category_proportion_avgticket = category_proportion_avgticket.sort_values(by='avg_ticket', ascending=False)
    fig_category_proportion_avgticket = px.bar(
        category_proportion_avgticket,
        x='avg_ticket',
        y='product_category',
        orientation='h',
        title='Ticket Médio por Categoria',
        color='product_category'
    )
    global_avg = dataset['avg_ticket']
    fig_category_proportion_avgticket.add_vline(x=global_avg, line_dash='dash', annotation_text='Ticket Médio global')

    product_fig = None
    category_fig = None
    if analysis_metric == 'Faturamento':
        product_fig = fig_product_rank_income
        category_fig = fig_category_proportion_income
    elif analysis_metric == 'Pedidos':
        product_fig = fig_product_rank_orders_amt
        category_fig = fig_category_proportion_orders_amt
    else: # analysis_metric == 'Ticket Médio'
        product_fig = fig_product_rank_avgticket
        category_fig = fig_category_proportion_avgticket

    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(product_fig)
    with col2: st.plotly_chart(category_fig)

    # === 03 DISTRIBUIÇÃO GEOGRÁFICA ===
    st.header("Distribuição Geográfica das Vendas")
    
    


    
if __name__ == '__main__':
    main()