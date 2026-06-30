"""
MongoDB Aggregation Pipeline Queries - DMart Product Catalog
Uses mongomock (in-memory MongoDB-compatible engine) since this environment has no
live DB network access. Swap `import mongomock` -> `import pymongo` and connect to
a real MongoDB URI to run identically against a live server.
"""
import pandas as pd
import mongomock
import json

df = pd.read_csv('data/DMart_clean.csv')
records = df.to_dict('records')

client = mongomock.MongoClient()
db = client['dmart_db']
db.products.insert_many(records)
print(f"Inserted {db.products.count_documents({})} documents into products collection\n")

results_log = []

def run(name, pipeline):
    res = list(db.products.aggregate(pipeline))
    results_log.append({'query': name, 'pipeline': pipeline, 'result': res})
    print(f"--- {name} ---")
    for r in res[:10]:
        print(r)
    print()

# Q1: Average discount % by category (mirrors SQL Q1)
run("Q1_avg_discount_by_category", [
    {"$group": {"_id": "$Category", "avg_discount_pct": {"$avg": "$Discount_Pct"}, "sku_count": {"$sum": 1}}},
    {"$sort": {"avg_discount_pct": -1}},
    {"$limit": 10}
])

# Q2: Top brands by average price (min 5 SKUs)
run("Q2_top_brands_avg_price", [
    {"$group": {"_id": "$Brand", "avg_price": {"$avg": "$Price"}, "sku_count": {"$sum": 1}}},
    {"$match": {"sku_count": {"$gte": 5}}},
    {"$sort": {"avg_price": -1}},
    {"$limit": 10}
])

# Q3: Brand concentration per category (top brand share)
run("Q3_brand_concentration", [
    {"$group": {"_id": {"category": "$Category", "brand": "$Brand"}, "sku_count": {"$sum": 1}}},
    {"$match": {"sku_count": {"$gt": 10}}},
    {"$sort": {"sku_count": -1}},
    {"$limit": 10}
])

# Q4: Most common price band per category (faceted)
run("Q4_price_band_distribution", [
    {"$match": {"Category": {"$in": ["Personal Care", "Packaged Food", "Grocery"]}}},
    {"$group": {"_id": {"category": "$Category", "band": "$Price_Band"}, "count": {"$sum": 1}}},
    {"$sort": {"_id.category": 1, "count": -1}}
])

# Q5: Top 10 most discounted individual products
run("Q5_top_discounted_products", [
    {"$sort": {"Discount_Pct": -1}},
    {"$limit": 10},
    {"$project": {"_id": 0, "Name": 1, "Brand": 1, "Category": 1, "Price": 1,
                  "DiscountedPrice": 1, "Discount_Pct": 1}}
])

with open('mongo/mongo_results.json', 'w') as f:
    json.dump(results_log, f, indent=2, default=str)

print("Saved full results to mongo/mongo_results.json")
