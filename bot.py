import os
import razorpay
import requests
import asyncio
from flask import Flask, request
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ENV
TOKEN = "8621358668:AAEzPQCtDTlWauYltL8kzkWBZ1h-oPwr-AM"

RAZORPAY_KEY_ID = "rzp_test_Sc6yE8eA5QA0QD"
RAZORPAY_KEY_SECRET = "riyorax123"

# INIT
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
app = Flask(__name__)

tg_app = ApplicationBuilder().token(TOKEN).build()

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    order = client.order.create({
        "amount": 19900,
        "currency": "INR",
        "payment_capture": 1,
        "notes": {"user_id": str(user_id)}
    })

    pay_url = f"https://rzp.io/l/{order['id']}"

    keyboard = [
        [InlineKeyboardButton("💳 Buy ₹199", url=pay_url)],
        [InlineKeyboardButton("📞 Support", url="https://t.me/riyoraxsupport")]
    ]

    await update.message.reply_photo(
        photo="https://i.ibb.co/1B4Z7Py",
        caption="🔥 Buy Premium Plan ₹199",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# WEBHOOK
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data.get("event") == "payment.captured":
        payment = data["payload"]["payment"]["entity"]
        user_id = payment.get("notes", {}).get("user_id")

        if user_id:
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={
                    "chat_id": user_id,
                    "text": "✅ Payment Successful!\nContact: @riyoraxsupport"
                }
            )

    return "ok"

# HANDLER
tg_app.add_handler(CommandHandler("start", start))

# RUN BOT (FIXED)
async def run_bot():
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()

# MAIN
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # run bot in background
    loop.create_task(run_bot())

    # run flask
    app.run(host="0.0.0.0", port=8080)
