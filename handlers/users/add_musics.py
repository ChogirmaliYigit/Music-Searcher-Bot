from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import dp, db, bot
from states.states import AdminStates


@dp.message_handler(text="/add_music", state="*", user_id=ADMINS)
async def add_music_to_db(message: types.Message, state: FSMContext):
    await message.answer(text="Qo'shiqni barcha ma'lumotlari bilan yuboring")
    await AdminStates.get_music.set()


@dp.message_handler(content_types=['audio'], state=AdminStates.get_music, user_id=ADMINS)
async def getmusic(message: types.Message, state: FSMContext):
    title = str(message.audio.title)
    duration = message.audio.duration
    file_size = message.audio.file_size
    performer = message.audio.performer
    file_id = message.audio.file_id

    # Make audio duration
    if duration < 60:
        duration = f'0:{duration if duration >= 10 else f"0{duration}"}'
    elif duration == 60:
        duration = f'1:00'
    elif duration > 60:
        minuts = duration // 60
        seconds = duration % 60
        duration = f'{minuts}:{seconds if seconds >= 10 else f"0{seconds}"}'
    
    # Make audio size
    if file_size >= 1073741824:
        gb = round(file_size / 1073741824, 2)
        file_size = f'{gb} Gb'
    elif file_size >= 1048576:
        mb = round(file_size / 1048576, 2)
        file_size = f'{mb} Mb'
    elif file_size >= 1024:
        kb = round(file_size / 1024, 2)
        file_size = f'{kb} Kb'
    elif file_size < 1024:
        file_size = f'{file_size} bayt'

    # Make audio title
    if title:
        title += f' | {duration} | {file_size}'
    else:
        title = 'Unknown'
    if performer:
        title = f'{performer} - {title}'

    keywords = message.caption
    new_keywords = str()
    for keyword in keywords:
        if keyword == ' ':
            new_keywords += ' '
        new_keywords += f'{keyword.strip()}'

    try:
        file = await db.add_fileid(title=title, file_id=file_id)
        await db.add_keyword(content=new_keywords, file_id=file.get('id'))
        await message.answer(text=f'<code>{title}</code> bazaga qo\'shildi!')
    except Exception as error:
        print(error)
        await message.answer(text="Uzr, xatolik yuz berdi! Keyinroq urinib ko'ring.")
