

/*10 produtos mais vendidos*/  
 
WITH Recent_Sales AS (
    SELECT 
        ProductKey,
        SUM(OrderQuantity) AS TotalQuantitySold
    FROM 
        (
            SELECT * FROM AdventureWorks_Sales2016
            UNION ALL
            SELECT * FROM AdventureWorks_Sales2017
        ) AS Sales
    GROUP BY 
        ProductKey
),
Bike_Products AS (
    SELECT 
        p.ProductKey,
        p.ProductName
    FROM 
        AdventureWorks_Products p
    JOIN 
        AdventureWorks_Product_Subcategories ps ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey
    JOIN 
        AdventureWorks_Product_Categories pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
    WHERE 
        pc.CategoryName = 'Bikes'
)
SELECT 
    bp.ProductName,
    rs.TotalQuantitySold
FROM 
    Recent_Sales rs
JOIN 
    Bike_Products bp ON rs.ProductKey = bp.ProductKey
ORDER BY 
    rs.TotalQuantitySold DESC
LIMIT 10;



/*Cliente com maior número de compras no trimestre*/ 
  
WITH Orders_Per_Quarter AS (
    SELECT 
        CustomerKey,
        QUARTER(STR_TO_DATE(OrderDate, '%d/%m/%Y')) AS OrderQuarter,
        COUNT(OrderNumber) AS OrderCount
    FROM 
        AdventureWorks_Sales2017
    GROUP BY 
        CustomerKey, 
        QUARTER(STR_TO_DATE(OrderDate, '%d/%m/%Y'))
),
Customers_With_Orders_In_All_Quarters AS (
    SELECT 
        CustomerKey,
        COUNT(DISTINCT OrderQuarter) AS QuartersWithOrders
    FROM 
        Orders_Per_Quarter
    GROUP BY 
        CustomerKey
    HAVING 
        COUNT(DISTINCT OrderQuarter) = 2
),
Total_Orders_Per_Customer AS (
    SELECT 
        o.CustomerKey, 
        SUM(o.OrderCount) AS TotalOrders
    FROM 
        Orders_Per_Quarter o
    JOIN 
        Customers_With_Orders_In_All_Quarters c 
        ON o.CustomerKey = c.CustomerKey
    GROUP BY 
        o.CustomerKey
)
SELECT 
    c.CustomerKey, 
    c.FirstName, 
    c.LastName, 
    t.TotalOrders
FROM 
    AdventureWorks_Customers c
JOIN 
    Total_Orders_Per_Customer t 
    ON c.CustomerKey = t.CustomerKey
ORDER BY 
    t.TotalOrders DESC
LIMIT 1;


/*Mês onde ocorre maior número de vendas*/   

WITH Monthly_Sales AS (
    SELECT 
        YEAR(STR_TO_DATE(OrderDate, '%d/%m/%Y')) AS OrderYear,
        MONTH(STR_TO_DATE(OrderDate, '%d/%m/%Y')) AS OrderMonth,
        SUM(OrderQuantity * p.ProductPrice) AS TotalSales,
        AVG(OrderQuantity * p.ProductPrice) AS AverageSalesPerOrder
    FROM 
        (
            SELECT * FROM AdventureWorks_Sales2015
            UNION ALL
            SELECT * FROM AdventureWorks_Sales2016
            UNION ALL
            SELECT * FROM AdventureWorks_Sales2017
        ) AS Sales
    JOIN 
        AdventureWorks_Products p ON Sales.ProductKey = p.ProductKey
    GROUP BY 
        OrderYear,
        OrderMonth
    HAVING 
        AVG(OrderQuantity * p.ProductPrice) > 500
)
SELECT 
    OrderYear,
    OrderMonth, 
    TotalSales
FROM 
    Monthly_Sales
ORDER BY 
    TotalSales DESC
LIMIT 1;


/*Territórios que mais venderam e tiveram crescimento*/ 

