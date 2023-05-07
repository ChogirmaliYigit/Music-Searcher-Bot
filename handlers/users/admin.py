import asyncio
from aiogram import types
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
import pandas as pd

@dp.message_handler(text="/allusers", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message, state: FSMContext):
    await state.finish()
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)

@dp.message_handler(text='/musics', user_id=ADMINS, state='*')
async def send_all_musics_count(message: types.Message, state: FSMContext):
    await state.finish()
    count = await db.count_musics()
    await message.answer(text=f"Bazada {count} ta qo'shiq bor.")

@dp.message_handler(text="/reklama", user_id=ADMINS, state='*')
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await state.finish()
    users = await db.select_all_users()
    for user in users:
        user_id = user[-1]
        await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message, state: FSMContext):
    await state.finish()
    await db.delete_users()
    await message.answer("Baza tozalandi!")
