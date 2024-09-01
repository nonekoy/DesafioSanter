

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Leitura das tabelas
customers = pd.read_csv('./desafio1/adventure/AdventureWorks_Customers.csv', parse_dates=['BirthDate'], dayfirst=True, encoding='ISO-8859-1')
product_categories = pd.read_csv('./desafio1/adventure/AdventureWorks_Product_Categories.csv')
product_subcategories = pd.read_csv('./desafio1/adventure/AdventureWorks_Product_Subcategories.csv')
products = pd.read_csv('./desafio1/adventure/AdventureWorks_Products.csv')
returns = pd.read_csv('./desafio1/adventure/AdventureWorks_Returns.csv', parse_dates=['ReturnDate'], dayfirst=True)
sales_2015 = pd.read_csv('./desafio1/adventure/AdventureWorks_Sales_2015.csv', parse_dates=['OrderDate', 'StockDate'], dayfirst=True)
sales_2016 = pd.read_csv('./desafio1/adventure/AdventureWorks_Sales_2016.csv', parse_dates=['OrderDate', 'StockDate'], dayfirst=True)
sales_2017 = pd.read_csv('./desafio1/adventure/AdventureWorks_Sales_2017.csv', parse_dates=['OrderDate', 'StockDate'], dayfirst=True)
territories = pd.read_csv('./desafio1/adventure/AdventureWorks_Territories.csv')



# Combina os dados em uma tabela só
sales_data = pd.concat([sales_2015, sales_2016, sales_2017])

# Converter OrderDate para datetime, permitindo formatos mistos, sem isso a tabela não é lida corretamente
sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'], format='mixed', dayfirst=True)

# Agrupar as vendas mensais somando apenas a coluna numérica relevante (OrderQuantity)
monthly_sales = sales_data.groupby(sales_data['OrderDate'].dt.to_period('M')).agg({'OrderQuantity': 'sum'}).reset_index()

# Converter de volta para datetime ou string para fins de plotagem
monthly_sales['OrderDate'] = monthly_sales['OrderDate'].dt.to_timestamp()

# Gráfico de linha
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x='OrderDate', y='OrderQuantity', marker='o')

# Adicionando linha de tendência
sns.regplot(data=monthly_sales, x=monthly_sales['OrderDate'].dt.month, y='OrderQuantity', scatter=False, color='red', order=2)

plt.title('Tendência Mensal das Vendas Totais')
plt.xlabel('Mês')
plt.ylabel('Quantidade Vendida')
#plt.show()




# Filtrar produtos da categoria "Bikes"
bikes_category_key = product_categories[product_categories['CategoryName'] == 'Bikes']['ProductCategoryKey'].values[0]
bikes_products = products[products['ProductSubcategoryKey'].isin(
    product_subcategories[product_subcategories['ProductCategoryKey'] == bikes_category_key]['ProductSubcategoryKey']
)]

# Somar vendas e calcular lucro por produto
bikes_sales = sales_data[sales_data['ProductKey'].isin(bikes_products['ProductKey'])]
bikes_sales_summary = bikes_sales.groupby('ProductKey').agg({
    'OrderQuantity': 'sum'
}).reset_index()

# Mesclar com informações do produto
bikes_sales_summary = bikes_sales_summary.merge(products[['ProductKey', 'ProductName', 'ProductPrice', 'ProductCost']], on='ProductKey')

# Calcular o lucro por produto
bikes_sales_summary['TotalRevenue'] = bikes_sales_summary['OrderQuantity'] * bikes_sales_summary['ProductPrice']
bikes_sales_summary['TotalCost'] = bikes_sales_summary['OrderQuantity'] * bikes_sales_summary['ProductCost']
bikes_sales_summary['Profit'] = bikes_sales_summary['TotalRevenue'] - bikes_sales_summary['TotalCost']

# Ordenar e selecionar os 10 mais vendidos
top_10_bikes = bikes_sales_summary.sort_values(by='OrderQuantity', ascending=False).head(10)

# Gráfico de barras
plt.figure(figsize=(12, 6))
sns.barplot(data=top_10_bikes, x='ProductName', y='OrderQuantity', color='skyblue', label='Quantidade Vendida')
sns.barplot(data=top_10_bikes, x='ProductName', y='Profit', color='darkblue', label='Lucro')

plt.title('Top 10 Produtos Mais Vendidos na Categoria "Bicicletas"')
plt.xlabel('Produto')
plt.ylabel('Quantidade Vendida e Lucro')
plt.xticks(rotation=45)
plt.legend()
#plt.show()


# Exemplo de filtro para uma categoria específica, como "Bicicletas"
# Adiciona uma coluna de mês com base na coluna de data
sales_data['Month'] = sales_data['OrderDate'].dt.to_period('M')

