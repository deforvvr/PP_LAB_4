import random
import time
from typing import Any, Dict

import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from api import get_all_films, ghibli_get
from formatters import format_movie


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Привет! Я кино-бот.\n\n"
        "Команды:\n"
        "/popular — новые фильмы (по году выхода)\n"
        "/top — фильмы с лучшей оценкой\n"
        "/search <запрос> — поиск фильма\n"
        "/movie <id> — детали фильма\n"
        "/random — случайный фильм\n"
        "/ping — проверка работы бота"
    )
    await update.message.reply_text(text)


async def popular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        movies = get_all_films()
        movies = sorted(
            movies, key=lambda m: int(m.get("release_date") or 0), reverse=True
        )[:5]
        if not movies:
            await update.message.reply_text("Не нашёл популярных фильмов.")
            return
        text = "\n\n".join(format_movie(m) for m in movies)
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except requests.RequestException:
        await update.message.reply_text("Ошибка сети при запросе к API.")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def top_rated(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        movies = get_all_films()
        movies = sorted(
            movies, key=lambda m: int(m.get("rt_score") or 0), reverse=True
        )[:5]
        if not movies:
            await update.message.reply_text("Не нашёл фильмы с высоким рейтингом.")
            return
        text = "\n\n".join(format_movie(m) for m in movies)
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except requests.RequestException:
        await update.message.reply_text("Ошибка сети при запросе к API.")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Использование: /search <запрос>")
        return
    try:
        query = " ".join(context.args)
        movies = get_all_films()
        query_lower = query.lower()
        movies = [m for m in movies if query_lower in (m.get("title") or "").lower()]
        movies = movies[:5]
        if not movies:
            await update.message.reply_text("Ничего не найдено.")
            return
        text = "\n\n".join(format_movie(m) for m in movies)
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except requests.RequestException:
        await update.message.reply_text("Ошибка сети при запросе к API.")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def movie_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Использование: /movie <id>")
        return
    try:
        movie_id = context.args[0]
        data = ghibli_get(f"/films/{movie_id}")
        title = data.get("title", "Без названия")
        overview = data.get("description", "Описание отсутствует.")
        rating = data.get("rt_score")
        rating_text = f"{rating}/100" if rating else "—"
        release = data.get("release_date") or "—"
        director = data.get("director") or "—"
        text = (
            f"*{title}*\n"
            f"Дата: {release}\n"
            f"Режиссёр: {director}\n"
            f"⭐️ {rating_text}\n\n"
            f"{overview}"
        )
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            await update.message.reply_text("Фильм не найден.")
        else:
            await update.message.reply_text("Ошибка сети при запросе к API.")
    except requests.RequestException:
        await update.message.reply_text("Ошибка сети при запросе к API.")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        movies = get_all_films()
        if not movies:
            await update.message.reply_text("Не удалось получить список фильмов.")
            return
        choice = random.choice(movies)
        await update.message.reply_text(format_movie(choice), parse_mode=ParseMode.MARKDOWN)
    except requests.RequestException:
        await update.message.reply_text("Ошибка сети при запросе к API.")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = int(time.time())
    await update.message.reply_text(f"Бот работает. Серверное время: {now}")
