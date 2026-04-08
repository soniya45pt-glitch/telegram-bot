import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8621358668:AAEzPQCtDTlWauYltL8kzkWBZ1h-oPwr-AM"

if not TOKEN:
    print("TOKEN NOT FOUND")
    exit()

ADMIN_ID = 6556890316

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    context.application.user_data[user_id] = True

    keyboard = [
        [InlineKeyboardButton("💎 1 Month - $3.99", url="https://rzp.io/rzp/Oa0lD2k")],
        [InlineKeyboardButton("🔥 2 Months - $6.99", url="https://rzp.io/rzp/Oa0lD2k")],
        [InlineKeyboardButton("👑 3 Months - $12.99", url="https://rzp.io/rzp/Oa0lD2k")],
        [InlineKeyboardButton("🎁 Offer - $10.99", url="https://rzp.io/rzp/Oa0lD2k")],
        [InlineKeyboardButton("✅ I Paid", callback_data="paid")]
    ]

    await update.message.reply_photo(
        photo="https://i.ibb.co/LDTNZfnw",
        caption="🔥 Choose your plan",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New Payment User ID: {user_id}"
    )

    await query.message.reply_text(f"Your ID: {user_id}")

async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        user_id = int(context.args[0])

        await context.bot.send_message(chat_id=user_id, text="Payment Successful 😏")

        await context.bot.send_photo(
            chat_id=user_id,
            photo="https://i.ibb.co/LDTNZfnw"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text="Join Channel:\nhttps://t.me/+1R4StxEOBEQ5YmNl"
        )

async def offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        for user_id in context.application.user_data:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="🔥 30% OFF - 3 Month only $10.99"
                )
            except:
                pass

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("offer", offer))

print("Bot Running...")
app.run_polling()
