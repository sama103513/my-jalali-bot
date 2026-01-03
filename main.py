import os
import jdatetime
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------------------------------------------------
# Bot Configuration
# ---------------------------------------------------------
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_NAME = "bot_railway"

# ---------------------------------------------------------
# Initialize Client
# ---------------------------------------------------------
app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------------------------------------------------
# Function to Get Persian Date
# ---------------------------------------------------------
def get_persian_date():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    j_date = jdatetime.date.fromgregorian(date=now, locale='fa_IR')
    day_name = j_date.strftime("%A")
    formatted_date = f"{day_name} {j_date.year}/{j_date.month:02d}/{j_date.day:02d}"
    return formatted_date

# ---------------------------------------------------------
# Start Command Handler
# ---------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("Bot started successfully!")

# ---------------------------------------------------------
# Main Handler: Supports Text and Photos
# ---------------------------------------------------------
@app.on_message((filters.text | filters.photo) & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        date_str = get_persian_date()
        footer_text = f"\n\n📅 {date_str}"
        
        sent_message = None
        
        if message.photo:
            # Handle Photo: Add date to caption
            original_caption = message.caption if message.caption else ""
            sent_message = await client.send_photo(
                chat_id=message.chat.id,
                photo=message.photo.file_id,
                caption=original_caption + footer_text
            )
        else:
            # Handle Text: Add date to message body
            original_text = message.text
            new_text = original_text + footer_text
            sent_message = await client.send_message(
                chat_id=message.chat.id,
                text=new_text,
                disable_web_page_preview=True
            )

        # Trick: Delete bot message, then copy it back to show original author
        if sent_message:
            await sent_message.delete()
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=message.chat.id,
                message_id=sent_message.id
            )
            
        # Delete the user's original message
        await message.delete()

    except Exception as e:
        print(f"Error: {e}")

# ---------------------------------------------------------
# Run the Bot
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
