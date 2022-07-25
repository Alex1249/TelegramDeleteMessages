import re
import json
from pyrogram import Client, filters
from pyrogram.types import Message


try:
    with open("config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    api_id = data['api_id']
    api_hash = data['api_hash']
    prefix = data['prefix']
except FileNotFoundError:
    api_id = input("Введите api_id: ")
    api_hash = input("Введите api_hash: ")
    prefix = "дд"

    data = {"api_id": api_id,
            "api_hash": api_hash, 
            "prefix": "дд"}

    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


app = Client("my_account", api_id = api_id, api_hash = api_hash)


async def prefix_filter(_, __, msg: Message):
    if msg.outgoing:
        return msg.text.lower().startswith(prefix)
    return False


cmd_filter = filters.create(prefix_filter)


@app.on_message(cmd_filter & filters.me)
async def delete_messages(client: Client, msg: Message):
    count = re.findall(prefix + r'\s?(\d+)', msg.text.lower())
    if count:
        count = int(count[0]) + 1
    else:
        count = 2
    message_ids = []
    offset = 0
    find = True
    while find:
        async for message in app.get_chat_history(chat_id=msg.chat.id, limit=100, offset=offset):
            if message.from_user.id == msg.from_user.id:
                message_ids.append(message.id)
                if len(message_ids) == count:
                    find = False
                    break
        offset += 100
        if offset >= 1000:
            break
    await app.delete_messages(msg.chat.id, message_ids)


@app.on_message(filters.command(commands="нст", prefixes="") & filters.me)
async def edit_prefix(bot: Client, msg: Message):
    global prefix
    res = re.findall(r"нст (.+)", msg.text.lower())
    if res:
        await msg.edit(f'Теперь префикс "{res[0]}"')
        prefix = res[0]
        data['prefix'] = prefix
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        await msg.edit(f"Укажите нвый префикс")
    
app.run()

# Written with love. By Alexey Kuznetsov.