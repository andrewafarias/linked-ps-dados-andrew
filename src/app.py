import streamlit as st
from data_processing import sales_data_process
from charts import build_charts
from utils import currency_format


def main():
    dataset = sales_data_process('data/vendas_linked_ps.csv')

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

    figures = build_charts(dataset, period_df, x_)

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(figures['fig_period_income'])
        st.plotly_chart(figures['fig_period_avgticket'])
    
    with col2:
        st.plotly_chart(figures['fig_period_orders_amt'])
    
    # === 02 ANÁLISE POR PRODUTO E CATEGORIA ===

    st.header("Análise de Produtos e Categorias")

    analysis_metric = st.radio(
        'Métrica de análise:',
        ['Faturamento', 'Pedidos', 'Ticket Médio'],
        horizontal=True,
        key='metric_selector'
    )

    product_fig = None
    category_fig = None
    if analysis_metric == 'Faturamento':
        product_fig = figures['fig_product_rank_income']
        category_fig = figures['fig_category_proportion_income']
    elif analysis_metric == 'Pedidos':
        product_fig = figures['fig_product_rank_orders_amt']
        category_fig = figures['fig_category_proportion_orders_amt']
    else: # analysis_metric == 'Ticket Médio'
        product_fig = figures['fig_product_rank_avgticket']
        category_fig = figures['fig_category_proportion_avgticket']

    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(product_fig)
    with col2: st.plotly_chart(category_fig)

    # === 03 DISTRIBUIÇÃO GEOGRÁFICA ===
    st.header("Distribuição Geográfica das Vendas")
    
    


    
if __name__ == '__main__':
    main()