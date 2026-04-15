from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# 🔑 BOT TOKEN
TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"


# 👑 ADMIN
ADMIN_ID = 6556890316

# 🔥 IMAGES
PHOTO1 = "https://kommodo.ai/i/P2L3WhbCt4oTPQfaGVYf"
PHOTO2 = "https://kommodo.ai/i/8poyQXs6LiEYbgQKS86N"
PHOTO3 = "https://kommodo.ai/i/iUd6mrIbiFfxCBq90AAk"

# 💰 PAYMENT LINKS
PAY_210 = "https://rzp.io/rzp/EeA4ZDf"
PAY_310 = "https://rzp.io/rzp/ToyNdQ5"
PAY_510 = "https://rzp.io/rzp/Lk6NTfah"

# 🔗 CHANNELS
CHANNEL_210 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_310 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_510 = "https://t.me/riyoraxsupport"

# 🆘 SUPPORT
SUPPORT = "@riyoraxsupport"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("💎 ₹210 Photo Access", url=PAY_210)],
        [InlineKeyboardButton("🎬 ₹310 Video Access", url=PAY_310)],
        [InlineKeyboardButton("📞 ₹510 Video Call Access", url=PAY_510)],
        [InlineKeyboardButton("🆘 Support", url=f"https://t.me/{SUPPORT.replace('@','')}")]
    ]

    await update.message.reply_photo(
        photo=PHOTO1,
        caption="🔥 Choose Your Plan & Unlock Access 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # ⏱ Auto sequence
    asyncio.create_task(auto_messages(update, context))

# ================= AUTO MESSAGES =================
async def auto_messages(update, context):
    chat_id = update.effective_chat.id

    await asyncio.sleep(900)  # 15 min
    await context.bot.send_photo(chat_id, PHOTO2, caption="🔥 Limited Offer - Choose Plan Now")

    await asyncio.sleep(900)  # 15 min
    await context.bot.send_photo(chat_id, PHOTO3, caption="⚡ Last Chance - Unlock Access Now")

    await asyncio.sleep(1200)  # 20 min
    await context.bot.send_message(chat_id, "⚠️ Your access is still locked! Don't miss this 🔥")

    await asyncio.sleep(300)  # 5 min
    await context.bot.send_message(chat_id, "🔥 Final Reminder: Unlock your premium access now!")

# ================= PAYMENT CLICK =================
async def payment_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.split("_")[1]
    user = query.from_user

    admin_text = f"""
💰 NEW PAYMENT CLICK

👤 Name: {user.first_name}
🔗 Username: @{user.username if user.username else 'NoUsername'}
🆔 ID: `{user.id}`
💎 Plan: ₹{plan}

👉 Approve:
/access {user.id} {plan}

👉 Reject:
/unaccess {user.id}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        parse_mode="Markdown"
    )

# ================= ACCESS =================
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = context.args[1]

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

    except:
        await update.message.reply_text("❌ Use: /access USER_ID PLAN")

# ================= UNACCESS =================
async def unaccess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment not confirmed. Contact support."
        )

        await update.message.reply_text("❌ Access removed")

    except:
        await update.message.reply_text("❌ Use: /unaccess USER_ID")

# ================= MAIN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("unaccess", unaccess))

app.run_polling()
