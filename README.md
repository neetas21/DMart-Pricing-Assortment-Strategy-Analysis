# DMart Pricing & Assortment Strategy Analysis

A full data analytics project (EDA + SQL + MongoDB) built on a real DMart product catalog dataset, completed as a data analyst portfolio piece.

## Business Problem

DMart's product portfolio spans 5,000+ SKUs across 21 categories and 822 brands. This project analyzes pricing strategy, discount behavior, brand concentration, and assortment depth to surface insights leadership could act on \u2014 reframed from "sales trends" to **pricing & assortment strategy**, since the dataset is a real product catalog snapshot, not transactional sales history (no order dates, quantities sold, or customers).

## Dataset

- **Source:** Real DMart product catalog export, uploaded by user (`DMart.csv`)
- **Raw size:** 5,189 products, 9 columns
- **Clean size:** 5,181 products, 14 columns (after dropping duplicates/nulls)
- **Fields:** Name, Brand, Category, SubCategory, Price, DiscountedPrice, Discount Amount/%, Price Band, Quantity (parsed), Origin, BreadCrumbs

## Project Structure

```
clean_data.py          -> Cleans raw CSV, outputs DMart_clean.csv
eda.py                  -> Generates 8 EDA charts + summary_stats.json
sql_queries.py           -> Loads data into SQLite, runs 8 business SQL queries
mongo_queries.py         -> Mirrors SQL queries as MongoDB aggregation pipelines (via mongomock)
build_report.js           -> Generates the Word report (docx)
build_ppt.js              -> Generates the PowerPoint deck (pptx)

DMart_clean.csv            -> Cleaned dataset
SQL_Query_Results.md        -> All SQL query outputs
MongoDB_Query_Results.json   -> All MongoDB pipeline outputs
DMart_Analysis_Report.docx    -> Full written report
DMart_Analysis_Presentation.pptx -> Presentation deck
```

## How to Reproduce

```bash
pip install pandas matplotlib seaborn tabulate mongomock --break-system-packages

python clean_data.py      # Step 1: clean raw data
python eda.py              # Step 2: generate charts + stats
python sql_queries.py       # Step 3: run SQL business queries
python mongo_queries.py      # Step 4: run MongoDB aggregation pipelines

npm install -g docx pptxgenjs react-icons react react-dom sharp
node build_report.js        # Step 5: generate Word report
node build_ppt.js            # Step 6: generate PPTX deck
```

## Data Cleaning Highlights

- Fixed 13 rows where a brand name had been scraped into the `Category` field
- Standardized 21 inconsistent `SubCategory` labels using the `BreadCrumbs` hierarchy
- Parsed free-text `Quantity` ("500 gm", "2x1L") into numeric value + standardized unit
- Derived `Discount_Amount`, `Discount_Pct`, and `Price_Band` (Budget/Mid/Upper-Mid/Premium)
- Cleaned a noisy `Description` field (mixed country-of-origin tags and marketing paragraphs) into a clean `Origin` field

## Key Findings

1. **Discounting is category-tiered:** staples (Grocery, Packaged Food) average ~27\u201329% discount, while discretionary categories (Electronics, Backpacks) are discounted 50\u201360% \u2014 consistent with a margin-protection-on-staples, clearance-on-discretionary strategy.
2. **Private label dominates:** "Unbranded/DMart" is the single largest brand by SKU count (398) and holds 100% category share in Fruits & Vegetables, Plant Containers, and Tableware.
3. **Outlier pricing distorts category averages:** a handful of premium products (Rs.5,000+) sit in categories otherwise priced under Rs.500 on average.
4. **Value-led positioning:** the catalog is heavily weighted toward Budget and Mid price bands across all major categories.
5. **SQL and MongoDB results were cross-validated** and matched exactly, confirming query logic correctness across both paradigms.

## On the MongoDB / SQL Choice

The data is inherently relational, so **SQL (SQLite)** was used as the primary query layer. A **MongoDB aggregation pipeline bonus section** was added using `mongomock` (an in-memory MongoDB-compatible engine), since this environment has no live database network access. The pipeline syntax is identical to production MongoDB/Atlas \u2014 the same scripts run unchanged against a real MongoDB connection via `pymongo`.

## Next Steps / Future Scope

- Live BI dashboard (Power BI/Tableau) tracking category KPIs, discount outlier alerts, private-label share, and price-band mix over time
- If transactional data (orders, quantities sold, customer IDs) becomes available, extend into sales trend analysis, demand forecasting, and customer segmentation