WITH Sales_2017 AS (
    SELECT 
        TerritoryKey,
        SUM(OrderQuantity * p.ProductPrice) AS TotalSales2017
    FROM 
        AdventureWorks_Sales2017 s
    JOIN 
        AdventureWorks_Products p ON s.ProductKey = p.ProductKey
    GROUP BY 
        TerritoryKey
),
Sales_2016 AS (
    SELECT 
        TerritoryKey,
        SUM(OrderQuantity * p.ProductPrice) AS TotalSales2016
    FROM 
        AdventureWorks_Sales2016 s
    JOIN 
        AdventureWorks_Products p ON s.ProductKey = p.ProductKey
    GROUP BY 
        TerritoryKey
),
Sales_Growth AS (
    SELECT 
        s2017.TerritoryKey,
        s2017.TotalSales2017,
        s2016.TotalSales2016,
        (s2017.TotalSales2017 - s2016.TotalSales2016) / s2016.TotalSales2016 * 100 AS SalesGrowth
    FROM 
        Sales_2017 s2017
    JOIN 
        Sales_2016 s2016 ON s2017.TerritoryKey = s2016.TerritoryKey
),
Sales_Above_Average AS (
    SELECT 
        TerritoryKey,
        TotalSales2017
    FROM 
        Sales_2017
    WHERE 
        TotalSales2017 > (SELECT AVG(TotalSales2017) FROM Sales_2017)
)
SELECT 
    t.TerritoryKey,
    tr.Region,
    tr.Country,
    tr.Continent,
    sg.TotalSales2017,
    sg.SalesGrowth
FROM 
    Sales_Above_Average t
JOIN 
    Sales_Growth sg ON t.TerritoryKey = sg.TerritoryKey
JOIN 
    AdventureWorks_Territories tr ON t.TerritoryKey = tr.SalesTerritoryKey
WHERE 
    sg.SalesGrowth > 10;

   
/*Territórios que estavam abaixo da média e voltaram*/  
   
WITH Sales_2017 AS (
    SELECT 
        TerritoryKey,
        SUM(OrderQuantity * p.ProductPrice) AS TotalSales2017
    FROM 
        AdventureWorks_Sales2017 s
    JOIN 
        AdventureWorks_Products p ON s.ProductKey = p.ProductKey
    GROUP BY 
        TerritoryKey
),
Sales_2016 AS (
    SELECT 
        TerritoryKey,
        SUM(OrderQuantity * p.ProductPrice) AS TotalSales2016
    FROM 
        AdventureWorks_Sales2016 s
    JOIN 
        AdventureWorks_Products p ON s.ProductKey = p.ProductKey
    GROUP BY 
        TerritoryKey
),
Sales_Growth AS (
    SELECT 
        s2017.TerritoryKey,
        s2017.TotalSales2017,
        s2016.TotalSales2016,
        (s2017.TotalSales2017 - s2016.TotalSales2016) / s2016.TotalSales2016 * 100 AS SalesGrowth
    FROM 
        Sales_2017 s2017
    JOIN 
        Sales_2016 s2016 ON s2017.TerritoryKey = s2016.TerritoryKey
),
Below_Average_Sales_2016 AS (
    SELECT 
        TerritoryKey,
        TotalSales2016
    FROM 
        Sales_2016
    WHERE 
        TotalSales2016 < (SELECT AVG(TotalSales2016) FROM Sales_2016)
)
SELECT 
    sg.TerritoryKey,
    tr.Region,
    tr.Country,
    tr.Continent,
    sg.SalesGrowth
FROM 
    Sales_Growth sg
JOIN 
    Below_Average_Sales_2016 bas ON sg.TerritoryKey = bas.TerritoryKey
JOIN 
    AdventureWorks_Territories tr ON sg.TerritoryKey = tr.SalesTerritoryKey
ORDER BY 
    sg.SalesGrowth DESC;
