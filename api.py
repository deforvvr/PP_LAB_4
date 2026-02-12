from typing import Any, Dict, List

import requests

API_BASE_URL = "https://ghibliapi.vercel.app"


def ghibli_get(path: str) -> Any:
    url = f"{API_BASE_URL}{path}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_all_films() -> List[Dict[str, Any]]:
    data = ghibli_get("/films")
    return data if isinstance(data, list) else []