# Exemplo de filtro para uma categoria específica (opcional)
selected_category_key = product_categories[product_categories['CategoryName'].str.lower() == 'Bikes'.lower()]['ProductCategoryKey'].values[0]
filtered_products = products[products['ProductSubcategoryKey'].isin(
    product_subcategories[product_subcategories['ProductCategoryKey'] == selected_category_key]['ProductSubcategoryKey'])]

# Filtrar vendas relacionadas à categoria selecionada
filtered_sales = sales_data[sales_data['ProductKey'].isin(filtered_products['ProductKey'])]

# Agrupar as vendas por região e por mês, somando a quantidade de pedidos
sales_by_region_month = filtered_sales.groupby(['TerritoryKey', 'Month'])['OrderQuantity'].sum().unstack()

# Mesclar com as regiões para obter os nomes das regiões
sales_by_region_month = sales_by_region_month.merge(territories[['SalesTerritoryKey', 'Region']], left_index=True, right_on='SalesTerritoryKey')
sales_by_region_month.set_index('Region', inplace=True)
sales_by_region_month.drop('SalesTerritoryKey', axis=1, inplace=True)

# Criar o mapa de calor
plt.figure(figsize=(12, 8))
sns.heatmap(sales_by_region_month, cmap='coolwarm', annot=True, fmt='.0f')
plt.title('Vendas por Região e Mês')
plt.xlabel('Mês')
plt.ylabel('Região')
#plt.show()




# Somar número de vendas e valor total por cliente
customer_sales = sales_data.groupby('CustomerKey').agg({
    'OrderQuantity': 'sum',
    'OrderLineItem': 'sum'  # Assumindo que isso seja o valor total (ou multiplique OrderQuantity por ProductPrice)
}).reset_index()

# Gráfico de dispersão
plt.figure(figsize=(10, 6))
sns.scatterplot(data=customer_sales, x='OrderQuantity', y='OrderLineItem', color='blue')

# Adicionar linha de regressão
sns.regplot(data=customer_sales, x='OrderQuantity', y='OrderLineItem', scatter=False, color='red')

plt.title('Relação entre Número de Vendas e Valor Total por Cliente')
plt.xlabel('Número de Vendas')
plt.ylabel('Valor Total das Vendas')
#plt.show()




# Resumir as vendas mensais por categoria de produto
# Converter OrderDate para datetime
sales_2016['OrderDate'] = pd.to_datetime(sales_2016['OrderDate'], format='%d/%m/%Y', errors='coerce')
sales_2017['OrderDate'] = pd.to_datetime(sales_2017['OrderDate'], format='%d/%m/%Y', errors='coerce')

# Extrair o mês e ano das datas
sales_2016['Month'] = sales_2016['OrderDate'].dt.to_period('M')
sales_2017['Month'] = sales_2017['OrderDate'].dt.to_period('M')

# Agrupar vendas por mês e produto
sales_2016_grouped = sales_2016.groupby(['Month', 'ProductKey'])['OrderQuantity'].sum().reset_index()
sales_2017_grouped = sales_2017.groupby(['Month', 'ProductKey'])['OrderQuantity'].sum().reset_index()

# Verificar as colunas do DataFrame products
print("Colunas disponíveis em products:")
print(products.columns)

# Juntar as vendas com produtos para obter a categoria
sales_2016_with_products = sales_2016_grouped.merge(products[['ProductKey', 'ProductSubcategoryKey']], on='ProductKey')
sales_2017_with_products = sales_2017_grouped.merge(products[['ProductKey', 'ProductSubcategoryKey']], on='ProductKey')

# Juntar com a tabela de categorias para obter o nome da categoria
sales_2016_with_category = sales_2016_with_products.merge(product_categories[['ProductCategoryKey', 'CategoryName']], left_on='ProductSubcategoryKey', right_on='ProductCategoryKey', how='left')
sales_2017_with_category = sales_2017_with_products.merge(product_categories[['ProductCategoryKey', 'CategoryName']], left_on='ProductSubcategoryKey', right_on='ProductCategoryKey', how='left')

# Agrupar vendas por mês e categoria
sales_2016_by_category_month = sales_2016_with_category.groupby(['Month', 'CategoryName'])['OrderQuantity'].sum().unstack(fill_value=0)
sales_2017_by_category_month = sales_2017_with_category.groupby(['Month', 'CategoryName'])['OrderQuantity'].sum().unstack(fill_value=0)

# Plotar gráfico de barras empilhadas
fig, ax = plt.subplots(figsize=(14, 8))

# Plotar dados de 2016
sales_2016_by_category_month.plot(kind='bar', stacked=True, ax=ax, position=0, width=0.4, color=sns.color_palette("tab20", len(sales_2016_by_category_month.columns)), label='2016')

# Plotar dados de 2017
sales_2017_by_category_month.plot(kind='bar', stacked=True, ax=ax, position=1, width=0.4, color=sns.color_palette("tab20", len(sales_2017_by_category_month.columns)), label='2017')

plt.title('Comparação das Vendas Mensais por Categoria de Produto - 2016 vs 2017')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Vendas')
plt.legend(title='Ano')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()