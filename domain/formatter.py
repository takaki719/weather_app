import datetime as dt

WEATHER_ICON = {
    "Rain": "🌧️", "Drizzle": "🌦️", "Clear": "☀️", "Clouds": "⛅", "Snow": "❄️", "Thunderstorm": "⛈️"
}

def build_message(day: str, forecast: dict) -> str:
    """
    メッセージの雛形を作成する関数  
    """
    
    jp_day = "今日" if day == "today" else "明日"
    w = forecast["weather"][0]
    main = w["main"]
    icon = WEATHER_ICON.get(main, "🌡️")
    temp_max = round(forecast["temp"]["max"])
    temp_min = round(forecast["temp"]["min"])
    pop = int(forecast["pop"] * 100)  # 降水確率 (0-1)

    date_txt = dt.datetime.fromtimestamp(forecast["dt"], dt.timezone(dt.timedelta(hours=9))).strftime("%-m/%-d(%a)")
    return (
        f"{jp_day}（{date_txt}）の天気 {icon}\n\n"
        f"・{w['description'].capitalize()}\n"
        f"・最高気温: {temp_max}℃\n"
        f"・最低気温: {temp_min}℃\n"
        f"・降水確率: {pop}%"
    )
