import os
import razorpay
import requests
from flask import Flask, request
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ENV VARIABLES
TOKEN ="8621358668:AAEzPQCtDTlWauYltL8kzkWBZ1h-oPwr-AM"

RAZORPAY_KEY_ID = "rzp_test_Sc7bAjtKJyImk1"

RAZORPAY_KEY_SECRET = "WbbKOcitkM2fvurkLpGi2vOD"

# INIT
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
app = Flask(__name__)

tg_app = ApplicationBuilder().token(TOKEN).build()

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # CREATE ORDER ₹199
    order = client.order.create({
        "amount": 19900,
        "currency": "INR",
        "payment_capture": 1,
        "notes": {"user_id": str(user_id)}
    })

    pay_url = f"https://rzp.io/l/{order['id']}"

    keyboard = [
        [InlineKeyboardButton("💳 Buy Subscription ₹199", url=pay_url)],
        [InlineKeyboardButton("📞 Support", url="https://t.me/riyoraxsupport")]
    ]

    await update.message.reply_photo(
        photo="https://kommodo.ai/i/x1cFUgjJQt009Fnvnel5",
        caption="🔥 Buy Premium Plan ₹199\n\n💎 Instant access after payment",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # Reminder after 60 sec
    async def reminder():
        import asyncio
        await asyncio.sleep(60)
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="⏳ You haven’t purchased yet.\nBuy now to unlock access 😏"
            )
        except:
            pass

    context.application.create_task(reminder())


# WEBHOOK (AUTO PAYMENT DETECT)
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
                    "text": "🎉 Payment Successful ✅\n\nContact support to get access:\n👉 @riyoraxsupport"
                }
            )

    return "ok"


# HANDLER
tg_app.add_handler(CommandHandler("start", start))


# RUN BOTH
if __name__ == "__main__":
    # Run Flask in background
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

    # Run Telegram bot
    print("Bot Running...")
    tg_app.run_polling()
