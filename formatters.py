from typing import Any, Dict


def format_movie(item: Dict[str, Any]) -> str:
    title = item.get("title") or "Без названия"
    release = item.get("release_date") or "—"
    score = item.get("rt_score")
    rating_text = f"{score}/100" if score else "—"
    movie_id = item.get("id", "—")
    return f"*{title}* ({release})\n⭐️ {rating_text} | ID: `{movie_id}`"
