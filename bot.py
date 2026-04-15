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

# 🔗 CHANNELS
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
        photo=
