from aiogram import types
from aiogram.dispatcher import FSMContext
from io import BytesIO
from pytube import YouTube
from aiogram.dispatcher.filters.builtin import Text
from loader import dp, db
from keyboards.inline.buttons import make_musics_markup
from states.states import UserState



@dp.message_handler(Text(startswith="https://www.youtube.com/" or "https://www.youtu.be/" or "https://youtube.com/" or "https://youtu.be/" or "http://www.youtube.com/" or "http://www.youtu.be/" or "http://youtube.com/" or "http://youtu.be/"), state="*")
async def get_audio(message:types.Message, state: FSMContext):
    link = message.text
    audio = await db.select_audio(link=link)
    if audio is None:
        msg = await message.reply(text="🔍")
        buffer = BytesIO()
        url = YouTube(link)
        if url.check_availability() is None:
            try:
                audio = url.streams.get_audio_only()
                audio.stream_to_buffer(buffer=buffer)
                buffer.seek(0)

                total_file_size = len(buffer.getbuffer())

                filename=url.title
                await msg.delete()
                loading = await message.answer(text=f"0% yuklanmoqda...")
                label = True
                while label:
                    if buffer:
                        label = False
                    for i in range(1, total_file_size, total_file_size // 100):
                        await loading.edit_text(text=f"{round(i / total_file_size, 2) * 100}%  yuklanmoqda...")
                await loading.edit_text(text="🔽 Yuborilmoqda...")
                await message.answer_chat_action(action="upload_audio")
                audio = await message.answer_audio(audio=buffer, caption=filename)
                await loading.delete()
                await db.add_audio(link=link, file_id=audio.audio.file_id, caption=audio.caption)
            except KeyError:
                await message.answer(text="Qo'shiqni yuklashda xatolik yuz berdi! Keyinroq urinib ko'ring yoki boshqa link jo'nating.")
        else:
            await message.answer("<b><i>Uzr, xatolik yuz berdi! Keyinroq urinib ko'ring!</i></b>", parse_mode='HTML')
    else:
        await message.answer_chat_action(action="upload_audio")
        audio = await message.answer_audio(audio=audio.get('file_id'), caption=audio.get('caption'))

@dp.message_handler(state=UserState.search_music_by_cat)
async def create_search(message: types.Message, state: FSMContext):
    user_search = message.text
    data = await state.get_data()
    cat_id = data.get('cat_id')
    audios = await db.select_all_fileids(category_id=cat_id)
    if audios:
        await message.answer(text="qo'shiq topildi")
    else:
        await message.reply(text=f"{message.text} bo'yicha hech qanday ma'lumot topilmadi")

    # user_search orqali api ga so'rov yuborish ishlanishi kerak

@dp.callback_query_handler(state=UserState.get_category)
async def get_category_user(call: types.CallbackQuery, state: FSMContext):
    cat = await db.get_cat(title=call.data)
    if cat:
        await state.update_data(cat_id=cat['id'])
        await call.message.answer(text=f"{cat['title']} kategoriyasi bo'yicha qo'shiqchi yoki qo'shiq nomini kiriting.")
        await UserState.search_music_by_cat.set()


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


