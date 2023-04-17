from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from utils.search import search


@dp.channel_post_handler(content_types=['audio'])
async def get_channel_audio(message: types.Message, state: FSMContext):
    keywords = list(message.caption)
    title = str(message.audio.title)
    duration = message.audio.duration
    file_size = message.audio.file_size
    performer = message.audio.performer
    file_id = message.audio.file_id

    # Make audio duration
    if duration < 60:
        duration = f'0:{duration}'
    elif duration == 60:
        duration = f'1:00'
    elif duration > 60:
        minuts = duration // 60
        seconds = duration % 60
        duration = f'{minuts}:{seconds}'
    
    # Makke audio size
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
    if performer:
        title = f'{performer} - {title}'

    new_keywords = str()
    for keyword in keywords:
        if keyword == ' ':
            new_keywords += ' '
        new_keywords += f'{keyword.strip()}'
    try:
        await db.add_music(title=title, file_id=file_id, keywords=new_keywords)
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=f"<code>{title}</code> bazaga muvaffaqiyatli qo'shildi!")
    except Exception as error:
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=f"<code>{title}</code> bazaga qo'shilmadi!")
