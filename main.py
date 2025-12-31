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
APP_NAME = "my_jalali_bot"

app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------------------------------------------------
# تابع دریافت تاریخ شمسی (با اصلاح زبان فارسی)
# ---------------------------------------------------------
def get_persian_date():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    
    # تبدیل به تاریخ شمسی با تنظیم لوکال (locale) برای فارسی کردن روز هفته
    j_date = jdatetime.date.fromgregorian(date=now, locale='fa_IR')
    
    day_name = j_date.strftime("%A") # حالا فارسی می‌شود: چهارشنبه
    formatted_date = f"{day_name} {j_date.year}/{j_date.month:02d}/{j_date.day:02d}"
    
    return formatted_date

# ---------------------------------------------------------
# دستور شروع
# ---------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("👋 سلام! من ربات هستم.\n\nهر متنی که برایم بفرستی، پیام را پاک می‌کنم و تاریخ شمسی را به انتهای آن اضافه می‌کنم.")

# ---------------------------------------------------------
# هندلر اصلی (حل مشکل تکرار پیام)
# ---------------------------------------------------------
@app.on_message(filters.text & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        original_text = message.text
        date_str = get_persian_date()
        new_text = f"{original_text}\n\n📅 {date_str}"
        
        # برای جلوگیری از دوبار نوشته شدن، ما پیام اصلی کاربر را پاک می‌کنیم
        # و یک پیام جدید که شامل متن + تاریخ است می‌فرستیم.
        
        # 1. پاک کردن پیام اصلی کاربر
        await message.delete()
        
        # 2. ارسال پیام جدید (شامل متن و تاریخ)
        # از chat_id و message_id برای ارسال در همان جای پیام قبلی استفاده می‌کنیم
        await client.send_message(
            chat_id=message.chat.id,
            text=new_text,
            reply_to_message_id=message.reply_to_message_id  # اگر در جواب کسی بوده، جایگاهش حفظ شود
        )
        
    except Exception as e:
        print(f"Error: {e}")
        # اگر به هر دلیلی نتوانست پاک کند (مثلاً دسترسی نداشت)، حداقل جواب بدهد
        await message.reply(f"خطا: {e}")

print("ربات در حال اجرا است...")
app.run()
