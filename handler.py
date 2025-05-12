from domain.weather_client import fetch_forecast
from domain.formatter import build_message
from adapters.line import send

def lambda_handler(event, _):
    """
    EventBridge から {"target_day": "today"} or "tomorrow" が渡ってくる想定
    """
    target_day = event.get("target_day", "today")
    forecast = fetch_forecast(target_day)
    message = build_message(target_day, forecast)
    send(message)
    return {"status": "ok"}
