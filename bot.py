import os, sys
# from core.dejure import Dejure, TelegramContact
# from core.tools import logger as log
from core import db, log, User, Contact, config, user_build_from_message
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()

token = config.bot.token
if not token:
    token = os.getenv("BOT_TOKEN")
if not token:
    log.critical("Bot token not set. Please read docs")
    sys.exit(0)
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="markdownv2")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    is_signup_user = db.user_get_by_uid(message.chat.id)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="Изменить", callback_data=f"info_change_{user.uid}")
    ]])
    if not is_signup_user:
        user = user_build_from_message(message)
        await message.answer(f"Регистрация нового пользователя\n{user.to_pretty()}", parse_mode=None, reply_markup=keyboard)
        return
    await message.answer(f"Информация о пользователе\n{is_signup_user.to_pretty()}", parse_mode=None, reply_markup=keyboard)

@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    users = db.user_list()
    if not users:
        await message.answer("Users not found")
    else:
        await message.answer(str(users))

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    db.registration()

# def get_keyboard():
#     buttons = []
#     for p in api.get_pods():
#         if not p.get_last_status():
#             buttons.append(
#                 [types.InlineKeyboardButton(text=f"{p.name} ⚠️", callback_data=f"{p.name}")]
#             )
#     buttons.append([types.InlineKeyboardButton(text="⏱", callback_data="refresh")])
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard

# @dp.message(Command("pods"))
# async def cmd_numbers(message: types.Message):
#     await message.answer("Проблемные поды", reply_markup=get_keyboard())


# @dp.callback_query(F.data.startswith("num_"))
# async def callbacks_num(callback: types.CallbackQuery):
#     user_value = user_data.get(callback.from_user.id, 0)
#     action = callback.data.split("_")[1]

#     if action == "incr":
#         user_data[callback.from_user.id] = user_value+1
#         await update_num_text(callback.message, user_value+1)
#     elif action == "decr":
#         user_data[callback.from_user.id] = user_value-1
#         await update_num_text(callback.message, user_value-1)
#     elif action == "finish":
#         await callback.message.edit_text(f"Итого: {user_value}")

#     await callback.answer()

async def run():
    log.info("Bot is starting...")
    await dp.start_polling(bot)
