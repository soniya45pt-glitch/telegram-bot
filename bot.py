import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# 🔐 BOT TOKEN
TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"

# 👑 ADMIN ID
ADMIN_ID = 6556890316

# 🔥 LINKS
PHOTO1 = "https://kommodo.ai/i/P2L3WhbCt4oTPQfaGVYf"
PHOTO2 = "https://kommodo.ai/i/8poyQXs6LiEYbgQKS86N"
PHOTO3 = "https://kommodo.ai/i/iUd6mrIbiFfxCBq90AAk"

PAY_210 = "https://rzp.io/rzp/EeA4ZDf"
PAY_310 = "https://rzp.io/rzp/ToyNdQ5"
PAY_510 = "https://rzp.io/rzp/Lk6NTfah"

CHANNEL_210 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_310 = "https://t.me/+Rw0Ok8hEhbI1N2U1"
CHANNEL_510 = "https://t.me/riyoraxsupport"

SUPPORT = "@riyoraxsupport"

logging.basicConfig(level=logging.INFO)

# 🟢 BUTTONS
def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ₹210 Photo Access", url=PAY_210)],
        [InlineKeyboardButton("🎬 ₹310 Video Access", url=PAY_310)],
        [InlineKeyboardButton("📞 ₹510 Video Call Access", url=PAY_510)],
        [InlineKeyboardButton("✅ I Paid", callback_data="paid")],
        [InlineKeyboardButton("📞 Support", url=f"https://t.me/{SUPPORT.replace('@','')}")]
    ])

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=PHOTO1,
        caption="🔥 Choose Your Plan & Unlock Access 🔥",
        reply_markup=get_buttons()
    )

    asyncio.create_task(followup(update, context))

# ⏳ FOLLOWUPS
async def followup(update, context):
    chat_id = update.effective_chat.id

    await asyncio.sleep(900)
    await context.bot.send_photo(chat_id, PHOTO2, caption="⚡ Limited Offer!", reply_markup=get_buttons())

    await asyncio.sleep(900)
    await context.bot.send_photo(chat_id, PHOTO3, caption="🔥 Last Chance!", reply_markup=get_buttons())

# 💰 I PAID
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    await query.answer()

    username = f"@{user.username}" if user.username else "No Username"

    text = f"""
💰 *NEW PAYMENT REQUEST*

👤 Name: {user.first_name}
🔗 Username: {username}
🆔 ID: `{user.id}`

👉 Approve:
`/access {user.id} 210`
`/access {user.id} 310`
`/access {user.id} 510`

👉 Reject:
`/unaccess {user.id}`
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )

    await query.message.reply_text("✅ Request sent! Wait for admin approval.")

# ✅ ACCESS
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = int(context.args[1])
    except:
        await update.message.reply_text("❌ Use: /access USER_ID PLAN")
        return

    if plan == 210:
        link = CHANNEL_210
    elif plan == 310:
        link = CHANNEL_310
    elif plan == 510:
        link = CHANNEL_510
    else:
        await update.message.reply_text("❌ Invalid plan")
        return

    await context.bot.send_message(user_id, f"✅ Access Granted!\nJoin here:\n{link}")
    await update.message.reply_text("✅ Done")

# ❌ UNACCESS
async def unaccess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Use: /unaccess USER_ID")
        return

    await context.bot.send_message(user_id, "❌ Access Denied by Admin")
    await update.message.reply_text("❌ Done")

# 🚀 RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("unaccess", unaccess))
app.add_handler(CallbackQueryHandler(paid, pattern="paid"))

print("Bot Running...")
app.run_polling()
