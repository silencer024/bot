import json
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import os

# توکن ربات تلگرام از متغیرهای محیطی
TOKEN = os.getenv("7769581588:AAFtAJJU_EBA6Bkb5KwSkumEqkBhGYFraL4")

# شناسه تلگرام آقا بهزاد
OWNER_ID = int(os.getenv("5140558566"))

# مسیر فایل ذخیره‌سازی اطلاعات
DATA_FILE = "user_data.json"

# تابع برای بارگذاری داده‌ها از فایل
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# تابع برای ذخیره داده‌ها به فایل
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# تابع برای پردازش پیام‌ها
def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id  # دریافت User ID فرستنده
    if user_id != OWNER_ID:
        update.message.reply_text("فقط آقا بهزاد می‌تونه اطلاعات وارد کنه! 🚫")
        return

    user_text = update.message.text.strip()

    # بارگذاری داده‌های ذخیره‌شده
    data = load_data()

    # ذخیره‌سازی اطلاعات جدید در فایل JSON
    if user_text.startswith("ثبت اطلاعات:"):
        info = user_text.replace("ثبت اطلاعات:", "").strip()
        # ذخیره‌سازی در قالب یک dictionary
        key, value = info.split(":", 1)
        data[key.strip()] = value.strip()

        # ذخیره اطلاعات جدید
        save_data(data)

        update.message.reply_text(f"اطلاعات '{key.strip()}' با موفقیت ذخیره شد!")

    else:
        # وقتی کاربر فقط سوال می‌کنه، جواب بدیم
        response = data.get(user_text, "متوجه نشدم، می‌تونی واضح‌تر بگی؟")
        update.message.reply_text(response)

# تابع اصلی برای اجرای ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()