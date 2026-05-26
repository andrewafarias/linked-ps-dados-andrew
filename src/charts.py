import plotly.express as px


def build_charts(dataset: dict, period_df, x_: str) -> dict:
    figures = {
        'fig_period_income': px.line(period_df, x=x_, y='income', title='Evolução do Faturamento'),
        'fig_period_orders_amt': px.line(period_df, x=x_, y='orders_amt', title='Evolução dos Pedidos'),
        'fig_period_avgticket': px.line(period_df, x=x_, y='avg_ticket', title='Evolução do Ticket Médio'),
        'fig_product_rank_income': px.bar(
            dataset['product_rank_income'],
            x='total_value',
            y='product_name',
            orientation='h',
            title='Top 5 Produtos com Maior Faturamento'
        ),
        'fig_product_rank_orders_amt': px.bar(
            dataset['product_rank_orders_amt'],
            x='order_id',
            y='product_name',
            orientation='h',
            title='Top 5 Produtos Mais Pedidos'
        ),
        'fig_product_rank_avgticket': px.bar(
            dataset['product_rank_avgticket'],
            x='avg_ticket',
            y='product_name',
            orientation='h',
            title='Top 5 Produtos com Maior Ticket Médio'
        ),
        'fig_category_proportion_income': px.pie(
            dataset['category_proportion_income'],
            names='product_category',
            values='total_value',
            title='Faturamento por Categoria'
        ),
        'fig_category_proportion_orders_amt': px.pie(
            dataset['category_proportion_orders_amt'],
            names='product_category',
            values='order_id',
            title='Pedidos por Categoria'
        ),
        'fig_category_proportion_avgticket': px.bar(
            dataset['category_proportion_avgticket'],
            x='avg_ticket',
            y='product_category',
            orientation='h',
            title='Ticket Médio por Categoria',
            color='product_category'
        ),
    }
    figures['fig_category_proportion_avgticket'].add_vline(
        x=dataset['avg_ticket'],
        line_dash='dash',
        annotation_text='Ticket Médio global'
    )
    return figures