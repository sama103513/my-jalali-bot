import os
import jdatetime
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# It is better to get ID and Hash from Environment Variables in Railway
API_ID = int(os.environ.get("API_ID", 2040))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_NAME = "railway_bot"

# ---------------------------------------------------------
# Client Initialization
# ---------------------------------------------------------
app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------------------------------------------------
# Helper Function: Get Persian Date
# ---------------------------------------------------------
def get_persian_date():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    j_date = jdatetime.date.fromgregorian(date=now, locale='fa_IR')
    day_name = j_date.strftime("%A")
    return f"{day_name} {j_date.year}/{j_date.month:02d}/{j_date.day:02d}"

# ---------------------------------------------------------
# Start Command
# ---------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("Bot is active on Railway!")

# ---------------------------------------------------------
# Main Handler (Text & Photo)
# ---------------------------------------------------------
@app.on_message((filters.text | filters.photo) & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        date_str = get_persian_date()
        footer = f"\n\n📅 {date_str}"
        sent_msg = None

        if message.photo:
            cap = message.caption or ""
            sent_msg = await client.send_photo(
                chat_id=message.chat.id,
                photo=message.photo.file_id,
                caption=cap + footer
            )
        else:
            sent_msg = await client.send_message(
                chat_id=message.chat.id,
                text=message.text + footer,
                disable_web_page_preview=True
            )

        # Execute the copy trick to preserve author name
        if sent_msg:
            await sent_msg.delete()
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=message.chat.id,
                message_id=sent_msg.id
            )
        
        await message.delete()

    except Exception as e:
        print(f"Error: {e}")

# ---------------------------------------------------------
# Run
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Starting bot...")
    app.run()
