import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio
from aiohttp import web
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from db import create_app, SessionLocal, User, ShippingCost


def load_env(path: str | None = None) -> None:
    """Load variables from a .env file into ``os.environ``.

    If a path is explicitly provided or the ``ENV_FILE`` environment variable is
    set, variables from that file override existing ones. Otherwise values are
    only added when they are missing. This allows tests to supply their own
    environment file and ensures the provided values take precedence over a
    globally defined ``BOT_TOKEN``.
    """

    env_path = path or os.getenv("ENV_FILE", str(Path(__file__).with_name(".env")))
    if not os.path.exists(env_path):
        return

    override = path is not None or "ENV_FILE" in os.environ

    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                if override:
                    os.environ[key] = value
                else:
                    os.environ.setdefault(key, value)


class LangStates(StatesGroup):
    choose = State()


class CountryStates(StatesGroup):
    choose = State()


def get_bot_token():
    load_env()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable missing")
    return token


bot = Bot(get_bot_token())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user or not user.language:
            kb = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="Deutsch"), KeyboardButton(text="English")]
            ], resize_keyboard=True)
            await message.answer(
                "Choose your language / Wähle deine Sprache", reply_markup=kb
            )
            await state.set_state(LangStates.choose)
            return

        if not user.country:
            countries = (
                session.query(ShippingCost.country)
                .order_by(ShippingCost.country)
                .all()
            )
            if countries:
                kb = ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text=c.country)] for c in countries],
                    resize_keyboard=True,
                )
                await message.answer("Choose country", reply_markup=kb)
                await state.set_state(CountryStates.choose)
                return

        greeting = "W\u00e4hle ein Produkt" if user.language == "de" else "Choose a product"
        await message.answer(greeting)


@dp.message(LangStates.choose)
async def set_language(message: types.Message, state: FSMContext):
    lang = "de" if message.text.lower().startswith("de") else "en"
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id, language=lang)
            session.add(user)
        else:
            user.language = lang
        session.commit()

        countries = (
            session.query(ShippingCost.country).order_by(ShippingCost.country).all()
        )

    if countries:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=c.country)] for c in countries],
            resize_keyboard=True,
        )
        await state.set_state(CountryStates.choose)
        await message.answer("Choose country", reply_markup=kb)
    else:
        await state.clear()
        greeting = "W\u00e4hle ein Produkt" if lang == "de" else "Choose a product"
        await message.answer(greeting, reply_markup=types.ReplyKeyboardRemove())


@dp.message(CountryStates.choose)
async def set_country(message: types.Message, state: FSMContext):
    country = message.text.strip()
    with SessionLocal() as session:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        if not user:
            user = User(telegram_id=message.from_user.id, country=country)
            session.add(user)
        else:
            user.country = country
        lang = user.language or 'en'
        session.commit()
    await state.clear()
    greeting = "W\u00e4hle ein Produkt" if lang == "de" else "Choose a product"
    await message.answer(greeting, reply_markup=types.ReplyKeyboardRemove())


def main():
    """Start the bot either via webhook or long polling."""
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

        async def on_shutdown(app: web.Application):
            await bot.delete_webhook()

        app.on_shutdown.append(on_shutdown)
        web.run_app(app, host=webhook_host, port=webhook_port, loop=loop)
    else:
        dp.run_polling(bot)


if __name__ == "__main__":
    main()
