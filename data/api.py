# -*- coding: utf-8 -*-
"""API.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LRYOpUiGYtaXhsDy9772NWb37olTZWg3
"""

# !pip install fastapi uvicorn pyngrok nest-asyncio
# from google.colab import drive

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from pyngrok import ngrok
import nest_asyncio
import pandas as pd

# drive.mount('/content/drive')

# ngrok authtoken '2uyn7n3HKZWzId7Qa75cXvQwahe_467hvkc9pMxpgqYvkEcJA'
import subprocess

subprocess.run(["ngrok", "authtoken", "2uyn7n3HKZWzId7Qa75cXvQwahe_467hvkc9pMxpgqYvkEcJA"])



# Initialize FastAPI app
app = FastAPI()

# Load JSON data
df = pd.read_json('data/competitor_pricing_for_API.json')
data_dict = df.to_dict(orient="records")

# API endpoint
@app.get("/competitorPricing")
def get_competitor_pricing():
    return JSONResponse(content={"data": data_dict})

# Allow nested event loops (needed for running FastAPI in Colab)
nest_asyncio.apply()

# Expose FastAPI app via ngrok
public_url = ngrok.connect(8000).public_url
print(f"API running on: {public_url}/docs")

# Start FastAPI server
uvicorn.run(app, host="127.0.0.1", port=8000)