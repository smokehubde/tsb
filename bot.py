# -*- coding: utf-8 -*-
"""Telegram Shop Bot entry point and handlers."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import load_env, setup_logging
from db import create_app, SessionLocal, User, ShippingCost
from currency import convert, COUNTRY_CURRENCY


class LangStates(StatesGroup):
    """Conversation state for language selection."""

    choose = State()


class CountryStates(StatesGroup):
    """Conversation state for country selection."""

    choose = State()


logger = logging.getLogger(__name__)

# Translations used in the main menu
GREETINGS = {
    "de": "W\xe4hle ein Produkt",
    "tr": "Bir \u00fcr\u00fcn se\u00e7",
    "ru": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0442\u043e\u0432\u0430\u0440",
}


def get_bot_token() -> str:
    """Return the bot token from the environment."""
    load_env()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable missing")
    return token


bot = Bot(get_bot_token())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """Handle the /start command."""
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user or not user.language:
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Deutsch"),
                        KeyboardButton(text="English"),
                        KeyboardButton(text="Türkçe"),
                        KeyboardButton(text="Русский"),
                    ]
                ],
                resize_keyboard=True,
            )
            await message.answer(
                "Choose your language / W\xe4hle deine Sprache", reply_markup=kb
            )
            await state.set_state(LangStates.choose)
            return

        if not user.country:
            countries = session.query(ShippingCost.country).order_by(ShippingCost.country).all()
            if countries:
                kb = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text=c.country)] for c in countries],
                    resize_keyboard=True,
                )
                await message.answer("Choose country", reply_markup=kb)
                await state.set_state(CountryStates.choose)
                return

        greeting = GREETINGS.get(user.language, "Choose a product")
        await message.answer(greeting)


@dp.message(LangStates.choose)
async def set_language(message: types.Message, state: FSMContext) -> None:
    """Store the user's chosen language."""
    text = message.text.lower()
    if text.startswith("de"):
        lang = "de"
    elif text.startswith("tr"):
        lang = "tr"
    elif text.startswith("ru"):
        lang = "ru"
    else:
        lang = "en"
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id, language=lang)
            session.add(user)
        else:
            user.language = lang
        session.commit()

        countries = session.query(ShippingCost.country).order_by(ShippingCost.country).all()

    if countries:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=c.country)] for c in countries],
            resize_keyboard=True,
        )
        await state.set_state(CountryStates.choose)
        await message.answer("Choose country", reply_markup=kb)
    else:
        await state.clear()
        greeting = GREETINGS.get(lang, "Choose a product")
        await message.answer(greeting, reply_markup=types.ReplyKeyboardRemove())


@dp.message(CountryStates.choose)
async def set_country(message: types.Message, state: FSMContext) -> None:
    """Store the chosen shipping country."""
    country = message.text.strip()
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id, country=country)
            session.add(user)
        else:
            user.country = country

        lang = user.language or "en"
        cost_entry = session.query(ShippingCost).filter_by(country=country).first()
        shipping_cost = cost_entry.cost if cost_entry else None
        session.commit()

    await state.clear()
    if shipping_cost is not None:
        currency = COUNTRY_CURRENCY.get(country, "EUR")
        if currency != "EUR":
            try:
                cost_converted = convert(shipping_cost, "EUR", currency)
                cost_text = f"{cost_converted:.2f} {currency} (\u2248 {shipping_cost} \u20ac)"
            except Exception:
                cost_text = f"{shipping_cost} \u20ac"
        else:
            cost_text = f"{shipping_cost} \u20ac"
        await message.answer(f"Shipping to {country}: {cost_text}")
    greeting = GREETINGS.get(lang, "Choose a product")
    await message.answer(greeting, reply_markup=types.ReplyKeyboardRemove())


def main(argv: list[str] | None = None) -> None:
    """Start the bot using webhook or long polling."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "INFO"))
    args = parser.parse_args([] if argv is None else argv)
    setup_logging(getattr(logging, args.log_level.upper(), logging.INFO), "bot.log")
    create_app()
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        webhook_host = os.getenv("WEBHOOK_HOST", "0.0.0.0")
        webhook_port = int(os.getenv("WEBHOOK_PORT", "8080"))
        webhook_path = os.getenv("WEBHOOK_PATH", "/webhook")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.set_webhook(webhook_url))

        app = web.Application()
        SimpleRequestHandler(dp, bot).register(app, path=webhook_path)
        setup_application(app, dp, bot=bot)

        async def on_shutdown(app: web.Application) -> None:
            await bot.delete_webhook()

        app.on_shutdown.append(on_shutdown)
        logging.info("Starting webhook on %s:%s", webhook_host, webhook_port)
        web.run_app(app, host=webhook_host, port=webhook_port, loop=loop)
    else:
        logging.info("Starting polling mode")
        dp.run_polling(bot)


if __name__ == "__main__":
    main()
