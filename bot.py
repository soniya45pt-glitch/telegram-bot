import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"
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

# 🔥 MEMORY DATABASE
users_db = {}

# 🔘 BUTTONS
def plans():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ₹210 Photo Access", url=PAY_210)],
        [InlineKeyboardButton("🎬 ₹310 Video Access", url=PAY_310)],
        [InlineKeyboardButton("📞 ₹510 Video Call Access", url=PAY_510)]
    ])

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_photo(
        PHOTO1,
        caption="🔥 Choose your plan\n\nAfter payment type:\n/paid 210 or /paid 310 or /paid 510",
        reply_markup=plans()
    )

    # followups
    asyncio.create_task(send_later(update, context, 900, PHOTO2))
    asyncio.create_task(send_later(update, context, 1800, PHOTO3))
    asyncio.create_task(reminder(update, context))

# ⏱ follow messages
async def send_later(update, context, delay, photo):
    await asyncio.sleep(delay)
    await context.bot.send_photo(
        update.effective_chat.id,
        photo,
        caption="⏳ Limited offer! Unlock now 🔥",
        reply_markup=plans()
    )

async def reminder(update, context):
    await asyncio.sleep(1200)
    await context.bot.send_message(update.effective_chat.id, "⚠️ Last chance!")

# 💰 PAID SYSTEM
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    try:
        plan = context.args[0]
    except:
        await update.message.reply_text("❌ Use: /paid 210 /310 /510")
        return

    username = user.username if user.username else "No Username"

    # save user
    users_db[user.id] = {
        "name": user.first_name,
        "username": username,
        "plan": plan
    }

    await context.bot.send_message(
        ADMIN_ID,
        f"""
💰 NEW PAYMENT REQUEST

👤 Name: {user.first_name}
🔗 Username: @{username}
🆔 ID: {user.id}
💎 Plan: ₹{plan}

👉 Approve:
/access {user.id} {plan}

👉 Reject:
/unaccess {user.id}
"""
    )

    await update.message.reply_text("✅ Request sent to admin")

# ✅ ACCESS
async def access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = context.args[1]
    except:
        await update.message.reply_text("❌ Use: /access USER_ID PLAN")
        return

    if plan == "210":
        link = CHANNEL_210
    elif plan == "310":
        link = CHANNEL_310
    elif plan == "510":
        link = CHANNEL_510
    else:
        return

    await context.bot.send_message(user_id, f"✅ Access Granted!\n{link}")
    await update.message.reply_text("✅ Approved")

# ❌ UNACCESS
async def unaccess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("❌ Use: /unaccess USER_ID")
        return

    await context.bot.send_message(user_id, "❌ Payment not confirmed")
    await update.message.reply_text("❌ Rejected")

# ⚙️ RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("paid", paid))
app.add_handler(CommandHandler("access", access))
app.add_handler(CommandHandler("unaccess", unaccess))

print("🔥 Bot Running...")
app.run_polling()
