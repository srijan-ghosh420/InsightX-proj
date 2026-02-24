import pandas as pd
import sqlite3
import os

# ==============================
# STEP 1: LOAD DATASET
# ==============================

print("Loading dataset...")

df = pd.read_csv("insightx_transactions.csv")

df.rename(columns={'amount (INR)': 'transaction_amount'}, inplace=True)

# Clean column names automatically
df.columns = (
    df.columns
    .str.strip()              # remove leading/trailing spaces
    .str.lower()              # convert to lowercase
    .str.replace(" ", "_")    # replace spaces with underscores
)

print(f"Total Rows Loaded: {len(df)}")
print("\nNormalized Columns:")
print(df.columns.tolist())

required_columns = [
    'transaction_type',
    'merchant_category',
    'receiver_age_group',
    'fraud_flag',
    'hour_of_day',
    'transaction_amount',
    'transaction_status',
    'device_type',
    'network_type',
    'is_weekend'
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise Exception(f"Missing required columns: {missing}")

# ==============================
# STEP 2: CLEAN NULL VALUES
# ==============================

print("\nCleaning dataset based on business rules...")

# Clean merchant_category for P2P
df.loc[df['transaction_type'] == 'P2P', 'merchant_category'] = \
    df.loc[df['transaction_type'] == 'P2P', 'merchant_category'].fillna('N/A (P2P)')

# Clean receiver_age_group for P2M
df.loc[df['transaction_type'] == 'P2M', 'receiver_age_group'] = \
    df.loc[df['transaction_type'] == 'P2M', 'receiver_age_group'].fillna('N/A (Merchant)')

# Ensure fraud_flag is integer
df['fraud_flag'] = df['fraud_flag'].fillna(0).astype(int)

# Optional: Ensure is_weekend is integer
df['is_weekend'] = df['is_weekend'].astype(int)


# ==============================
# STEP 3: FEATURE ENGINEERING
# ==============================

print("\nCreating derived columns...")

def categorize_time(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour <= 23:
        return 'Peak Evening'
    else:
        return 'Late Night'

# Add time_block
df['time_block'] = df['hour_of_day'].apply(categorize_time)

# Add high value flag (₹5000+)
df['is_high_value'] = (df['transaction_amount'] >= 5000).astype(int)

print("Feature engineering complete.")


# ==============================
# STEP 4: CREATE SQLITE DATABASE
# ==============================

print("\nCreating SQLite database...")

conn = sqlite3.connect('transactions'
'.db')

df.to_sql('transactions', conn, if_exists='replace', index=False)

print("Database successfully created: transactions.db")


# ==============================
# STEP 5: GROUND TRUTH QUERIES
# ==============================

print("\nRunning Ground Truth Queries...\n")

cursor = conn.cursor()

# ----------------------------------
# Query 1: Overall Failure Rate
# ----------------------------------
cursor.execute("""
    SELECT 
        ROUND(
            (SUM(CASE WHEN transaction_status = 'FAILED' THEN 1 ELSE 0 END) * 100.0) 
            / COUNT(*), 2
        ) AS failure_rate_percentage
    FROM transactions;
""")

failure_rate = cursor.fetchone()[0]
print(f"Ground Truth Failure Rate: {failure_rate}%")

# ----------------------------------
# Query 2: Top 3 Flagged Merchant Categories
# ----------------------------------
cursor.execute("""
    SELECT 
        merchant_category, 
        COUNT(*) as flagged_count 
    FROM transactions 
    WHERE fraud_flag = 1 
      AND transaction_type = 'P2M'
    GROUP BY merchant_category 
    ORDER BY flagged_count DESC 
    LIMIT 3;
""")

top_categories = cursor.fetchall()

print("\nTop 3 Flagged Merchant Categories:")
for category in top_categories:
    print(category)

# ----------------------------------
# Query 3: Android + 5G + Weekend Failure Rate
# ----------------------------------
cursor.execute("""
    SELECT 
        ROUND(
            (SUM(CASE WHEN transaction_status = 'FAILED' THEN 1 ELSE 0 END) * 100.0) 
            / COUNT(*), 2
        ) AS android_5g_weekend_failure_rate
    FROM transactions 
    WHERE device_type = 'Android' 
      AND network_type = '5G' 
      AND is_weekend = 1;
""")

android_failure = cursor.fetchone()[0]
print(f"\nAndroid/5G/Weekend Failure Rate: {android_failure}%")

conn.close()

print("\nAll Ground Truth queries executed successfully.")