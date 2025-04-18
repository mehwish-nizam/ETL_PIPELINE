# -*- coding: utf-8 -*-
"""BDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nu8r6Ca_jNhY0YGoXuT106y_XoozEynn
"""

# from google.colab import drive
# drive.mount('/content/drive')
# pip install pymongo
import pymongo
from pymongo import MongoClient
import pandas as pd
import requests

import json
with open("config/db_config.json") as f:
    config = json.load(f)

mongo_uri = config["mongodb_uri"]
api_url = config["api_url"]

# Source 1: SpreadSheet
df_sales = pd.read_excel('data/mobile_sales.xlsx')
# Source 2: JSON file
df_reviews = pd.read_json('data/customer_reviews.json')
# Source 3: CSV file
df_marketplace = pd.read_csv('data/marketplace_sales.csv')
# Source 4: MongoDb
client = MongoClient(mongo_uri)
db = client["mobile_store"]
collection = db["inventory"]
# Source 5: Rest API created using FastApi
api_url = api_url
print("Collection exists:", collection)
print("Connection test:", collection.find_one())

df_inventory = pd.DataFrame(list(collection.find()))

response = requests.get(api_url)  # Gradio APIs use POST requests
if response.status_code == 200:
    data = response.json()["data"]  # Extract data from Gradio response
    df_pricing = pd.DataFrame(data)  # Convert to Pandas DataFrame
    print(df_pricing.head())  # Display first 5 rows
else:
    print(f"API Error: {response.status_code}, {response.text}")



# Check All 5 sources data is loaded
print(df_pricing.head())
print(df_marketplace.head())
print(df_sales.head())
print(df_reviews.head())
print(df_inventory.head())

#************* Data Cleaning ****************
# Handling Missing Values
df_sales.fillna(df_sales.median(numeric_only=True), inplace=True)
df_marketplace.fillna(df_marketplace.median(numeric_only=True), inplace=True)
df_reviews.fillna("Unknown", inplace=True)
df_inventory.fillna("Unknown", inplace=True)
df_pricing.fillna("Unknown", inplace=True)

# Remove Duplicates

df_sales.drop_duplicates(inplace=True)
df_marketplace.drop_duplicates(inplace=True)
df_reviews.drop_duplicates(inplace=True)
df_inventory.drop_duplicates(inplace=True)
df_pricing.drop_duplicates(inplace=True)


#************* Data Normalization ****************

# Convert Dates to Standard Format (ISO 8601 - UTC)

df_sales["Date"] = pd.to_datetime(df_sales["Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
df_marketplace["Date"] = pd.to_datetime(df_marketplace["Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
df_inventory["Last Restocked Date"] = pd.to_datetime(df_inventory["Last Restocked Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

# Standardize Product Names
df_sales["Phone Model"] = df_sales["Phone Model"].str.title()
df_marketplace["Model"] = df_marketplace["Model"].str.title()
df_reviews["Model"] = df_reviews["Model"].str.title()
df_inventory["Model"] = df_inventory["Model"].str.title()
df_pricing["model"] = df_pricing["model"].str.title()

#************* Data Aggregation ****************

# Calculate Total Sales Per Model
df_sales_agg = df_sales.groupby("Phone Model").agg({"Units Sold": "sum", "Revenue (USD)": "sum"}).reset_index()

# Calculate Average Rating Per Model
df_reviews_agg = df_reviews.groupby("Model").agg({"Rating": "mean"}).reset_index()
df_reviews_agg.rename(columns={"Model": "Phone Model", "Rating": "Average Rating"}, inplace=True)

# Merge Inventory Data (Sales vs Stock)
df_sales_inventory = df_sales_agg.merge(df_inventory, left_on="Phone Model", right_on="Model", how="left").drop(columns=["Model"])
df_sales_inventory.rename(columns={"Stock Available": "Remaining Stock"}, inplace=True)


#************* Feature Engineering ****************

# Calculate Revenue Per Unit
df_sales["Revenue Per Unit"] = df_sales["Revenue (USD)"] / df_sales["Units Sold"]

# Classify Customer Sentiment
df_reviews["Sentiment"] = df_reviews["Rating"].apply(lambda x: "Positive" if x >= 4 else "Neutral" if x == 3 else "Negative")

#************* Standardize Measurement Units ****************
exchange_rates = {"EUR": 1.1, "GBP": 1.3, "INR": 0.012, "USD": 1}
df_sales["Revenue (USD)"] = df_sales["Revenue (USD)"].apply(lambda x: x * exchange_rates["USD"])

#************* Timestamp Standardization ****************

df_sales["Date"] = pd.to_datetime(df_sales["Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
df_marketplace["Date"] = pd.to_datetime(df_marketplace["Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
df_inventory["Last Restocked Date"] = pd.to_datetime(df_inventory["Last Restocked Date"]).dt.strftime('%Y-%m-%dT%H:%M:%SZ')

#************* Categorize Data Types ****************

df_pricing.rename(columns={"model": "Phone Model", "competitor": "Competitor Name", "price": "Competitor Price"}, inplace=True)

#************* Data Validation ****************

# Flag records with:
# Negative sales figures
# Zero or negative prices
df_sales = df_sales[df_sales["Units Sold"] > 0]
df_pricing = df_pricing[df_pricing["Competitor Price"] > 0]


#************* Data Aggregation ****************

# We summarize key statistics:
#     Total revenue per model
#     Average customer rating
#     Remaining stock levels
df_final = df_sales_agg.merge(df_reviews_agg, on="Phone Model", how="left")
df_final = df_final.merge(df_sales_inventory, on="Phone Model", how="left")
# df_final = df_final.merge(df_ pricing, on="Phone Model", how="left")

#************* Data Consolidation ****************
df_final.to_csv("output/final_cleaned_data.csv", index=False)


