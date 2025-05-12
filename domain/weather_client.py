import boto3, datetime as dt, requests, os
from functools import lru_cache

@lru_cache
def _get_api_key():
    ssm = boto3.client("ssm")
    api_key = ssm.get_parameter(Name="OWM_API_KEY", WithDecryption=True)["Parameter"]["Value"]
    print("✅ APIキーの取得結果:", api_key)  # ← これ追加！
    return ssm.get_parameter(Name="OWM_API_KEY", WithDecryption=True)["Parameter"]["Value"]

LAT, LON = os.getenv("LAT", "34.7320499"), os.getenv("LON", "135.7336346")  # default: 東京駅

def fetch_forecast(day: str):
    """day: 'today' or 'tomorrow'"""
    dt_now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    target_idx = 0 if day == "today" else 1
    url = (
        "https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={LAT}&lon={LON}&exclude=minutely,hourly,alerts"
        f"&units=metric&lang=ja&appid={_get_api_key()}"
    )
    res = requests.get(url, timeout=5).json()
    return res["daily"][target_idx]  # dict
