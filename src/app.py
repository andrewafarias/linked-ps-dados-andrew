import streamlit as st
import data_processing as dp
import charts
from utils import currency_format


def render_sales_overview_panel(sales_data):
    st.header("Visão Geral")

    cancel_rate = dp.get_cancel_rate(sales_data)
    orders_amt = dp.get_orders_amt(sales_data)

    # Remove os pedidos cancelados para não influenciar as métricas posteriores.
    sales_data = sales_data[sales_data['order_status'] != 'Cancelado']

    total_income = dp.get_total_income(sales_data)
    avg_ticket = dp.get_avg_ticket(sales_data)

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
        card_avg_ticket = st.container(border=True)
        with card_avg_ticket:
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
        period_df = dp.get_day_metrics(sales_data)
        period_figures = charts.build_period_charts(period_df, 'order_date')
    elif granularity == "Mensal":
        period_df = dp.get_month_metrics(sales_data)
        period_figures = charts.build_period_charts(period_df, 'month_name')
    else: # Trimestral
        period_df = dp.get_quarter_metrics(sales_data)
        period_figures = charts.build_period_charts(period_df, 'order_quarter')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(period_figures['period_income'])
        st.plotly_chart(period_figures['period_avg_ticket'])
    
    with col2:
        st.plotly_chart(period_figures['period_orders_amt'])

    

def render_products_and_categories_panel(sales_data):
    st.header("Produtos e Categorias")

    analysis_metric = st.radio(
        'Métrica de análise:',
        ['Faturamento', 'Volume', 'Ticket Médio'],
        horizontal=True,
        key='metric_selector'
    )

    product_metrics = dp.get_product_metrics(sales_data)
    category_metrics = dp.get_category_metrics(sales_data)

    product_fig = None
    category_fig = None
    
    if analysis_metric == 'Faturamento':
        rank = product_metrics.sort_values(by='total_value', ascending=False).head(5).iloc[::-1]
        product_fig = charts.build_product_rank_income(rank)
        category_fig = charts.build_category_proportion_income(category_metrics.sort_values(by='total_value', ascending=False))

    elif analysis_metric == 'Volume':
        rank = product_metrics.sort_values(by='quantity', ascending=False).head(5).iloc[::-1]
        product_fig = charts.build_product_rank_orders_amt(rank)
        category_fig = charts.build_category_proportion_orders_amt(category_metrics.sort_values(by='quantity', ascending=False))
        
    else: # analysis_metric == 'Ticket Médio'
        rank = product_metrics.sort_values(by='avg_ticket', ascending=False).head(5).iloc[::-1]
        product_fig = charts.build_product_rank_avg_ticket(rank)
        avg_ticket = dp.get_avg_ticket(sales_data)
        category_fig = charts.build_category_proportion_avg_ticket(category_metrics.sort_values(by='avg_ticket', ascending=False), avg_ticket)

    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(product_fig)
    with col2: st.plotly_chart(category_fig)

