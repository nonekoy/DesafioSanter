

# Documentação dos scripts
## Visão geral

 Nesta pasta estão ad tabelas CSV retiradas com o script utilizado no mysql a partir do banco de dados "AdventureWorks".

Script: Script.sql

# Estrutura dos Scripts

## Quais são os 10 produtos mais vendidos (em quantidade) na categoria "Bikes", considerando apenas vendas feitas nos últimos dois anos?

Objetivo: Identificar os 10 produtos mais vendidos na categoria "Bikes" nos últimos dois anos (2016 e 2017), com base na quantidade vendida.
Decisões de Implementação:
CTEs: Foram usadas Common Table Expressions (CTEs) para dividir a lógica da consulta em partes gerenciáveis. Recent_Sales captura as vendas agregadas para cada produto em 2016 e 2017, enquanto Combined_Sales combina esses resultados para determinar as quantidades totais vendidas.
JOINs: Foram utilizados JOINs para unir as tabelas de vendas com as tabelas de produtos, subcategorias e categorias, filtrando por produtos da categoria "Bicicletas".
LIMIT: A consulta é ordenada pelas quantidades vendidas em ordem decrescente e limitada aos 10 produtos mais vendidos, garantindo que apenas os principais produtos sejam retornados.

10 produtos mais vendidos
nome do arquivo resultante- _WITH_Recent_Sales_AS_SELECT_ProductKey_SUM_OrderQuantity_AS_Tot_202409011330


## Cliente com o Maior Número de Pedidos Realizados

Objetivo: Identificar o cliente que realizou o maior número de pedidos, considerando apenas clientes que fizeram pelo menos um pedido em cada trimestre do último ano fiscal.
Decisões de Implementação:
CTEs: A consulta utiliza CTEs para identificar os clientes que fizeram pedidos em todos os trimestres do último ano fiscal. Em seguida, outra CTE é usada para calcular o número total de pedidos realizados por esses clientes.
Filtragem por Trimestre: A filtragem é feita para garantir que apenas os clientes que fizeram pedidos em todos os quatro trimestres do último ano fiscal sejam considerados.
Ordenação e Limite: A consulta final ordena os clientes pelo número total de pedidos em ordem decrescente, retornando o cliente com o maior número de pedidos.

Cliente com maior número de compras no trimestre
nome do arquivo resultante-_WITH_Orders_Per_Quarter_AS_SELECT_CustomerKey_QUARTER_STR_TO_DA_202409011330


## Mês com Maior Valor de Vendas (Receita Total) com Receita Média por Venda Acima de 500

Objetivo: Determinar o mês com o maior valor total de vendas, considerando apenas os meses em que a receita média por venda foi superior a 500 unidades monetárias.
Decisões de Implementação:
Subconsultas: A consulta utiliza subconsultas para calcular a receita média por venda por mês e para filtrar apenas os meses onde essa média foi superior a 500 unidades monetárias.
Agrupamento por Mês: A receita total é agrupada por mês, e os meses que atendem ao critério de receita média são selecionados.
Ordenação por Receita Total: A consulta final ordena os meses pela receita total em ordem decrescente, identificando o mês com maior valor de vendas.

Mês onde ocorre maior número de vendas
nome do arquivo resultante-monthly_sales_202409011331


## Territórios com Vendas Acima da Média e Crescimento Superior a 10%

Objetivo: Identificar os territórios que tiveram vendas acima da média no último ano fiscal e também apresentaram um crescimento de vendas superior a 10% em relação ao ano anterior.
Decisões de Implementação:
CTEs: As CTEs são usadas para calcular as vendas totais por território para os dois últimos anos fiscais, a média de vendas por território e o crescimento percentual de um ano para o outro.
Cálculo de Crescimento: A consulta calcula o crescimento percentual das vendas de cada território em relação ao ano anterior.
Filtragem por Crescimento e Vendas Acima da Média: A consulta final filtra apenas os territórios que tiveram um crescimento superior a 10% e cujas vendas ficaram acima da média, garantindo que apenas os territórios com desempenho excepcional sejam listados.

Territórios que mais venderam e tiveram crescimento
nome do arquivo resultante-_WITH_Sales_2017_AS_SELECT_TerritoryKey_SUM_OrderQuantity_p_Prod_202409011331


## Territórios que Estavam Abaixo da Média e Voltaram

Objetivo: Identificar os territórios que, em 2016, tiveram vendas totais abaixo da média, mas que mostraram um crescimento positivo de vendas em 2017.
Sales_2017: Calcula as vendas totais por território para o ano de 2017. O valor total de vendas é calculado multiplicando a quantidade vendida (OrderQuantity) pelo preço do produto (ProductPrice).
Sales_2016: Realiza o mesmo cálculo para o ano de 2016.
Sales_Growth: Calcula o crescimento percentual das vendas de 2017 em relação a 2016 para cada território, identificando se houve crescimento ou declínio.
Below_Average_Sales_2016: Identifica os territórios que tiveram vendas abaixo da média em 2016, utilizando uma subconsulta para calcular a média total de vendas de todos os territórios naquele ano.
O script realiza JOINs entre os resultados das CTEs e a tabela de territórios (AdventureWorks_Territories) para obter informações geográficas adicionais, como região, país e continente.
Apenas os territórios que estavam abaixo da média de vendas em 2016 e que apresentaram crescimento em 2017 são selecionados.
Os resultados são ordenados pelo percentual de crescimento (SalesGrowth) em ordem decrescente, destacando os territórios que mais se recuperaram.

Territórios que estavam abaixo da média e voltaram
nome do arquivo resultante-_WITH_Sales_2017_AS_SELECT_TerritoryKey_SUM_OrderQuantity_p_Prod_202409011331-1725208302183