import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8621358668:AAEDOhQKuPONhjpYunWONwnlZf46lT1IPZM"

# 🔥 EDIT THESE
ADMIN_ID = 6556890316
SUPPORT_USERNAME = "@riyoraxsupport"

# 🔥 CHANNEL LINKS
PHOTO_CHANNEL = "https://t.me/+z3WIRBU88qo1MWNl"
VIDEO_CHANNEL = "https://t.me/+fdz3Bwf5d9g0NjU1"
VIP_CHANNEL = "https://t.me/riyoraxsupport"

# 🔥 PHOTOS
PHOTO1 = "https://kommodo.ai/i/8poyQXs6LiEYbgQKS86N"
PHOTO2 = "https://kommodo.ai/i/iUd6mrIbiFfxCBq90AAk"
PHOTO3 = "https://kommodo.ai/i/P2L3WhbCt4oTPQfaGVYf"

# 🔥 PAYMENT LINKS
PAY_210 = "https://rzp.io/rzp/jYJzQXV"
PAY_310 = "https://rzp.io/rzp/TB73Ea9K"
PAY_510 = "https://rzp.io/rzp/74RIEDVK"

# 🔹 BUTTONS (COMMON FOR ALL)
def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 ₹210 Photo Access", url=PAY_210)],
        [InlineKeyboardButton("💳 ₹310 Video Access", url=PAY_310)],
        [InlineKeyboardButton("💳 ₹510 Video Call + VIP", url=PAY_510)],
        [InlineKeyboardButton("✅ I Paid ₹210", callback_data="paid_210")],
        [InlineKeyboardButton("✅ I Paid ₹310", callback_data="paid_310")],
        [InlineKeyboardButton("✅ I Paid ₹510", callback_data="paid_510")],
        [InlineKeyboardButton("🆘 Support", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ])

# 🔹 PLAN TEXT (reuse everywhere)
def plan_text():
    return (
        "🔥 PREMIUM ACCESS 🔥\n\n"
        "💎 ₹210 → Photo Access\n"
        "🎬 ₹310 → Video Access\n"
        "📞 ₹510 → Video Call + VIP\n\n"
        "⚡ Limited Offer – Choose now!"
    )

# 🔹 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        PHOTO1,
        caption=plan_text(),
        reply_markup=get_buttons()
    )

    asyncio.create_task(followup(update, context))

# 🔹 FOLLOWUP SYSTEM
async def followup(update, context):
    chat_id = update.effective_chat.id

    # ⏳ 15 min बाद (2nd photo + plans)
    await asyncio.sleep(900)
    await context.bot.send_photo(
        chat_id,
        PHOTO2,
        caption="⏳ Hurry! Users are unlocking fast!\n\n" + plan_text(),
        reply_markup=get_buttons()
    )

    # ⏳ 15 min बाद (3rd photo + plans)
    await asyncio.sleep(900)
    await context.bot.send_photo(
        chat_id,
        PHOTO3,
        caption="🔥 Last Chance!\n\n" + plan_text(),
        reply_markup=get_buttons()
    )

    # ⏳ 20 min बाद (reminder)
    await asyncio.sleep(1200)
    await context.bot.send_message(
        chat_id,
        "⚡ Access closing soon!\n\n" + plan_text(),
        reply_markup=get_buttons()
    )

    # ⏳ 25 min बाद (final reminder)
    await asyncio.sleep(1500)
    await context.bot.send_message(
        chat_id,
        "🚀 Final Reminder! Unlock now!\n\n" + plan_text(),
        reply_markup=get_buttons()
    )

# 🔹 USER CLICKED I PAID
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data

    await query.answer()

    plan = data.split("_")[1]

    await context.bot.send_message(
        ADMIN_ID,
        f"💰 Payment Request\n\nUser: @{user.username}\nID: {user.id}\nPlan: ₹{plan}"
    )

    await query.message.reply_text(
        "✅ Payment request sent!\nWait for admin approval."
    )

# 🔹 ADMIN APPROVE
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        plan = context.args[1]

        if plan == "210":
            msg = f"✅ Photo Access Granted!\n👉 {PHOTO_CHANNEL}"

        elif plan == "310":
            msg = f"🎬 Video Access Granted!\n👉 {VIDEO_CHANNEL}"

        elif plan == "510":
            msg = (
                f"🔥 VIP Access Granted!\n"
                f"👉 Channel: {VIP_CHANNEL}\n"
                f"📞 Video Call Available!"
            )

        await context.bot.send_message(user_id, msg)
        await update.message.reply_text("Approved ✅")

    except:
        await update.message.reply_text("❌ Use: /approve USER_ID PLAN")

# 🔹 RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CallbackQueryHandler(paid, pattern="paid_"))

print("Bot Running...")
app.run_polling()
