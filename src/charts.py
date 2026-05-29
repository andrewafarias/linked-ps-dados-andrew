import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#================================
#--- 01 VISÃO GERAL DE VENDAS ---
#================================

def build_period_charts(period_df: pd.DataFrame, xaxis_column: str) -> dict:
    x_labels = {
        'order_date': 'Data',
        'month_name': 'Mês',
        'order_quarter': 'Trimestre'
    }
    labels = {
        xaxis_column: x_labels.get(xaxis_column, 'Período'),
        'income': 'Faturamento (R$)',
        'orders_amt': 'Volume de Pedidos',
        'avg_ticket': 'Ticket Médio (R$)'
    }
    plot = px.bar if xaxis_column == 'order_quarter' else px.line
    figures = {
        'period_income': plot(period_df, x=xaxis_column, y='income', title='Evolução do Faturamento', labels=labels),
        'period_orders_amt': plot(period_df, x=xaxis_column, y='orders_amt', title='Evolução dos Pedidos', labels=labels),
        'period_avg_ticket': plot(period_df, x=xaxis_column, y='avg_ticket', title='Evolução do Ticket Médio', labels=labels),
    }

    # Arruma os ticks dos gráficos de trimestre
    if xaxis_column == 'order_quarter':
        for fig in figures.values():
            fig.update_xaxes(
                tickmode = 'array',
                tickvals = [1, 2, 3, 4],
                ticktext = ['Q1', 'Q2', 'Q3', 'Q4']
            )
    
    return figures

# def build_status_charts(status_df: pd.DataFrame) -> go.Figure:
#     return px.pie(
#         status_df,
#         names='order_status',
#         values='order_id',
#         title='Status dos Pedidos',
#         labels={'order_status': 'Status', 'order_id': 'Quantidade de pedidos'}
#     )

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
        title='Top 5 produtos com maior faturamento',
        hover_data={'product_category':True, 'unit_price_mean':':.2f'},
        labels={'total_value': 'Faturamento (R$)', 'product_name': 'Produto', 'unit_price_mean': 'Preço médio (R$)'}
    )

@st.cache_data
def build_product_rank_orders_amt(product_rank_orders_amt_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        product_rank_orders_amt_df,
        x='quantity',
        y='product_name',
        orientation='h',
        title='Top 5 produtos de maior volume de vendas',
        hover_data={'product_category':True, 'unit_price_mean':':.2f'},
        labels={'quantity': 'Quantidade Vendida', 'product_name': 'Produto', 'unit_price_mean': 'Preço médio (R$)'}
    )

