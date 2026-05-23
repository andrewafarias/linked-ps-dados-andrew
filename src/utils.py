import pandas as pd

month_translator = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

def print_data_info(filepath: str):
    sales_data = pd.read_csv(filepath)
    
    print('--- Resumo da Tabela:')
    print(sales_data)
    print('\n', 20*'=', '\n')

    print('--- Informações')
    print(sales_data.info())
    print('\n', 20*'=', '\n')

    print('--- Estatísticas básicas')
    print(sales_data.describe())
    print('\n', 20*'=', '\n')

    print('--- Categorias de produtos vendidos:')
    categories_list = sales_data['product_category'].unique()
    print(categories_list)
    print('\n', 20*'=', '\n')

    print('--- Produtos distintos que foram vendidos')
    products_sold = sales_data['product_name'].unique()
    print(products_sold)
    print('\n', 20*'=', '\n')

    print('--- Verificação de se todas as vendas ocorreram em 2024')
    dates: list[str] = sales_data['order_date'].to_list()
    for dt in dates:
        year, *_ = dt.split('-')
        year = int(year)
        if(year != 2024):
            print("Ano diferente de 2024 encontrado!!!", year)
    print('Verificação finalizada.')
    print('\n', 20*'=', '\n')

    print('--- Regiões com venda')
    regions = sales_data['customer_region'].unique()
    print(regions)
    print('\n', 20*'=', '\n')

    print('--- Métodos de pagamento utilizados')
    paym_methods = sales_data['payment_method'].unique()
    print(paym_methods)
    print('\n', 20*'=', '\n')

    print('--- Status de entrega')
    order_statuses = sales_data['order_status'].unique()
    print(order_statuses)
    print('\n', 20*'=', '\n')

def grab_csv_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

if __name__ == '__main__':
    # print_data_info('data/vendas_linked_ps.csv')
    df = pd.read_csv('data/vendas_linked_ps.csv')
    canceled_orders = df.loc[df['order_status'] == 'Cancelado']
    print(canceled_orders, '\n', canceled_orders['order_id'].count())