import os
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = 12345678  # Replace with your API_ID from https://my.telegram.org
API_HASH = "your_api_hash"  # Replace with your API_HASH
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = Client("broadcast-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

GROUPS_FILE = "groups.json"

def load_groups():
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, "r") as f:
        return json.load(f)

def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(_, message: Message):
    # Bot stays silent
    pass

@app.on_message(filters.group)
async def track_groups(_, message: Message):
    groups = load_groups()
    if message.chat.id not in groups:
        groups.append(message.chat.id)
        save_groups(groups)

@app.on_message(filters.private & filters.user(ADMIN_ID))
async def broadcast_handler(_, message: Message):
    if not message.text:
        return

    groups = load_groups()
    success = 0
    fail = 0

    for group_id in groups:
        try:
            await message.copy(group_id)
            success += 1
        except:
            fail += 1

    await message.reply_text(f"✅ Broadcasted to {success} groups.\n❌ Failed in {fail}.")

@app.on_message(filters.private & ~filters.user(ADMIN_ID))
async def silent_others(_, message: Message):
    # Ignore messages from non-admin users
    pass

if __name__ == "__main__":
    app.run()
