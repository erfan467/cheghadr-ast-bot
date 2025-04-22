
import os
import telebot
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image = Image.open(BytesIO(downloaded_file))
    
    bot.send_message(message.chat.id, "در حال تحلیل تصویر...")

    try:
        predictions = classifier(image)
        top_pred = predictions[0]
        label = top_pred['label']
        score = top_pred['score']

        estimated_price = round(score * 1000_000)

        response = f"این تصویر به نظر می‌رسد: {label}\nاعتماد مدل: {round(score*100, 2)}٪\nقیمت تقریبی: {estimated_price:,} تومان"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا در تحلیل تصویر: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! عکس محصول رو بفرست تا برات توضیح و قیمت حدودی بگم.")

()bot.polling
