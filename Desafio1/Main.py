
import pandas as pd

# Exemplo de como carregar um arquivo CSV específico, por exemplo, 'Product.csv'
df_product = pd.read_csv('./adventure/AdventureWorks_Customers.csv')

# Visualizar as primeiras linhas do DataFrame para verificar a importação
print(df_product.head())