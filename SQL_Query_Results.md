# SQL Business Query Results — DMart Product Catalog

## Q1 top10 discounted categories

```sql
SELECT Category, ROUND(AVG(Discount_Pct),2) AS Avg_Discount_Pct, COUNT(*) AS SKU_Count
FROM products
GROUP BY Category
ORDER BY Avg_Discount_Pct DESC
LIMIT 10;
```

| Category                  |   Avg_Discount_Pct |   SKU_Count |
|:--------------------------|-------------------:|------------:|
| Electronics & Accessories |              59.87 |           7 |
| Smartwatches              |              58.34 |           1 |
| Backpacks                 |              51.73 |          13 |
| Computer Accessories      |              37.62 |           2 |
| Clothing & Accessories    |              32.36 |          97 |
| Appliances                |              31.65 |          53 |
| Plant Container           |              30.97 |          23 |
| Beauty & Cosmetics        |              29.15 |          46 |
| Home & Kitchen            |              29.11 |         886 |
| Packaged Food             |              28.68 |        1124 |

## Q2 brands highest avg price

```sql
SELECT Brand, ROUND(AVG(Price),2) AS Avg_Price, COUNT(*) AS SKU_Count
FROM products
GROUP BY Brand
HAVING COUNT(*) >= 5
ORDER BY Avg_Price DESC
LIMIT 10;
```

| Brand            |   Avg_Price |   SKU_Count |
|:-----------------|------------:|------------:|
| Boat             |     3275.71 |           7 |
| Wonderchef       |     2970    |          10 |
| Usha             |     2398    |          10 |
| Crompton Greaves |     2304.45 |          11 |
| Prestige         |     2158.93 |          14 |
| Raymond          |     2099    |           8 |
| Portronics       |     2094    |          10 |
| Bajaj            |     2009.35 |          17 |
| Wildcraft        |     1908.38 |           8 |
| Pigeon           |     1700.23 |          13 |

## Q3 subcategories most skus

```sql
SELECT SubCategory, Category, COUNT(*) AS SKU_Count
FROM products
GROUP BY SubCategory, Category
ORDER BY SKU_Count DESC
LIMIT 10;
```

| SubCategory      | Category          |   SKU_Count |
|:-----------------|:------------------|------------:|
| Snacks & Farsans | Packaged Food     |         302 |
| Masala & Spices  | Grocery           |         297 |
| Beverages        | Dairy & Beverages |         282 |
| Skin Care        | Personal Care     |         221 |
| Face Care        | Personal Care     |         164 |
| Hair Care        | Personal Care     |         160 |
| Specials         | Grocery           |         157 |
| Dairy            | Dairy & Beverages |         147 |
| Bed & Bath       | Home & Kitchen    |         146 |
| Packaged Food    | Packaged Food     |         135 |

## Q4 products above category avg price

```sql
WITH cat_avg AS (
    SELECT Category, AVG(Price) AS avg_price
    FROM products
    GROUP BY Category
)
SELECT p.Name, p.Brand, p.Category, p.Price, ROUND(c.avg_price,2) AS Category_Avg_Price
FROM products p
JOIN cat_avg c ON p.Category = c.Category
WHERE p.Price > c.avg_price * 3
ORDER BY p.Price DESC
LIMIT 10;
```

| Name                                             | Brand      | Category       |   Price |   Category_Avg_Price |
|:-------------------------------------------------|:-----------|:---------------|--------:|---------------------:|
| Philips UV-C Disinfection System                 | Philips    | Home & Kitchen |   10990 |               503.45 |
| Bathla Advance 5 Step Ladder-Orange              | Bathla     | Home & Kitchen |    8999 |               503.45 |
| Godrej Goldilocks Personal White Locker          | Godrej     | Home & Kitchen |    7669 |               503.45 |
| Bathla Advance 4 Step Ladder-Orange              | Bathla     | Home & Kitchen |    6799 |               503.45 |
| Borges Extra Light Olive Oil                     | Borges     | Grocery        |    5500 |               394.09 |
| Wonderchef Nutri-Blend Black                     | Wonderchef | Home & Kitchen |    5300 |               503.45 |
| Boat Black Stone 650R Bluetooth Speaker          | Boat       | Grocery        |    4990 |               394.09 |
| Wonderchef Non-Stick Burlington Set : 5 Pieces   | Wonderchef | Grocery        |    4900 |               394.09 |
| Butterfly Stainless Steel Outer Lid Curve Cooker | Butterfly  | Home & Kitchen |    4851 |               503.45 |
| Figaro Olive Oil Tin                             | Figaro     | Grocery        |    4500 |               394.09 |

## Q5 brand concentration per category

```sql
SELECT Category, Brand, COUNT(*) AS SKU_Count,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY Category), 2) AS Pct_of_Category
FROM products
GROUP BY Category, Brand
HAVING SKU_Count > 10
ORDER BY Pct_of_Category DESC
LIMIT 10;
```

