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
# ایجاد کلاینت ربات با قابلیت مدیریت خطای Flood
# ---------------------------------------------------------
app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    max_retries=5  # تعداد دفعات تلاش مجدد در صورت خطا
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
# هندلر اصلی
# ---------------------------------------------------------
@app.on_message(filters.text & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        original_text = message.text
        date_str = get_persian_date()
        new_text = f"{original_text}\n\n📅 {date_str}"
        
        await message.delete()
        await client.send_message(
            chat_id=message.chat.id,
            text=new_text,
            disable_web_page_preview=True
        )
        
    except Exception as e:
        print(f"Error: {e}")
        # اگر خطا غیر از Flood بود، به کاربر اطلاع ندهیم تا اسپم نشود
        pass

# ---------------------------------------------------------
# اجرای ربات (با مدیریت خطای FloodWait)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("ربات در حال اجرا است...")
    try:
        app.run()
    except Exception as e:
        print(f"خطای سیستمی: {e}")
