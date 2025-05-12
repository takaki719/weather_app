import os, json, requests, boto3
from functools import lru_cache


LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/broadcast"


@lru_cache
def _get_token():
    ssm = boto3.client("ssm")
    res = ssm.get_parameter(Name="LINE_ACCESS_TOKEN", WithDecryption=True)
    return res["Parameter"]["Value"]


def send(message: str) -> None:
    payload = {"messages": [{"type": "text", "text": message}]}
    headers = {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json",
    }
    r = requests.post(LINE_PUSH_ENDPOINT, headers=headers, json=payload, timeout=5)
    r.raise_for_status()
