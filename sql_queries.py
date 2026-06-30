import sqlite3
import pandas as pd

conn = sqlite3.connect('sql/dmart.db')

queries = {}

queries['Q1_top10_discounted_categories'] = """
SELECT Category, ROUND(AVG(Discount_Pct),2) AS Avg_Discount_Pct, COUNT(*) AS SKU_Count
FROM products
GROUP BY Category
ORDER BY Avg_Discount_Pct DESC
LIMIT 10;
"""

queries['Q2_brands_highest_avg_price'] = """
SELECT Brand, ROUND(AVG(Price),2) AS Avg_Price, COUNT(*) AS SKU_Count
FROM products
GROUP BY Brand
HAVING COUNT(*) >= 5
ORDER BY Avg_Price DESC
LIMIT 10;
"""

queries['Q3_subcategories_most_skus'] = """
SELECT SubCategory, Category, COUNT(*) AS SKU_Count
FROM products
GROUP BY SubCategory, Category
ORDER BY SKU_Count DESC
LIMIT 10;
"""

queries['Q4_products_above_category_avg_price'] = """
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
"""

queries['Q5_brand_concentration_per_category'] = """
SELECT Category, Brand, COUNT(*) AS SKU_Count,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY Category), 2) AS Pct_of_Category
FROM products
GROUP BY Category, Brand
HAVING SKU_Count > 10
ORDER BY Pct_of_Category DESC
LIMIT 10;
"""

queries['Q6_zero_discount_products_count'] = """
SELECT Category, COUNT(*) AS Zero_Discount_Products
FROM products
WHERE Discount_Pct = 0
GROUP BY Category
ORDER BY Zero_Discount_Products DESC
LIMIT 10;
"""

queries['Q7_price_band_distribution_by_category'] = """
SELECT Category, Price_Band, COUNT(*) AS SKU_Count
FROM products
WHERE Category IN ('Personal Care','Packaged Food','Grocery','Home & Kitchen','Dairy & Beverages')
GROUP BY Category, Price_Band
ORDER BY Category, SKU_Count DESC;
"""

queries['Q8_top_discounted_individual_products'] = """
SELECT Name, Brand, Category, Price, DiscountedPrice, Discount_Pct
FROM products
ORDER BY Discount_Pct DESC
LIMIT 10;
"""

results = {}
with open('sql/query_results.md', 'w') as out:
    out.write("# SQL Business Query Results — DMart Product Catalog\n\n")
    for name, q in queries.items():
        df = pd.read_sql_query(q, conn)
        results[name] = df
        out.write(f"## {name.replace('_',' ')}\n\n```sql\n{q.strip()}\n```\n\n")
        out.write(df.to_markdown(index=False))
        out.write("\n\n")
        print(f"--- {name} ---")
        print(df.to_string(index=False))
        print()

conn.close()
