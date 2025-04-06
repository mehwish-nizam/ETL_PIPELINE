from pymongo import MongoClient
import pandas as pd
import json


def load_data_to_mongo(df):
    with open("config/db_config.json") as f:
        config = json.load(f)
    client = MongoClient(config["mongodb_uri"])
    db = client["mobile_store"]
    collection = db["consolidated_data"]
    df.drop(columns=["_id"], errors="ignore", inplace=True)
    collection.insert_many(df.to_dict("records"))
    print("Data loaded successfully")

if __name__ == "__main__":
    df = pd.read_csv("output/final_cleaned_data.csv")
    load_data_to_mongo(df)
