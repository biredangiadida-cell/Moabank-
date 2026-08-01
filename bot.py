from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==========================
# CONFIG
# ==========================
TOKEN = "YOUR_BOT_TOKEN"

BOT_NAME = "🏦 MoaBank"

# ==========================
# START
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("👤 Create Account", callback_data="create")],
        [InlineKeyboardButton("🔐 Login", callback_data="login")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("💸 Transfer", callback_data="transfer")],
        [InlineKeyboardButton("📥 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("📤 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("☎️ Support", callback_data="support")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"""
🏦 <b>{BOT_NAME}</b>

Baga nagaan dhuftan.

Maal gochuu barbaaddu?

👇 Button keessaa tokko filadhu.
""",
        parse_mode="HTML",
        reply_markup=reply_markup,
    )

# ==========================
# BUTTONS
# ==========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "create":
        await query.edit_message_text(
            "👤 Account uumuu jalqabne."
        )

    elif query.data == "login":
        await query.edit_message_text(
            "🔐 PIN kee galchi."
        )

    elif query.data == "balance":
        await query.edit_message_text(
            "💰 Balance kee yeroo ammaatti: ETB 0.00"
        )

    elif query.data == "transfer":
        await query.edit_message_text(
            "💸 Transfer service."
        )

    elif query.data == "deposit":
        await query.edit_message_text(
            "📥 Deposit service."
        )

    elif query.data == "withdraw":
        await query.edit_message_text(
            "📤 Withdrawal service."
        )

    elif query.data == "history":
        await query.edit_message_text(
            "📜 Transaction history."
        )

    elif query.data == "settings":
        await query.edit_message_text(
            "⚙️ Settings."
        )

    elif query.data == "support":
        await query.edit_message_text(
            "☎️ Customer Support."
        )

# ==========================
# MAIN
# ==========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🏦 MoaBank Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