| Category               | Brand           |   SKU_Count |   Pct_of_Category |
|:-----------------------|:----------------|------------:|------------------:|
| Fruits & Vegetables    | Unbranded/DMart |          69 |            100    |
| Plant Container        | Unbranded/DMart |          23 |            100    |
| Raincoat               | Zeel            |          33 |            100    |
| School Supplies        | Navneet         |          11 |            100    |
| Tableware              | Unbranded/DMart |          17 |            100    |
| Dairy & Beverages      | Amul            |          60 |             39.47 |
| Clothing & Accessories | Feather Soft    |          23 |             29.87 |
| Clothing & Accessories | No Fuss         |          22 |             28.57 |
| Grocery                | Unbranded/DMart |         157 |             26.08 |
| Home & Kitchen         | Unbranded/DMart |         101 |             25.7  |

## Q6 zero discount products count

```sql
SELECT Category, COUNT(*) AS Zero_Discount_Products
FROM products
WHERE Discount_Pct = 0
GROUP BY Category
ORDER BY Zero_Discount_Products DESC
LIMIT 10;
```

| Category          |   Zero_Discount_Products |
|:------------------|-------------------------:|
| Dairy & Beverages |                        6 |
| Baby & Kids       |                        3 |
| Packaged Food     |                        1 |

## Q7 price band distribution by category

```sql
SELECT Category, Price_Band, COUNT(*) AS SKU_Count
FROM products
WHERE Category IN ('Personal Care','Packaged Food','Grocery','Home & Kitchen','Dairy & Beverages')
GROUP BY Category, Price_Band
ORDER BY Category, SKU_Count DESC;
```

| Category          | Price_Band          |   SKU_Count |
|:------------------|:--------------------|------------:|
| Dairy & Beverages | Budget (<100)       |         189 |
| Dairy & Beverages | Mid (100-300)       |         166 |
| Dairy & Beverages | Upper-Mid (300-700) |          66 |
| Dairy & Beverages | Premium (700+)      |           8 |
| Grocery           | Budget (<100)       |         499 |
| Grocery           | Mid (100-300)       |         318 |
| Grocery           | Upper-Mid (300-700) |         148 |
| Grocery           | Premium (700+)      |          93 |
| Home & Kitchen    | Mid (100-300)       |         353 |
| Home & Kitchen    | Budget (<100)       |         293 |
| Home & Kitchen    | Upper-Mid (300-700) |         145 |
| Home & Kitchen    | Premium (700+)      |          95 |
| Packaged Food     | Budget (<100)       |         726 |
| Packaged Food     | Mid (100-300)       |         339 |
| Packaged Food     | Upper-Mid (300-700) |          52 |
| Packaged Food     | Premium (700+)      |           7 |
| Personal Care     | Mid (100-300)       |         649 |
| Personal Care     | Budget (<100)       |         342 |
| Personal Care     | Upper-Mid (300-700) |         207 |
| Personal Care     | Premium (700+)      |          35 |

## Q8 top discounted individual products

```sql
SELECT Name, Brand, Category, Price, DiscountedPrice, Discount_Pct
FROM products
ORDER BY Discount_Pct DESC
LIMIT 10;
```

| Name                                                     | Brand           | Category                  |   Price |   DiscountedPrice |   Discount_Pct |
|:---------------------------------------------------------|:----------------|:--------------------------|--------:|------------------:|---------------:|
| Naagin Indian Hot Sauce - Original                       | Naagin          | Packaged Food             |      50 |                 1 |          98    |
| Naagin Indian Hot Sauce - Smoky Bhoot                    | Naagin          | Packaged Food             |      50 |                 1 |          98    |
| Naagin Indian Hot Sauce - Kantha Bomb                    | Naagin          | Packaged Food             |      50 |                 1 |          98    |
| Disposable FFP2 Face Mask                                | Unbranded/DMart | Grocery                   |     425 |                60 |          85.88 |
| Geep Micro USB High Speed Charging Cable (1 Metre)       | Geep            | Electronics & Accessories |     299 |                49 |          83.61 |
| Micro USB Charging Cable (1 Metre)                       | Unbranded/DMart | Home & Kitchen            |     249 |                49 |          80.32 |
| Zebronics Aux Cable ASC100                               | Zebronics       | Appliances                |     169 |                34 |          79.88 |
| Syska LED Bulb B22 6500K                                 | Syska           | Grocery                   |     329 |                73 |          77.81 |
| Dr.WaterR Stainless Steel Milk Frother                   | Dr.WaterR       | Home & Kitchen            |    1499 |               349 |          76.72 |
| Trident Comfort Living Bath Towel 380 GSM - Tango Tomato | Trident         | Grocery                   |     599 |               149 |          75.13 |

