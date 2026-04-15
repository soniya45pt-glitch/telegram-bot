from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# 🔑 TOKEN
TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"


# 👑 ADMIN
ADMIN_ID = 6556890316

# 📸 PHOTOS
PHOTO1 = "https://kommodo.ai/i/P2L3WhbCt4oTPQfaGVYf"
PHOTO2 = "https://kommodo.ai/i/8poyQXs6LiEYbgQKS86N"
PHOTO3 = "https://kommodo.ai/i/iUd6mrIbiFfxCBq90AAk"

# 💰 PAYMENT LINKS
PAY_210 = "https://rzp.io/rzp/EeA4ZDf"
PAY_310 = "https://rzp.io/rzp/ToyNdQ5"
PAY_510 = "https://rzp.io/rzp/Lk6NTfah"

# 🔗 CHANNEL LINKS
CHANNEL_210 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_310 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_510 = "https://t.me/riyoraxsupport"

# 🆘 SUPPORT
SUPPORT = "@riyoraxsupport"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 ₹210 Photo Access", callback_data="pay_210")],
        [InlineKeyboardButton("🎬 ₹310 Video Access", callback_data="pay_310")],
        [InlineKeyboardButton("📞 ₹510 Video Call Access", callback_data="pay_510")],
        [InlineKeyboardButton("🆘 Support", url=f"https://t.me/{SUPPORT.replace('@','')}")]
    ]

    await update.message.reply_photo(
        photo=PHOTO1,
        caption="🔥 Choose Your Plan & Unlock Access 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    asyncio.create_task(auto_messages(update, context))


# ================= AUTO MESSAGE =================
async def auto_messages(update, context):
    chat_id = update.effective_chat.id

    await asyncio.sleep(900)
    await context.bot.send_photo(chat_id, PHOTO2, caption="🔥 Limited Offer!")

    await asyncio.sleep(900)
    await context.bot.send_photo(chat_id, PHOTO3, caption="⚡ Last Chance!")

    await asyncio.sleep(1200)
    await context.bot.send_message(chat_id, "⚠️ Access still locked!")

    await asyncio.sleep(300)
    await context.bot.send_message(chat_id, "🔥 Final Reminder!")


# ================= BUTTON =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    await query.answer()

    if query.data == "pay_210":
        plan = "210"
        link = PAY_210
    elif query.data == "pay_310":
        plan = "310"
        link = PAY_310
    elif query.data == "pay_510":
        plan = "510"
        link = PAY_510
    else:
        return

    # USER ko link
    await query.message.reply_text(f"💳 Pay here:\n{link}")

    # ADMIN ko request (COPY FIX)
    text = f"""
💰 NEW PAYMENT CLICK

👤 Name: {user.first_name}
🔗 Username: @{user.username if user.username else 'NoUsername'}
🆔 ID: `{user.id}`
💎 Plan: ₹{plan}

👉 Approve:
`/access {user.id} {plan}`

👉 Reject:
`/unaccess {user.id}`
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )


# ================= ACCESS =================
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        text = update.message.text.split()

        if len(text) < 3:
            await update.message.reply_text("❌ Use: /access USER_ID PLAN")
            return

        user_id = int(text[1])
        plan = text[2]

        if plan == "210":
            link = CHANNEL_210
        elif plan == "310":
            link = CHANNEL_310
        else:
            link = CHANNEL_510

        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment Approved!\n\n🔓 Join here:\n{link}"
        )

        await update.message.reply_text("✅ Access given")

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Error")


# ================= UNACCESS =================
async def unaccess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        text = update.message.text.split()

        if len(text) < 2:
            await update.message.reply_text("❌ Use: /unaccess USER_ID")
            return

        user_id = int(text[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment not confirmed. Contact support."
        )

        await update.message.reply_text("❌ Access removed")

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Error")


# ================= MAIN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("unaccess", unaccess))

print("Bot Running...")
app.run_polling()