def render_geographical_distribution_panel(sales_data):
    st.header('Distribuição Geográfica das Vendas')
    region_df = dp.get_region_metrics(sales_data)
    
    col1, col2, col3 = st.columns(3)

    # Coluna de faturamento por região
    with col1:

        # Faz cartão de maior faturamento
        container = st.container(border=True)
        with container:
            max_region_ind = region_df['total_value'].idxmax()
            best_region_name = region_df.loc[max_region_ind]['customer_region']
            best_region_avg_ticket = region_df.loc[max_region_ind]['total_value'].item()
            best_region_avg_ticket = currency_format(best_region_avg_ticket)
            st.metric('Maior faturamento', f'{best_region_name}', delta_description=best_region_avg_ticket)

        # Plota gráfico de faturamento por região
        fig = charts.build_regions_income(region_df)
        st.plotly_chart(fig)
    
    # Coluna de pedidos por região
    with col2:

        # Faz cartão de maior volume de pedidos
        container = st.container(border=True)
        with container:
            max_region_ind = region_df['order_id'].idxmax()
            best_region_name = region_df.loc[max_region_ind]['customer_region']
            best_region_orders_amt = str(region_df.loc[max_region_ind]['order_id'].item())
            best_region_orders_amt += " pedidos"
            st.metric('Maior volume de pedidos', f'{best_region_name}', delta_description=best_region_orders_amt)
        
        # Plota gráfico de volume de pedidos por região
        fig = charts.build_regions_orders_amt(region_df)
        st.plotly_chart(fig)
    
    # Coluna de ticket médio por região
    with col3:

        # Faz cartão de maior ticket médio
        container = st.container(border=True)
        with container:
            max_region_ind = region_df['avg_ticket'].idxmax()
            best_region_name = region_df.loc[max_region_ind]['customer_region']
            best_region_avg_ticket = region_df.loc[max_region_ind]['avg_ticket'].item()
            best_region_avg_ticket = currency_format(best_region_avg_ticket) + " por compra"
            st.metric('Maior ticket médio', f'{best_region_name}', delta_description=best_region_avg_ticket)

        # Plota gráfico de ticket médio por região
        fig = charts.build_regions_avg_ticket(region_df)
        st.plotly_chart(fig)
    
    opt = st.radio(
        'Escolha o atributo a ser analisado por região',
        ['Produto', 'Categoria'],
        horizontal=True,
        key='type_selector'
    )


    if opt == 'Categoria':
        # === GRÁFICOS DE MAIOR CATEGORIA POR REGIÃO ===
        # st.subheader('Categorias por região')
        
        region_category_df = dp.get_region_category_metrics(sales_data)
        figs = charts.build_region_category_charts(region_category_df)

        col1, col2, col3 = st.columns(3)

        with col1: st.plotly_chart(figs['income_fig'])
        with col2: st.plotly_chart(figs['orders_fig'])
        with col3: st.plotly_chart(figs['ticket_fig'])
    else:
        # === GRÁFICOS DE MAIOR PRODUTO POR REGIÃO ===
        # st.subheader('Produtos por região')
        
        region_product_df = dp.get_region_product_metrics(sales_data)
        figs = charts.build_region_product_charts(region_product_df)

        col1, col2, col3 = st.columns(3)

        with col1: st.plotly_chart(figs['income_fig'])
        with col2: st.plotly_chart(figs['orders_fig'])
        with col3: st.plotly_chart(figs['ticket_fig'])

def render_weekday_analysis(sales_data):
    st.header('Dias da Semana')

    weekday_df = dp.get_weekday_metrics(sales_data)
    income, order_amt, avg_ticket = (
        charts.build_weekday_avg_income(weekday_df),
        charts.build_weekday_avg_orders_amt(weekday_df),
        charts.build_weekday_avg_ticket(weekday_df),
    )

    col1, col2, col3 = st.columns(3)
    with col1: st.plotly_chart(income)
    with col2: st.plotly_chart(order_amt)
    with col3: st.plotly_chart(avg_ticket)