@st.cache_data
def build_product_rank_avg_ticket(product_rank_avg_ticket_df: pd.DataFrame) -> go.Figure:
    return px.bar(
        product_rank_avg_ticket_df,
        x='avg_ticket',
        y='product_name',
        orientation='h',
        title='Top 5 produtos com maior ticket médio',
        hover_data={'unit_price_mean': ':.2f', 'product_category':True},
        labels={'avg_ticket': 'Ticket Médio (R$)', 'product_name': 'Produto', 'unit_price_mean': 'Preço médio (R$)'}
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
#--- 03 DISTRIBUIÇÃO GEOGRÁFICA DAS VENDAS ---
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

@st.cache_data
def build_region_category_charts(region_category_df: pd.DataFrame) -> dict[str, go.Figure]:
    
    # -- Constrói o chart de categorias mais pedidas em cada estado
    orders_rank = (
        region_category_df
        .sort_values(['customer_region', 'order_id'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
        .sort_values('customer_region', ascending=True)
    )

    orders_fig = px.bar(
        orders_rank,
        x='customer_region',
        y='order_id',
        color='product_category',
        title='Categoria com mais pedidos por região',
        labels={'customer_region': 'Região', 'order_id': 'Quantidade de pedidos', 'product_category': 'Categoria'}
    )

    # -- Constrói o chart de categorias de maior faturamento em cada estado
    income_rank = (
        region_category_df
        .sort_values(['customer_region', 'total_value'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
        .sort_values('customer_region', ascending=True)
    )
    income_fig = px.bar(
        income_rank,
        x='customer_region',
        y='total_value',
        color='product_category',
        title='Categoria de maior faturamento por região',
        labels={'customer_region': 'Região', 'total_value': 'Faturamento', 'product_category': 'Categoria'}
    )

    # -- Constrói o chart de categoria com maior ticket médio por região
    ticket_rank = (
        region_category_df
        .sort_values(['customer_region', 'avg_ticket'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
        .sort_values('customer_region', ascending=True)
    )
    ticket_fig = px.bar(
        ticket_rank,
        x='customer_region',
        y='avg_ticket',
        color='product_category',
        title='Categoria de maior ticket médio por região',
        labels={'customer_region': 'Região', 'avg_ticket': 'Ticket médio', 'product_category': 'Categoria'}
    )

    return {'orders_fig': orders_fig, 'income_fig': income_fig, 'ticket_fig':ticket_fig}

@st.cache_data
def build_region_product_charts(region_product_df: pd.DataFrame) -> dict[str, go.Figure]:
    
    # -- Constrói o chart de Produtos mais pedidas em cada estado
    orders_rank = (
        region_product_df
        .sort_values(['customer_region', 'order_id'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
    )

    orders_fig = px.bar(
        orders_rank,
        x='customer_region',
        y='order_id',
        color='product_name',
        title='Produto com mais pedidos por região',
        labels={'customer_region': 'Região', 'order_id': 'Quantidade de pedidos', 'product_name': 'Produto'}
    )

    # -- Constrói o chart de Produtos de maior faturamento em cada estado
    income_rank = (
        region_product_df
        .sort_values(['customer_region', 'total_value'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
    )
    income_fig = px.bar(
        income_rank,
        x='customer_region',
        y='total_value',
        color='product_name',
        title='Produto de maior faturamento por região',
        labels={'customer_region': 'Região', 'total_value': 'Faturamento', 'product_name': 'Produto'}
    )

    # -- Constrói o chart de Produto com maior ticket médio por região
    ticket_rank = (
        region_product_df
        .sort_values(['customer_region', 'avg_ticket'], ascending=[True, False])
        .groupby('customer_region').head(1)
        .reset_index()
    )
    ticket_fig = px.bar(
        ticket_rank,
        x='customer_region',
        y='avg_ticket',
        color='product_name',
        title='Produto de maior ticket médio por região',
        labels={'customer_region': 'Região', 'avg_ticket': 'Ticket médio', 'product_name': 'Produto'}
    )

    return {'orders_fig': orders_fig, 'income_fig': income_fig, 'ticket_fig':ticket_fig}

#=====================================
#--- 04 ANÁLISE DOS DIAS DA SEMANA ---
#=====================================

@st.cache_data
def build_weekday_avg_income(weekday_metrics: pd.DataFrame) -> go.Figure:
    return px.bar(
        weekday_metrics,
        x='weekday_name',
        y='avg_income',
        title='Faturamento médio por dia de semana',
        labels={'weekday_name': '', 'avg_income': 'Faturamento médio (R$)'}
    )

@st.cache_data
def build_weekday_avg_orders_amt(weekday_metrics: pd.DataFrame) -> go.Figure:
    return px.bar(
        weekday_metrics,
        x='weekday_name',
        y='avg_order_amt',
        title='Quantidade média de pedidos por dia de semana',
        labels={'weekday_name': '', 'avg_order_amt':'Quantidade média de pedidos'}
    )

@st.cache_data
def build_weekday_avg_ticket(weekday_metrics: pd.DataFrame) -> go.Figure:
    return px.bar(
        weekday_metrics,
        x='weekday_name',
        y='avg_ticket',
        title='Ticket médio por dia de semana',
        labels={'weekday_name': '', 'avg_ticket': 'Ticket médio (R$)'}
    )

if __name__ == '__main__':
    from data_processing import *
    df = grab_csv_data('data/vendas_linked_ps.csv')
    region_df = get_region_category_metrics(df)
    #print(region_df)
    build_region_category_charts(region_df)