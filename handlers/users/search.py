from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from utils.search import search
from keyboards.inline.buttons import make_musics_markup
from states.states import UserState


@dp.message_handler(state='*')
async def create_search(message: types.Message, state: FSMContext):
    await state.finish()
    user_search = message.text

    markup, msg = await make_musics_markup(user_search=user_search)

    if msg:
        await message.answer(text=msg, reply_markup=markup)
    else:
        await message.reply(text=f"❌ <code>{message.text}</code> bo'yicha hech qanday ma'lumot topilmadi! ❌")

    await state.update_data({'user_search': user_search})


@dp.callback_query_handler(state='*')
async def music_list_actions(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    user_search = data.get('user_search')
    if 'next' in call.data or 'previous' in call.data:
        action, number = call.data.split('_')
        number = int(number)
        if action == 'next':
            markup, msg = await make_musics_markup(user_search=user_search, number=number+10)
            await call.message.edit_text(text=msg, reply_markup=markup)
        if action == 'previous':
            markup, msg = await make_musics_markup(user_search=user_search, number=number-10)
            await call.message.edit_text(text=msg, reply_markup=markup)
    else:
        file = await db.select_file(id=int(call.data))
        await call.message.answer_audio(audio=file.get('file_id'), caption=f'{file.get("title")}')
