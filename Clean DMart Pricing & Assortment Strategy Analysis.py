import pandas as pd
import numpy as np
import re

df = pd.read_csv('data/DMart_raw.csv')
print("Raw shape:", df.shape)

# 1. Drop fully empty / near-duplicate rows
df = df.dropna(subset=['Name', 'Price'])

# 2. Fix Category using BreadCrumbs where Category looks like a brand name (data scraping error)
bad_categories = ['Zebronics','Geep','Butterfly','Wonderchef','Syska','Pigeon','Joyo Plastics']
electronics_keywords = ['charg','plug','adapter','earphone','bluetooth','headphone','speaker','cable','usb']

def fix_category(row):
    cat = row['Category']
    if cat in bad_categories or pd.isna(cat):
        name = str(row['Name']).lower()
        if any(k in name for k in electronics_keywords):
            return 'Electronics & Accessories'
        elif cat in ['Butterfly','Wonderchef','Pigeon']:
            return 'Home & Kitchen'
        else:
            return 'Home & Kitchen'
    return cat

df['Category'] = df.apply(fix_category, axis=1)

# Roll up near-duplicate categories (e.g. 'DMart Grocery' -> 'Grocery')
df['Category'] = df['Category'].replace({'DMart Grocery': 'Grocery', 'Specials': 'Grocery'})

# 3. Clean SubCategory using BreadCrumbs second segment when available
def clean_subcat(row):
    sub = row['SubCategory']
    if pd.isna(sub):
        bc = str(row['BreadCrumbs'])
        if '>' in bc:
            return bc.split('>')[-1].strip()
        return 'Uncategorized'
    # remove redundant prefix like 'Grocery/Dry Fruits' -> 'Dry Fruits'
    if '/' in str(sub):
        return str(sub).split('/')[-1].strip()
    return sub

df['SubCategory'] = df.apply(clean_subcat, axis=1)

# 4. Parse Quantity into numeric value + standardized unit
def parse_quantity(q):
    if pd.isna(q):
        return np.nan, np.nan
    q = str(q).strip().lower().replace(' ', '')
    # handle patterns like 2x1l, 5kg, 500gm, 4pcs, 5u
    m = re.match(r'(\d+)x(\d+\.?\d*)(\w+)', q)
    if m:
        mult, val, unit = m.groups()
        return float(mult) * float(val), unit
    m = re.match(r'(\d+\.?\d*)(\w+)', q)
    if m:
        val, unit = m.groups()
        return float(val), unit
    return np.nan, np.nan

parsed = df['Quantity'].apply(parse_quantity)
df['Qty_Value'] = parsed.apply(lambda x: x[0])
df['Qty_Unit_Raw'] = parsed.apply(lambda x: x[1])

unit_map = {
    'gm':'g','g':'g','kg':'kg','ml':'ml','l':'L','ltr':'L',
    'pcs':'pcs','pc':'pcs','u':'unit','units':'unit'
}
df['Qty_Unit'] = df['Qty_Unit_Raw'].map(unit_map).fillna(df['Qty_Unit_Raw'])

# Standardize to grams/ml for weight/volume comparison (Standard_Qty_g_ml)
def standardize(row):
    val, unit = row['Qty_Value'], row['Qty_Unit']
    if pd.isna(val):
        return np.nan
    if unit == 'kg':
        return val * 1000
    if unit == 'L':
        return val * 1000
    if unit in ['g','ml']:
        return val
    return np.nan  # pcs/unit not comparable to weight

df['Standard_Qty'] = df.apply(standardize, axis=1)

# 5. Clean Origin (Description column is really "Country of Origin" when short; else noise)
def clean_origin(desc):
    if pd.isna(desc):
        return 'Not Specified'
    desc = str(desc).strip()
    if len(desc) <= 20 and ' ' not in desc.strip():
        return desc
    return 'Not Specified'

df['Origin'] = df['Description'].apply(clean_origin)
df = df.drop(columns=['Description', 'Qty_Unit_Raw'])

# 6. Discount calculations
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['DiscountedPrice'] = pd.to_numeric(df['DiscountedPrice'], errors='coerce')
df = df.dropna(subset=['Price','DiscountedPrice'])
df = df[df['Price'] > 0]

df['Discount_Amount'] = df['Price'] - df['DiscountedPrice']
df['Discount_Pct'] = (df['Discount_Amount'] / df['Price'] * 100).round(2)
df['Discount_Pct'] = df['Discount_Pct'].clip(lower=0)  # guard against negative/bad data

# 7. Price band / positioning tier
def price_band(p):
    if p < 100: return 'Budget (<100)'
    elif p < 300: return 'Mid (100-300)'
    elif p < 700: return 'Upper-Mid (300-700)'
    else: return 'Premium (700+)'
df['Price_Band'] = df['DiscountedPrice'].apply(price_band)

# 8. Clean Brand (strip whitespace, fill missing as 'Unbranded/DMart')
df['Brand'] = df['Brand'].fillna('Unbranded/DMart').str.strip()
df['Name'] = df['Name'].str.strip()

# 9. Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before-len(df)} exact duplicate rows")

# Reorder columns
cols = ['Name','Brand','Category','SubCategory','Price','DiscountedPrice',
        'Discount_Amount','Discount_Pct','Price_Band','Qty_Value','Qty_Unit',
        'Standard_Qty','Origin','BreadCrumbs']
df = df[cols]

df.to_csv('data/DMart_clean.csv', index=False)
print("Clean shape:", df.shape)
print(df.head(3).to_string())
print("\nNulls remaining:\n", df.isnull().sum())
