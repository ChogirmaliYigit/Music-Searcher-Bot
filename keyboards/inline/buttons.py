from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db
from utils.search import search


async def make_musics_markup(user_search, number=0):
    keywords = await db.select_all_keywords()
    data = []
    for keyword in keywords:
        data.append(keyword.get('content'))
    result = search(text=user_search, data=data)

    total_files = []
    cnt = 0

    if number == 0:
        msg = f'Sahifa: 1\n\n'
    else:
        msg = f'Sahifa: {number // 10 + 1}\n\n'

    last_result = {}
    items = []
    for index, item in enumerate(result):
        items.append(item)
        if item >= 55:
            last_result.update({f'{index}': item})

    for index in last_result.keys():
        keys = await db.get_files_by_keyword(content=str(keywords[int(index)].get('content')))
        files = await db.get_fileids(id=keys.get('file_id'))
        total_files.append(files)

    for file in total_files[number:number+10]:
        if cnt == 10:
            break
        cnt += 1
        msg += f'{cnt}. {file.get("title")}\n'

    markup = InlineKeyboardMarkup(row_width=5)
    i = 0
    if cnt != 0:
        for item in total_files[number:number+10]:
            i += 1
            markup.insert(InlineKeyboardButton(text=f'{i}', callback_data=f"{item.get('id')}"))
            cnt -= 1

    if number != 0 and total_files[number+10:]:
        markup.row(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f'previous_{number}'), InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"next_{number}"))

    elif number != 0:
        markup.row(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f'previous_{number}'))

    elif total_files[number+10:]:
        markup.row(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"next_{number}"))

    if not total_files:
        msg = ""

    return markup, msg
