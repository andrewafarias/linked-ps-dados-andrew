import streamlit as st
import plotly.express as px
from data_processing import sales_data_process
from utils import currency_format


def main():
    dataset = sales_data_process('data/vendas_linked_ps.csv')

    st.set_page_config(
        page_title="Andrew - Desafio de Dados",
        page_icon="📊",
        layout="wide"
    )

    st.title("Dashboard de Desempenho de Vendas")

    # === TOPO DO DASHBOARD ===

    st.header("Visão Geral")

    # --- Cartões KPI
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card_income = st.container(border=True)
        with card_income:
            st.metric("Faturamento", currency_format(dataset['total_income']))

    with col2:
        card_sales = st.container(border=True)
        with card_sales:
            st.metric("Vendas", dataset['sales_amt'])
    
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
    elif granularity == "Trimestral":
        period_df = dataset['quarter_summary']
        x_ = 'order_quarter'
    else:
        raise ValueError('Erro: A visão temporal não foi selecionada corretamente. Valor inesperado.')

    fig_period_income = px.line(period_df, x=x_, y='income', title='Evolução do Faturamento')
    fig_period_sales_amt = px.line(period_df, x=x_, y='sales_amt', title='Evolução das Vendas')
    fig_period_avgticket = px.line(period_df, x=x_, y='avg_ticket', title='Evolução do Ticket Médio')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_period_income)
        st.plotly_chart(fig_period_avgticket)
    
    with col2:
        st.plotly_chart(fig_period_sales_amt)
    
    # === 02 ANÁLISE POR PRODUTO E CATEGORIA
    st.header("Análise de Produtos e Categorias")



    
    
if __name__ == '__main__':
    main()