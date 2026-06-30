import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 110

df = pd.read_csv('data/DMart_clean.csv')

# ---- 1. Category distribution (SKU count) ----
plt.figure(figsize=(9,5))
cat_counts = df['Category'].value_counts().head(10)
sns.barplot(x=cat_counts.values, y=cat_counts.index, palette='viridis')
plt.title('Top 10 Categories by Number of Products (SKU Count)')
plt.xlabel('Number of Products')
plt.tight_layout()
plt.savefig('charts/01_category_sku_count.png')
plt.close()

# ---- 2. Average discount % by category ----
plt.figure(figsize=(9,5))
disc_by_cat = df.groupby('Category')['Discount_Pct'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=disc_by_cat.values, y=disc_by_cat.index, palette='rocket')
plt.title('Average Discount % by Category (Top 10)')
plt.xlabel('Average Discount %')
plt.tight_layout()
plt.savefig('charts/02_avg_discount_by_category.png')
plt.close()

# ---- 3. Price distribution ----
plt.figure(figsize=(9,5))
sns.histplot(df['DiscountedPrice'].clip(upper=2000), bins=50, kde=True, color='teal')
plt.title('Distribution of Discounted Price (capped at ₹2000 for readability)')
plt.xlabel('Discounted Price (₹)')
plt.tight_layout()
plt.savefig('charts/03_price_distribution.png')
plt.close()

# ---- 4. Price band split ----
plt.figure(figsize=(7,7))
band_counts = df['Price_Band'].value_counts()
plt.pie(band_counts.values, labels=band_counts.index, autopct='%1.1f%%',
        colors=sns.color_palette('pastel'))
plt.title('Product Mix by Price Band')
plt.tight_layout()
plt.savefig('charts/04_price_band_split.png')
plt.close()

# ---- 5. Top 15 brands by SKU count ----
plt.figure(figsize=(9,6))
top_brands = df['Brand'].value_counts().head(15)
sns.barplot(x=top_brands.values, y=top_brands.index, palette='mako')
plt.title('Top 15 Brands by Number of SKUs Listed')
plt.xlabel('Number of SKUs')
plt.tight_layout()
plt.savefig('charts/05_top_brands.png')
plt.close()

# ---- 6. Brand concentration within top categories (HHI-style) ----
top_cats = df['Category'].value_counts().head(5).index
fig, axes = plt.subplots(1, 5, figsize=(20,5))
for ax, cat in zip(axes, top_cats):
    sub = df[df['Category']==cat]
    top5 = sub['Brand'].value_counts().head(5)
    ax.bar(top5.index, top5.values, color=sns.color_palette('crest', 5))
    ax.set_title(cat, fontsize=10)
    ax.tick_params(axis='x', rotation=60, labelsize=8)
plt.suptitle('Top 5 Brands within Top 5 Categories (Assortment Concentration)')
plt.tight_layout()
plt.savefig('charts/06_brand_concentration.png')
plt.close()

# ---- 7. Discount % vs Price (scatter) ----
plt.figure(figsize=(9,6))
sample = df.sample(min(1500, len(df)), random_state=42)
sns.scatterplot(data=sample, x='Price', y='Discount_Pct', hue='Category',
                 alpha=0.5, legend=False, palette='husl')
plt.xlim(0, 2000)
plt.title('Discount % vs Original Price (sample)')
plt.tight_layout()
plt.savefig('charts/07_discount_vs_price.png')
plt.close()

# ---- 8. SubCategory depth - top 15 ----
plt.figure(figsize=(9,6))
subcat_counts = df['SubCategory'].value_counts().head(15)
sns.barplot(x=subcat_counts.values, y=subcat_counts.index, palette='flare')
plt.title('Top 15 Sub-Categories by SKU Count (Assortment Depth)')
plt.xlabel('Number of Products')
plt.tight_layout()
plt.savefig('charts/08_subcategory_depth.png')
plt.close()

# ---- Summary stats for report ----
summary = {
    'total_skus': len(df),
    'total_categories': df['Category'].nunique(),
    'total_subcategories': df['SubCategory'].nunique(),
    'total_brands': df['Brand'].nunique(),
    'avg_price': round(df['Price'].mean(),2),
    'median_price': round(df['Price'].median(),2),
    'avg_discount_pct': round(df['Discount_Pct'].mean(),2),
    'median_discount_pct': round(df['Discount_Pct'].median(),2),
    'max_discount_pct': round(df['Discount_Pct'].max(),2),
    'pct_zero_discount': round((df['Discount_Pct']==0).mean()*100,2),
    'top_category': df['Category'].value_counts().idxmax(),
    'top_category_share_pct': round(df['Category'].value_counts(normalize=True).max()*100,2),
    'top_brand': df['Brand'].value_counts().idxmax(),
    'top_brand_skus': int(df['Brand'].value_counts().max()),
    'most_discounted_category': disc_by_cat.idxmax(),
    'most_discounted_category_pct': round(disc_by_cat.max(),2),
}
import json
with open('charts/summary_stats.json','w') as f:
    json.dump(summary, f, indent=2)

for k,v in summary.items():
    print(f"{k}: {v}")
