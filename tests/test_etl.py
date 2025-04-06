import pandas as pd
import json
import pytest
from pymongo import MongoClient

# Fixture to load config
@pytest.fixture
def config():
    with open("config/db_config.json") as f:
        return json.load(f)

# Test MongoDB connection
def test_mongodb_connection(config):
    client = MongoClient(config["mongodb_uri"])
    db = client["mobile_store"]
    collection = db["inventory"]
    sample = collection.find_one()
    assert sample is not None, "MongoDB collection is empty or not reachable"

# Test API is reachable and returns data
def test_api_response(config):
    import requests
    response = requests.get(config["api_url"])
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

# Test that all input files exist and are readable
@pytest.mark.parametrize("path", [
    "data/mobile_sales.xlsx",
    "data/customer_reviews.json",
    "data/marketplace_sales.csv",
])
def test_input_files_exist(path):
    try:
        if path.endswith(".xlsx"):
            df = pd.read_excel(path)
        elif path.endswith(".json"):
            df = pd.read_json(path)
        elif path.endswith(".csv"):
            df = pd.read_csv(path)
        assert not df.empty
    except Exception as e:
        pytest.fail(f"Failed to load {path}: {e}")
