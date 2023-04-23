from aiogram import types
from aiogram.dispatcher import FSMContext
from io import BytesIO
from pytube import YouTube
from aiogram.dispatcher.filters.builtin import Text
from loader import dp, db, bot
from data.config import ADMINS
from utils.search import search
from keyboards.inline.buttons import make_musics_markup
from states.states import UserState



@dp.message_handler(Text(startswith="https://www.youtube.com/" or "https://youtu.be/" or "https://www.youtube.com/" or "http://youtu.be/"), state="*")
async def get_audio(message:types.Message, state: FSMContext):
    link=message.text
    audio = await db.select_audio(link=link)
    if audio is None:
        buffer=BytesIO()
        url=YouTube(link)
        if url.check_availability() is None:
            audio=url.streams.get_audio_only()
            audio.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
            filename=url.title
            white = '◽️'
            black = '◼️'
            xabar = await bot.send_message(chat_id=message.from_user.id, text='<b>Yuklanmoqda</b>', parse_mode='HTML')
            for i in range(1,11):
                oq = (10-i) * white
                qora = i*black 
                await xabar.edit_text(text=f"{qora}{oq}\n{10*i}% yuklanmoqda...")
            await xabar.delete()
            await message.answer_chat_action(action="upload_audio")
            audio = await message.answer_audio(audio=buffer, caption=filename)
            await db.add_audio(link=link, file_id=audio.audio.file_id, caption=audio.caption)
        else:
            await message.answer("<b><i>Uzr, xatolik yuz berdi! Keyinroq urinib ko'ring!</i></b>", parse_mode='HTML')
    else:
        await message.answer_chat_action(action="upload_audio")
        audio = await message.answer_audio(audio=audio.get('file_id'), caption=audio.get('caption'))

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


