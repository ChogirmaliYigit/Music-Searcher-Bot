from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db
from utils.search import search


async def make_musics_markup(user_search, number=0):
    keywords = await db.select_all_keywords()
    data = []
    for keyword in keywords:
        data.append(keyword.get('keywords'))
    result = search(text=user_search, data=data)

    total_files = []
    added_files = []
    cnt = 0
    if number == 0:
        msg = f'Sahifa: 1\n\n'
    else:
        msg = f'Sahifa: {number // 10}\n\n'
    while result:
        if max(result) >= 55:
            index = result.index(max(result))
            files = await db.get_fileids(keywords=keywords[index].get('keywords'))
            total_files.append(files[0])
            result.remove(max(result))
            if total_files:
                for file in total_files[number:number+10]:
                    if cnt == 10:
                        break
                    else:
                        if file.get('id') not in added_files:
                            cnt += 1
                            msg += f'{cnt}. {file.get("title")}\n'
                            added_files.append(file.get('id'))
        else:
            break

    markup = InlineKeyboardMarkup(row_width=5)
    i = 0
    for item in total_files[number:number+10]:
        if cnt != 0:
            i += 1
            markup.insert(InlineKeyboardButton(text=f'{i}', callback_data=f'{item.get("id")}'))
            cnt -= 1

    if number != 0:
        markup.row(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f'previous_{number-10}'))
    try:
        if added_files[number+10:]:
            markup.row(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"next_{number+10}"))
    except Exception as err:
        print(err)

    if not total_files:
        msg = ""
    return markup, msg
