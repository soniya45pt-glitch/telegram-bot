import os
import hmac
import hashlib
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"

RAZORPAY_KEY = "rzp_test_Sc8aWzlO5mDpTw"
RAZORPAY_SECRET = "czM9tZFA43yGGGFkBtebrPdL"
WEBHOOK_SECRET = "riyorax123"

client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

app = Flask(__name__)
tg_app = ApplicationBuilder().token(TOKEN).build()

user_orders = {}

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Create Razorpay order
    order = client.order.create({
        "amount": 21000,  # ₹210
        "currency": "INR",
        "payment_capture": 1
    })

    order_id = order["id"]
    user_orders[order_id] = user_id

    payment_link = f"https://rzp.io/rzp/Oa0lD2k?order_id={order_id}"

    keyboard = [
        [InlineKeyboardButton("💳 Pay ₹210", url=payment_link)],
        [InlineKeyboardButton("🆘 Support", url="https://t.me/riyoraxsupport")]
    ]
    await update.message.reply_photo(
        photo="https://kommodo.ai/i/x1cFUgjJQt009Fnvnel5",
        caption="🔥 Premium Access\n\nPay ₹210 to unlock full access",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

tg_app.add_handler(CommandHandler("start", start))

# ===== WEBHOOK (RAZORPAY) =====
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.data
    received_sig = request.headers.get("X-Razorpay-Signature")

    generated_sig = hmac.new(
        bytes(WEBHOOK_SECRET, 'utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    if generated_sig != received_sig:
        return "Invalid signature", 400

    data = request.json

    if data["event"] == "payment.captured":
        order_id = data["payload"]["payment"]["entity"]["order_id"]

        if order_id in user_orders:
            user_id = user_orders[order_id]

            import asyncio
            asyncio.run(
                tg_app.bot.send_message(
                    chat_id=user_id,
                    text="✅ Payment Successful!\n\nContact support: @riyoraxsupport"
                )
            )

    return "OK", 200

# ===== RUN BOTH =====
if __name__ == "__main__":
    import threading

    # Run Flask (webhook server)
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=8080)
    ).start()

    # Run Telegram bot (polling)
    print("Bot Running...")
    tg_app.run_polling()
