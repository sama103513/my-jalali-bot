import os
import jdatetime
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------------------------------------------------
# تنظیمات ربات
# ---------------------------------------------------------
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_NAME = "ربات تاریخ شمسی"

# ---------------------------------------------------------
# ایجاد کلاینت ربات
# ---------------------------------------------------------
app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    max_retries=5
)

# ---------------------------------------------------------
# تابع دریافت تاریخ شمسی
# ---------------------------------------------------------
def get_persian_date():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    
    j_date = jdatetime.date.fromgregorian(date=now, locale='fa_IR')
    day_name = j_date.strftime("%A")
    formatted_date = f"{day_name} {j_date.year}/{j_date.month:02d}/{j_date.day:02d}"
    
    return formatted_date

# ---------------------------------------------------------
# دستور شروع
# ---------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("👋 سلام! من ربات هستم.\n\nپیام شما را حذف کرده و با تاریخ شمسی دوباره ارسال می‌کنم.")

# ---------------------------------------------------------
# هندلر اصلی: پشتیبانی از متن و عکس
# ---------------------------------------------------------
@app.on_message((filters.text | filters.photo) & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        date_str = get_persian_date()
        footer_text = f"\n\n📅 {date_str}"
        
        sent_message = None
        
        # بررسی اینکه پیام عکس است یا متن ساده
        if message.photo:
            # --- مدیریت عکس ---
            original_caption = message.caption if message.caption else ""
            
            # ارسال عکس با کپشن جدید (کپشن اصلی + تاریخ)
            sent_message = await client.send_photo(
                chat_id=message.chat.id,
                photo=message.photo.file_id,
                caption=original_caption + footer_text
            )
            
        else:
            # --- مدیریت متن ---
            original_text = message.text
            new_text = original_text + footer_text
            
            # ارسال متن جدید
            sent_message = await client.send_message(
                chat_id=message.chat.id,
                text=new_text,
                disable_web_page_preview=True
            )

        # اعمال تکنیک "حذف و کپی" برای نمایش نویسنده اصلی
        if sent_message:
            # 1. حذف پیامی که به نام ربات ارسال شد
            await sent_message.delete()
            
            # 2. کپی پیام برای نمایش به نام نویسنده اصلی
            # چون پیام مبدا حذف شده، تلگرام آن را به نام فرستنده قبلی (کاربر) نشان می‌دهد
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=message.chat.id,
                message_id=sent_message.id
            )
            
        # 3. حذف پیام اصلی کاربر
        await message.delete()

    except Exception as e:
        print(f"Error: {e}")

# ---------------------------------------------------------
# اجرای ربات
# ---------------------------------------------------------
if __name__ == "__main__":
    print("ربات در حال اجرا است...")
    app.run()
