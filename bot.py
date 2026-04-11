import asyncio
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_paid

TOKEN = "8621358668:AAEzPQCtDTlWauYltL8kzkWBZ1h-oPwr-AM"

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)

    chat_id = update.effective_chat.id

    await typing(context, chat_id)

    await update.message.reply_text("💚 Hey baby... listen to me 😘")

    asyncio.create_task(flow(chat_id, context, user_id))


# TYPING
async def typing(context, chat_id):
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    await asyncio.sleep(random.randint(2, 4))


# VOICE SEND
async def send_voice(context, chat_id):
    await context.bot.send_voice(
        chat_id=chat_id,
        voice=open("voice.ogg", "rb"),
        caption="💚 Listen carefully..."
    )


# FLOW
async def flow(chat_id, context, user_id):

    await asyncio.sleep(10)
    if not is_paid(user_id):
        await typing(context, chat_id)
        await context.bot.send_message(chat_id, "I'm waiting for you 😈")

    await asyncio.sleep(10)
    if not is_paid(user_id):
        await send_voice(context, chat_id)

    await asyncio.sleep(15)
    if not is_paid(user_id):
        keyboard = [[InlineKeyboardButton("💸 Buy Now", callback_data="buy")]]
        await context.bot.send_message(chat_id, "Unlock me baby 🔥", reply_markup=InlineKeyboardMarkup(keyboard))


# BUTTON
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    payment_link = f"https://rzp.io/l/YOUR_LINK?user_id={user_id}"

    if query.data == "buy":
        await query.message.reply_text(f"💳 Pay here:\n{payment_link}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()
print("Bot Running...")
app.run_polling()
