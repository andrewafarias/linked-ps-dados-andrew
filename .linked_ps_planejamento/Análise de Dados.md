# Variáveis



| **Variável**         | **Dtype** | **Não-Nulos** | **Média** | **Mín** | **Máx** | **Categorias / Valores Possíveis**                      | **Detalhes Adicionais**           |
| -------------------- | --------- | ------------- | --------- | ------- | ------- | ------------------------------------------------------- | --------------------------------- |
| **order_id**         | `str`     | 1200          |           |         |         |                                                         | ID único do pedido.               |
| **order_date**       | `str`     | 1200          |           |         |         |                                                         | Todos os pedidos feitos em 2024.  |
| **product_category** | `str`     | 1200          |           |         |         | `Beleza`, `Esportes`, `Moda`, `Livros`, `Casa e Jardim` | 6 categorias no total.            |
| **product_name**     | `str`     | 1200          |           |         |         |                                                         | 41 tipos de produtos distintos.   |
| **quantity**         | `int64`   | 1200          | 1.72      | 1.00    | 5.00    |                                                         | Quantidade de produtos no pedido. |
| **unit_price**       | `float64` | 1200          | 185.37    | 26.28   | 1635.01 |                                                         | Preço por unidade.                |
| **total_value**      | `float64` | 1200          | 312.70    | 26.28   | 7407.35 |                                                         | Valor total do pedido.            |
| **customer_region**  | `str`     | 1200          |           |         |         | `Nordeste`, `Sul`, `Sudeste`, `Norte`, `Centro-Oeste`   | Região nacional do cliente.       |
| **payment_method**   | `str`     | 1200          |           |         |         | `Cartao`, `PIX`, `Boleto`                               | Método de pagamento.              |
| **order_status**     | `str`     | 1200          |           |         |         | `Entregue`, `Em transito`, `Cancelado`                  | Status atual do pedido.           |

 0. order_id (str): id do pedido
 1. order_date (str): data do pedido
	 - Todos os pedidos foram feitos em 2024
 2. product_category  (str): categoria do pedido
	 - 6 categorias no total: Beleza, Esportes, Moda, Livros, 'Casa e Jardim'.
 3. product_name (str): nome do produto do pedido
	 -  41 tipos de produtos distintos no total foram vendidos em um ano.
 4. quantity (int64): quantidade de produtos no pedido
 5. unit_price float64: preço por unidade
 6. total_value float64: valor total do pedido
 7. customer_region str: região nacional do cliente
	 1. ['Nordeste', 'Sul', 'Sudeste', 'Norte', 'Centro-Oeste']
 8. payment_method str: método de pagamento
	 1. ['Cartao', 'PIX', 'Boleto']
 9. order_status str: se foi entregue ou cancelado
	 1. ['Entregue', 'Em transito', 'Cancelado']

          quantity   unit_price  total_value
count  1200.000000  1200.000000  1200.000000
mean      1.720833   185.368233   312.699400
std       1.006849   270.472143   521.207179
min       1.000000    26.280000    26.280000
25%       1.000000    53.297500    84.187500
50%       1.000000   118.295000   159.870000
75%       2.000000   187.597500   329.155000
max       5.000000  1635.010000  7407.350000

 ==================== 

 #   Column            Non-Null Count  Dtype  
---  ------            --------------  -----  
 0   order_id          1200 non-null   str    
 1   order_date        1200 non-null   str    
 2   product_category  1200 non-null   str    
 3   product_name      1200 non-null   str    
 4   quantity          1200 non-null   int64  
 5   unit_price        1200 non-null   float64
 6   total_value       1200 non-null   float64
 7   customer_region   1200 non-null   str    
 8   payment_method    1200 non-null   str    
 9   order_status      1200 non-null   str    

Aqui está a tabela reestruturada com colunas dedicadas para cada tipo de métrica e metadado. As células que não se aplicam a determinadas variáveis (como estatísticas numéricas para textos ou listas de categorias para números) foram deixadas em branco.

# Produtos vendidos
--- Produtos distintos que foram vendidos
<ArrowStringArray>
[                  'Cabo HDMI 2m',  'Pinceis de Maquiagem Kit 12pc',
          'Tênis de Corrida Nike',             'Tapete de Yoga 6mm',
      'Teclado Mecânico Redragon',                  'Boné Snapback',
               'Meia Kit 3 pares',             'Pai Rico Pai Pobre',
              'Algoritmos - CLRS',             'Garrafa Térmica 1L',
         'Camisa Social Slim Fit',           'Regador de Jardim 5L',
   'Sapiens - Uma Breve Historia',               'A Startup Enxuta',
  'Smartphone Samsung Galaxy A54',               'Tapete Sala 2x3m',
             'Calça Jeans Skinny',       'Kit Ferramentas 42 peças',
         'Vassoura Elétrica Robô',                     'Clean Code',
        'Kit Skincare Vitamina C',               'Hub USB 7 portas',
        'Perfume Masculino 100ml',     'Shampoo Antirresíduo 300ml',
           'Webcam Full HD 1080p',         'Mouse Sem Fio Logitech',
        'Bolsa Feminina de Couro',          'Protetor Solar FPS 60',
     'Panela de Pressão Elétrica',         'Tênis Casual Masculino',
          'Luminária LED de Mesa', 'Secador de Cabelo Profissional',
         'Carregador Turbo USB-C',            'Vestido Floral Midi',
    'Jogo de Cama Queen 300 fios',           'Corda de Pular Speed',
         'Bicicleta Speed Aro 29',              'Whey Protein 900g',
   'Fone de Ouvido Bluetooth JBL',               'Halteres Par 5kg',
              'O Poder do Hábito']
Length: 41, dtype: str