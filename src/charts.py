import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#================================
#--- 01 VISÃO GERAL DE VENDAS ---
#================================

def build_period_charts(period_df: pd.DataFrame, x_: str) -> dict:
    x_labels = {
        'order_date': 'Data',
        'month_name': 'Mês',
        'order_quarter': 'Trimestre'
    }
    labels = {
        x_: x_labels.get(x_, 'Período'),
        'income': 'Faturamento (R$)',
        'orders_amt': 'Volume de Pedidos',
        'avg_ticket': 'Ticket Médio (R$)'
    }
    return {
        'period_income': px.line(period_df, x=x_, y='income', title='Evolução do Faturamento', labels=labels),
        'period_orders_amt': px.line(period_df, x=x_, y='orders_amt', title='Evolução dos Pedidos', labels=labels),
        'period_avg_ticket': px.line(period_df, x=x_, y='avg_ticket', title='Evolução do Ticket Médio', labels=labels),
    }

#===========================================
#--- 02 ANALISE DE PRODUTOS E CATEGORIAS ---
#===========================================
@st.cache_data
def build_product_rank_income(product_rank_income_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        product_rank_income_df,
        x='total_value',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Faturamento',
        labels={'total_value': 'Faturamento (R$)', 'product_name': 'Produto'}
    )

@st.cache_data
def build_product_rank_orders_amt(product_rank_orders_amt_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        product_rank_orders_amt_df,
        x='quantity',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos de Maior Volume de Vendas',
        labels={'quantity': 'Quantidade Vendida', 'product_name': 'Produto'}
    )

@st.cache_data
def build_product_rank_avg_ticket(product_rank_avg_ticket_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        product_rank_avg_ticket_df,
        x='avg_ticket',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Ticket Médio',
        labels={'avg_ticket': 'Ticket Médio (R$)', 'product_name': 'Produto'}
    )

@st.cache_data
def build_category_proportion_income(category_proportion_income_df: pd.DataFrame) -> go.Figure:
    return px.pie(
        category_proportion_income_df,
        names='product_category',
        values='total_value',
        title='Faturamento por Categoria',
        labels={'product_category': 'Categoria', 'total_value': 'Faturamento (R$)'}
    )

@st.cache_data
def build_category_proportion_orders_amt(category_proportion_orders_amt_df: pd.DataFrame) -> go.Figure:
    return px.pie(
        category_proportion_orders_amt_df,
        names='product_category',
        values='quantity',
        title='Volume de Vendas por Categoria',
        labels={'product_category': 'Categoria', 'quantity': 'Quantidade Vendida'}
    )

@st.cache_data
def build_category_proportion_avg_ticket(category_proportion_avg_ticket_df: pd.DataFrame, avg_ticket: float) -> go.Figure:
    fig = px.bar(
        category_proportion_avg_ticket_df,
        x='avg_ticket',
        y='product_category',
        orientation='h',
        title='Ticket Médio por Categoria',
        color='product_category',
        labels={'avg_ticket': 'Ticket Médio (R$)', 'product_category': 'Categoria'}
    )
    fig.add_vline(
        x=avg_ticket,
        line_dash='dash',
        annotation_text='Ticket Médio global',
        annotation_position='bottom right'
    )
    return fig

#=============================================
#--- 05 DISTRIBUIÇÃO GEOGRÁFICA DAS VENDAS ---
#=============================================

@st.cache_data
def build_regions_income(region_df: pd.DataFrame,) -> go.Figure:
    return px.bar(
        region_df,
        x='customer_region',
        y='total_value',
        title='Faturamento por Região',
        labels={'customer_region': 'Região', 'total_value': 'Faturamento (R$)'}
        #color='customer_region'
    ).update_layout(showlegend=False)

@st.cache_data
def build_regions_orders_amt(region_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        region_df,
        x='customer_region',
        y='order_id',
        title='Pedidos por Região',
        labels={'customer_region': 'Região', 'order_id': 'Volume de Pedidos'}
        #color='customer_region'
    ).update_layout(showlegend=False)

@st.cache_data
def build_regions_avg_ticket(region_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        region_df,
        x='customer_region',
        y='avg_ticket',
        title='Ticket Médio por Região',
        labels={'customer_region': 'Região', 'avg_ticket': 'Ticket Médio (R$)'}
        #color='customer_region'
    ).update_layout(showlegend=False)
