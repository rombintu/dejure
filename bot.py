import os, sys
# from core.dejure import Dejure, TelegramContact
# from core.tools import logger as log
from core import db, log, User, Contact, config, user_build_from_message
from core import Action, ParseMode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()

token = config.bot.token
if not token:
    token = os.getenv("BOT_TOKEN")
if not token:
    log.critical("Bot token not set. Please read docs")
    sys.exit(0)
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.md2.value)
dp = Dispatcher()

@dp.message(Command("start", "info"))
async def cmd_start(message: types.Message):
    user: User = db.user_get_by_uid(message.chat.id)
    if not user:
        user = user_build_from_message(message)
        user = db.sign_up(user)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="Изменить", callback_data=f"user_update_{user.uid}")
    ]])
    await message.answer(f"Информация о пользователе\n{user.to_pretty()}", parse_mode=None, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("user_"))
async def callbacks_user(callback: types.CallbackQuery):
    data = callback.data.split("_")
    action = data[1]
    uid = data[-1]
    user = db.user_get_by_uid(uid)
    if not user:
        await callback.answer("Пользователь не найден. Повторите позже")
        return
    log.debug(f"User: {user.contact.t_name} Action: {action} id: {uid}")
    match action:
        case Action.update.value:
            log.debug(action) # TODO

    await callback.answer()

async def run():
    log.info("Bot is starting...")
    await dp.start_polling(bot)
