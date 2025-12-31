import os
import jdatetime
from datetime import datetime
import pytz  # کتابخانه تنظیم منطقه زمانی
from pyrogram import Client, filters
from pyrogram.types import Message

# ---------------------------------------------------------
# تنظیمات ربات
# ---------------------------------------------------------
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"

# دریافت توکن از متغیرهای محیطی (ایمن‌ترین روش در فضای ابری)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

APP_NAME = "my_jalali_bot"

app = Client(
    name=APP_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------------------------------------------------
# تابع دریافت تاریخ شمسی (اصلاح شده)
# ---------------------------------------------------------
def get_persian_date():
    # تنظیم منطقه زمانی به تهران
    tehran_tz = pytz.timezone("Asia/Tehran")
    
    # دریافت زمان فعلی با منطقه زمانی تهران
    now = datetime.now(tehran_tz)
    
    # تبدیل به تاریخ شمسی
    j_date = jdatetime.date.fromgregorian(date=now)
    
    # دریافت نام روز هفته
    day_name = j_date.strftime("%A")
    
    # فرمت‌بندی نهایی (مثال: جمعه ۱۴۰۳/۰۲/۰۱)
    formatted_date = f"{day_name} {j_date.jyear}/{j_date.jmonth:02d}/{j_date.jday:02d}"
    
    return formatted_date

# ---------------------------------------------------------
# دستور شروع
# ---------------------------------------------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("👋 سلام! من ربات هستم.\n\nهر متنی که برایم بفرستی، تاریخ شمسی و روز هفته را به پایین آن اضافه می‌کنم.")

# ---------------------------------------------------------
# هندلر اصلی برای دریافت متن و افزودن تاریخ
# ---------------------------------------------------------
@app.on_message(filters.text & ~filters.command("start"))
async def footer_handler(client: Client, message: Message):
    try:
        # دریافت متن اصلی پیام کاربر
        original_text = message.text
        
        # دریافت تاریخ شمسی
        date_str = get_persian_date()
        
        # اضافه کردن تاریخ به انتهای متن
        new_text = f"{original_text}\n\n📅 {date_str}"
        
        # ارسال پاسخ
        await message.reply(new_text, quote=True)
        
    except Exception as e:
        # اگر خطایی رخ داد، چاپ کن
        print(f"Error: {e}")
        await message.reply_text("متاسفانه خطایی رخ داد.")

# ---------------------------------------------------------
# اجرای ربات
# ---------------------------------------------------------
print("ربات در حال اجرا است...")
app.run()
