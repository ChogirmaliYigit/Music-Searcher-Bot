from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from data.config import ADMINS
from states.states import UserState
from keyboards.inline.buttons import make_categories_markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.username
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    # user = await db.select_user(telegram_id=message.from_user.id)
    await bot.send_message(chat_id=ADMINS[0], text=f"@{name} bazaga oldin qo'shilgan")
    categories = await db.select_all_categories()
    await message.answer(f"Xush kelibsiz! @{name}", reply_markup=make_categories_markup(categories=categories))
    await UserState.get_category.set()
