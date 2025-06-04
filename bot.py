import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db import create_app, SessionLocal, User


class LangStates(StatesGroup):
    choose = State()


def get_bot_token():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable missing")
    return token


bot = Bot(get_bot_token())
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    with SessionLocal() as session:
        user = (
            session.query(User)
            .filter_by(telegram_id=message.from_user.id)
            .first()
        )
        if not user or not user.language:
            kb = ReplyKeyboardMarkup(
                keyboard=[[
                    KeyboardButton(text="Deutsch"),
                    KeyboardButton(text="English"),
                ]],
                resize_keyboard=True,
            )
            await message.answer(
                "Choose your language / Wähle deine Sprache",
                reply_markup=kb,
            )
            await state.set_state(LangStates.choose)
        else:
            greeting = (
                "W\u00e4hle ein Produkt"
                if user.language == "de"
                else "Choose a product"
            )
            await message.answer(greeting)


@dp.message(LangStates.choose)
async def set_language(message: types.Message, state: FSMContext):
    lang = "de" if message.text.lower().startswith("de") else "en"
    with SessionLocal() as session:
        user = (
            session.query(User)
            .filter_by(telegram_id=message.from_user.id)
            .first()
        )
        if not user:
            user = User(telegram_id=message.from_user.id, language=lang)
            session.add(user)
        else:
            user.language = lang
        session.commit()
    await state.clear()
    greeting = "W\u00e4hle ein Produkt" if lang == "de" else "Choose a product"
    await message.answer(greeting, reply_markup=types.ReplyKeyboardRemove())


def main():
    create_app()
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
