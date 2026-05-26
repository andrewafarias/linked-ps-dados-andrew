import streamlit as st
import data_processing as dp
import charts
from utils import currency_format, grab_csv_data


def render_sales_overview_panel(sales_data):
    st.header("Visão Geral")

    total_income = dp.get_total_income(sales_data)
    orders_amt = dp.get_orders_amt(sales_data)
    avg_ticket = dp.get_avg_ticket(sales_data)
    cancel_rate = dp.get_cancel_rate(sales_data)

    # --- Cartões KPI
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card_income = st.container(border=True)
        with card_income:
            st.metric("Faturamento", currency_format(total_income))

    with col2:
        card_orders_amt = st.container(border=True)
        with card_orders_amt:
            st.metric("Pedidos", orders_amt)
    
    with col3:
        card_avgticket = st.container(border=True)
        with card_avgticket:
            st.metric("Ticket médio", currency_format(avg_ticket))

    with col4:
        card_cancelrate = st.container(border=True)
        with card_cancelrate:
            st.metric("Taxa de cancelamento", f"{cancel_rate*100:.2f}%")
    
    # --- Gráficos de tendência

    # Seleção de como o usuário quer visualizar os gráficos de tendência (por dia, mês, trimestre)
    granularity = st.radio(
        "Escolha a visão temporal:",
        ["Diário", "Mensal", "Trimestral"],
        horizontal=True,
        key="time_selector"
    )

    if granularity == "Diário":
        period_df = dp.get_day_summary(sales_data)
        period_figures = charts.build_period_charts(period_df, 'order_date')
    elif granularity == "Mensal":
        period_df = dp.get_month_summary(sales_data)
        period_figures = charts.build_period_charts(period_df, 'month_name')
    else:
        period_df = dp.get_quarter_summary(sales_data)
        period_figures = charts.build_period_charts(period_df, 'order_quarter')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(period_figures['period_income'])
        st.plotly_chart(period_figures['period_avgticket'])
    
    with col2:
        st.plotly_chart(period_figures['period_orders_amt'])


def render_products_and_categories_panel(sales_data):
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
        product_fig = charts.build_product_rank_income(dp.get_product_rank_income(sales_data))
        category_fig = charts.build_category_proportion_income(dp.get_category_proportion_income(sales_data))
    elif analysis_metric == 'Pedidos':
        product_fig = charts.build_product_rank_orders_amt(dp.get_product_rank_volume(sales_data))
        category_fig = charts.build_category_proportion_orders_amt(dp.get_category_proportion_volume(sales_data))
    else: # analysis_metric == 'Ticket Médio'
        product_fig = charts.build_product_rank_avgticket(dp.get_product_rank_avgticket(sales_data))
        avg_ticket = dp.get_avg_ticket(sales_data)
        category_fig = charts.build_category_proportion_avgticket(dp.get_category_proportion_avgticket(sales_data), avg_ticket)

    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(product_fig)
    with col2: st.plotly_chart(category_fig)

def render_geographical_distribution_panel(sales_data):
    st.header('Distribuição Geográfica das Vendas')
    

def main():
    sales_data = grab_csv_data('data/vendas_linked_ps.csv')
    
    st.set_page_config(
        page_title="Andrew - Desafio de Dados",
        page_icon="📊",
        layout="wide"
    )

    st.title("Dashboard de Desempenho de Pedidos")

    # === 01 VISÃO GERAL DE VENDAS - TOPO DO DASHBOARD ===
    render_sales_overview_panel(sales_data)
    
    # === 02 ANÁLISE POR PRODUTO E CATEGORIA ===
    render_products_and_categories_panel(sales_data)

    # === 03 DISTRIBUIÇÃO GEOGRÁFICA ===
    render_geographical_distribution_panel(sales_data)
    

if __name__ == '__main__':
    main()