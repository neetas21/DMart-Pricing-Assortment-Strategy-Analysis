# DMart Pricing & Assortment Strategy Analysis

## About This Project

I built this project to practice end-to-end data analysis on a real, messy dataset rather than a pre-cleaned competition dataset. I sourced a real DMart product catalog export (5,181 SKUs after cleaning, spanning 21 categories and 822 brands) and used it to answer a practical retail business question using SQL, MongoDB, and standard EDA techniques.

## Why I Reframed the Business Problem

The dataset I found is a product catalog snapshot, not transactional sales data \u2014 there are no order dates, quantities sold, or customer IDs. Rather than simulate fake transactions to force a "sales trends" narrative, I chose to scope the analysis around what the data could actually support: **pricing strategy, discount behavior, and assortment composition**. I think this is the more honest and more useful approach \u2014 in real analyst work, you rarely get the dataset you wish you had, and knowing how to extract genuine insight from what's actually available is the real skill being tested.

## Business Problem

DMart's catalog spans 5,000+ SKUs and 800+ brands. I wanted to answer:
- Is DMart's discounting strategy consistent and deliberate across categories, or inconsistent?
- How exposed are categories to private-label vs. branded competition?
- Is assortment depth (SKUs per sub-category) balanced relative to category importance?
- Where are pricing outliers that could distort category-level benchmarks?

## What I Did

**1. Data Cleaning**
The raw data had real-world quirks I had to handle: 13 rows where a brand name had been scraped into the Category field, inconsistent sub-category labels, and a free-text Quantity field ("500 gm", "2x1L") that needed parsing into numeric values. I also derived discount percentage and price-band tiers (Budget / Mid / Upper-Mid / Premium) as new analytical fields.

**2. Exploratory Data Analysis**
I analyzed catalog composition, discount behavior by category, price distribution, brand concentration, and assortment depth, producing eight charts to support the findings.

**3. SQL Analysis**
I loaded the cleaned data into SQLite and wrote queries using GROUP BY aggregations, window functions, and joins to answer the business questions above.

**4. MongoDB Aggregation Pipeline (Bonus)**
To round out my querying skills, I re-ran the same business questions as MongoDB aggregation pipelines. I didn't have access to a live MongoDB server in my working environment, so I used `mongomock`, an in-memory library that replicates MongoDB's query engine \u2014 the pipeline syntax is identical to what I'd run against a live MongoDB/Atlas instance. Results matched my SQL output exactly, which I used as a cross-validation check on my own query logic.

**5. Reporting**
I packaged the findings into a formal Word report and a presentation deck, and closed both with a proposed scope for a live BI dashboard as a natural next phase of this work.

## Key Findings

- Discounting is clearly category-tiered: staples like Grocery and Packaged Food average ~27\u201329% discount, while discretionary categories like Electronics and Backpacks are discounted 50\u201360%, suggesting a margin-protection-on-staples / clearance-on-discretionary strategy.
- DMart's own private label ("Unbranded/DMart") is the single largest brand by SKU count and holds 100% category share in Fruits & Vegetables, Plant Containers, and Tableware \u2014 meaning zero branded competition in those segments.
- A small number of outlier-priced products (Rs.5,000+) sit in categories otherwise averaging under Rs.500, which distorts category-level pricing benchmarks if not handled separately.
- The catalog is heavily weighted toward Budget and Mid price bands across every major category, reflecting a clear value-retail positioning.

## Project Files

| File | Purpose |
|---|---|
| `clean_data.py` | Cleans the raw catalog and outputs `DMart_clean.csv` |
| `eda.py` | Generates all EDA charts and summary statistics |
| `sql_queries.py` | Loads data into SQLite and runs the business SQL queries |
| `mongo_queries.py` | Mirrors the SQL queries as MongoDB aggregation pipelines |
| `build_report.js` / `build_ppt.js` | Generate the Word report and PowerPoint deck |
| `DMart_clean.csv` | The cleaned dataset |
| `SQL_Query_Results.md` / `MongoDB_Query_Results.json` | Full query outputs |
| `DMart_Analysis_Report.docx` | Full written report |
| `DMart_Analysis_Presentation.pptx` | Presentation deck |

## How to Run It

```bash
pip install pandas matplotlib seaborn tabulate mongomock --break-system-packages

python clean_data.py
python eda.py
python sql_queries.py
python mongo_queries.py

npm install -g docx pptxgenjs react-icons react react-dom sharp
node build_report.js
node build_ppt.js
```

## Tools Used

Python (pandas, matplotlib, seaborn), SQLite, MongoDB aggregation pipelines, and Word/PowerPoint report generation.

## What I'd Do Next

If I get access to genuine transactional data (orders, quantities sold, timestamps) for this catalog, I'd extend this into sales trend analysis, demand forecasting, and customer segmentation. I'd also build out the dashboard concept I scoped at the end of the report into an actual live Power BI or Tableau view.
