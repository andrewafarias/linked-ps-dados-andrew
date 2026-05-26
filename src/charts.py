import streamlit as st
import plotly.express as px


def _build_period_charts(period_df, x_: str) -> dict:
    return {
        'period_income': px.line(period_df, x=x_, y='income', title='Evolução do Faturamento'),
        'period_orders_amt': px.line(period_df, x=x_, y='orders_amt', title='Evolução dos Pedidos'),
        'period_avgticket': px.line(period_df, x=x_, y='avg_ticket', title='Evolução do Ticket Médio'),
    }

@st.cache_data
def build_charts(dataset: dict) -> dict:
    period_charts = {
        'Diário': _build_period_charts(dataset['day_summary'], 'order_date'),
        'Mensal': _build_period_charts(dataset['month_summary'], 'month_name'),
        'Trimestral': _build_period_charts(dataset['quarter_summary'], 'order_quarter'),
    }

    product_rank_income = px.bar(
        dataset['product_rank_income'],
        x='total_value',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Faturamento'
    )
    product_rank_orders_amt = px.bar(
        dataset['product_rank_orders_amt'],
        x='order_id',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos Mais Pedidos'
    )
    product_rank_avgticket = px.bar(
        dataset['product_rank_avgticket'],
        x='avg_ticket',
        y='product_name',
        orientation='h',
        title='Top 5 Produtos com Maior Ticket Médio'
    )

    category_proportion_income = px.pie(
        dataset['category_proportion_income'],
        names='product_category',
        values='total_value',
        title='Faturamento por Categoria'
    )
    category_proportion_orders_amt = px.pie(
        dataset['category_proportion_orders_amt'],
        names='product_category',
        values='order_id',
        title='Pedidos por Categoria'
    )
    category_proportion_avgticket = px.bar(
        dataset['category_proportion_avgticket'],
        x='avg_ticket',
        y='product_category',
        orientation='h',
        title='Ticket Médio por Categoria',
        color='product_category'
    )
    category_proportion_avgticket.add_vline(
        x=dataset['avg_ticket'],
        line_dash='dash',
        annotation_text='Ticket Médio global'
    )

    return {
        'period_charts': period_charts,
        'product_rank_income': product_rank_income,
        'product_rank_orders_amt': product_rank_orders_amt,
        'product_rank_avgticket': product_rank_avgticket,
        'category_proportion_income': category_proportion_income,
        'category_proportion_orders_amt': category_proportion_orders_amt,
        'category_proportion_avgticket': category_proportion_avgticket,
    }