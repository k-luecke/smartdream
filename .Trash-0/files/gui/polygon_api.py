
import requests
import os
import pandas as pd

# Set your Polygon.io API key as an environment variable or paste here directly
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "REPLACE_WITH_YOUR_API_KEY")

BASE_URL = "https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{start}/{end}"

def fetch_polygon_data(ticker, start_date, end_date, adjusted=True):
    url = BASE_URL.format(ticker=ticker.upper(), start=start_date, end=end_date)
    params = {
        "adjusted": str(adjusted).lower(),
        "sort": "asc",
        "limit": 50000,
        "apiKey": POLYGON_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Polygon API Error: {response.status_code} - {response.text}")

    data = response.json()
    if "results" not in data:
        raise Exception(f"No data found for {ticker} between {start_date} and {end_date}")

    df = pd.DataFrame(data["results"])
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.rename(columns={'t': 'timestamp', 'o': 'open', 'h': 'high',
                       'l': 'low', 'c': 'close', 'v': 'volume'}, inplace=True)
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    return df