def render_insights_and_conclusions(sales_data):
    st.header('Insights')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(
            title='O e-commerce está crescendo!',
            icon='📈',
            body=
                'Através dos gráficos de faturamento e volume por trimestre, observamos uma tendência ' \
                'geral de crescimento, não isolada somente ao final do ano (que normalmente se espera ' \
                'um aumento). Entretanto, seria interessante ter dados de outros anos para saber se nã' \
                'o é um comportamento cíclico.')
        
        st.success(
            title='Os produtos de maior valor estão sendo bem aproveitados',
            icon='🎯',
            body=
                'Percebe-se que, em geral, os produtos e categorias de maior ticket médio são també' \
                'm aqueles que mais dão faturamento. Assim, não há um produto de grande valor co' \
                'm potencial mal aproveitado. Somente foge a esta regra o "Tênis de Corrida Nike", ' \
                'que talvez precise de mais anúncios.'
        )

        st.success(
            title='A plataforma consegue sua rentabilidade por produtos de alto valor',
            icon='💵',
            body=
                'É possível notar, pelos gráficos de rank de produtos, que os de maior faturamento ' \
                'são o de maior preço unitário. Isso diminui os custos logísticos de entrega!'
        )
    
    with col2:
        st.warning(
            title='Há uma possível falta de anúncios para o natal',
            icon='🎁',
            body=
                'Pelo gráfico de pedidos por dia do ano, nota-se que as compras de presentes para'    \
                ' o natal ocorrem em sua maioria no dia 23, um dia antes da véspera. A não ser que o' \
                ' frete seja extremamente rápido, isso significa que o e-commerce está captando some' \
                'nte aqueles que se esqueceram de comprar os presentes a tempo. Pode ser interessan'  \
                'te anunciar os produtos com uma antecedência maior, captando uma quantidade maior '  \
                'de compradores.'
        )

        st.warning(
            title='A plataforma não está tendo um bom alcance',
            icon='🙈',
            body=
                'Percebe-se um baixo volume de pedidos, pela média dos dias da semana. Enquanto iss' \
                'o seria esperado de um estabelecimento que vende somente produtos de valor agregad' \
                'o, não é o caso de um e-commerce de produtos diversos. É necessário aumentar o alc' \
                'ance da plataforma com anúncios, promoções ou outras formas.'
        )

        st.warning(
            title='O e-commerce não está aproveitando o dia do consumidor',
            icon='🛒',
            body=
                'O dia do consumidor (15 de março), que é o de maior ticket médio do ano, não é um ' \
                'dos de maior faturamento. A plataforma precisa investir mais em marketing para apr' \
                'oveitar este dia.'
        )

    with col3:
        st.info(
            title='Não há um dia privilegiado de compras',
            icon='🛍️',
            body=
                'Pelo o que se observa dos gráficos dos dias da semana, todas as métricas relaciona' \
                'das não se diferenciam significativamente entre os dias. Portanto, a plataforma pa' \
                'rar em algum dia específico não causaria mais dano do que em outro.'
        )
        
        st.info(
            title='Maneiras de otimizar o tempo de entrega e faturamento',
            icon='🛵',
            body= 
                'Analisando os gráficos de pedidos de produtos e categorias por região, pode-se otimiz' \
                'ar o tempo de entrega distribuindo os produtos em centros de distribuição estratégico' \
                's, de acordo com a região em que são mais pedidos. Por exemplo, distribuir mais ele'   \
                'trônicos para os centros na região Sudeste, mais "Tapete Sala 2x3m" para o Nordeste, ' \
                'etc.'
        )
        st.info(
            title='Maneiras de otimizar o faturamento',
            icon='💰',
            body= 
                'Análogo à otimização do tempo de entrega, pode-se aumentar o faturamento observand' \
                'o os produtos de maior ticket médio em cada região e os anunciando em seus' \
                ' respectivos lugares de destaque. Por exemplo, anunciar produtos de esporte ao nor' \
                'deste pode ter um alto retorno, por ser uma categoria com grande ticket médio nessa' \
                ' região.'
        )

def main():
    sales_data = dp.grab_csv_data('data/vendas_linked_ps.csv')
    
    st.set_page_config(
        page_title="Andrew - Desafio de Dados",
        page_icon="📊",
        layout="wide"
    )
    
    st.logo('.streamlit/logo.png', )

    st.title("Dashboard de Desempenho de Pedidos")

    # 01 VISÃO GERAL DE VENDAS
    render_sales_overview_panel(sales_data)
    sales_data = sales_data[sales_data['order_status'] != 'Cancelado'] # Gambiarra

    # 02 ANÁLISE POR PRODUTO E CATEGORIA
    render_products_and_categories_panel(sales_data)

    # 03 DISTRIBUIÇÃO GEOGRÁFICA
    render_geographical_distribution_panel(sales_data)

    # 04 ANÁLISE SEMANAL
    render_weekday_analysis(sales_data)

    # 05 INSGHTS E CONCLUSÕES
    render_insights_and_conclusions(sales_data)
    
    

if __name__ == '__main__':
    main()