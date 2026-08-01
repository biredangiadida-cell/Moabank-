# ==========================================
# MoaBank Telegram Bot
# Part 1 - Imports & Setup
# ==========================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import (
    create_tables,
    create_user,
    get_user,
    update_balance,
    add_transaction,
    get_transactions,
)

# ==========================================
# CONFIG
# ==========================================

TOKEN = "8918296234:AAEiQsu_h--Pu_wRkQThwFUnjfrhEIUKE58"

BOT_NAME = "🏦 MoaBank"

# ==========================================
# START MENU
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton(
            "👤 Create Account",
            callback_data="create"
        )],

        [InlineKeyboardButton(
            "🔐 Login",
            callback_data="login"
        )],

        [InlineKeyboardButton(
            "💰 Balance",
            callback_data="balance"
        )],

        [InlineKeyboardButton(
            "💸 Transfer",
            callback_data="transfer"
        )],

        [InlineKeyboardButton(
            "📥 Deposit",
            callback_data="deposit"
        )],

        [InlineKeyboardButton(
            "📤 Withdraw",
            callback_data="withdraw"
        )],

        [InlineKeyboardButton(
            "📜 History",
            callback_data="history"
        )],

        [InlineKeyboardButton(
            "⚙️ Settings",
            callback_data="settings"
        )],

        [InlineKeyboardButton(
            "☎️ Support",
            callback_data="support"
        )],

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""
🏦 <b>{BOT_NAME}</b>

Baga Nagaan Dhuftan.

Maal hojjechuu barbaaddu?

👇 Button keessaa tokko filadhu.
"""

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=reply_markup,
    )async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "create":
        await query.edit_message_text(
            "👤 Create Account\n\nMaqaa guutuu kee ergi."
        )
        context.user_data["step"] = "name"

    elif data == "login":
        await query.edit_message_text(
            "🔐 PIN kee ergi."
        )
        context.user_data["step"] = "login"

    elif data == "balance":

        user = get_user(query.from_user.id)

        if not user:
            await query.edit_message_text(
                "❌ Account hin qabdu."
            )
            return

        await query.edit_message_text(
            f"""
🏦 MoaBank

👤 {user[2]}

💰 Balance

ETB {user[5]:,.2f}
"""
        )

    elif data == "deposit":

        await query.edit_message_text(
            "💵 Deposit Amount ergi."
        )

        context.user_data["step"] = "deposit"

    elif data == "withdraw":

        await query.edit_message_text(
            "💸 Withdraw Amount ergi."
        )

        context.user_data["step"] = "withdraw"

    elif data == "transfer":

        await query.edit_message_text(
            "💳 Transfer yeroo dhiyootti ni dabalama."
        )

    elif data == "history":

        await query.edit_message_text(
            "📜 Transaction History yeroo dhiyootti ni dabalama."
        )

    elif data == "settings":

        await query.edit_message_text(
            "⚙️ Settings."
        )

    elif data == "support":

        await query.edit_message_text(
            "☎️ Customer Support."
        )async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "step" not in context.user_data:
        return

    step = context.user_data["step"]

    # NAME

    if step == "name":

        context.user_data["name"] = update.message.text

        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📱 Phone Number kee ergi."
        )

        return

    # PHONE

    if step == "phone":

        context.user_data["phone"] = update.message.text

        context.user_data["step"] = "pin"

        await update.message.reply_text(
            "🔐 PIN (4 digits) ergi."
        )

        return

    # PIN

    if step == "pin":

        pin = update.message.text

        if len(pin) != 4:

            await update.message.reply_text(
                "❌ PIN 4 digits ta'uu qaba."
            )

            return

        create_user(

            update.effective_user.id,

            context.user_data["name"],

            context.user_data["phone"],

            pin,

        )

        context.user_data.clear()

        await update.message.reply_text(
            "✅ Account Milkaa'inaan Uumame."
        )

        return

    # LOGIN

    if step == "login":

        user = get_user(update.effective_user.id)

        if not user:

            await update.message.reply_text(
                "❌ Account hin jiru."
            )

            context.user_data.clear()

            return

        if update.message.text != user[4]:

            await update.message.reply_text(
                "❌ PIN sirrii miti."
            )

            return

        context.user_data.clear()

        await update.message.reply_text(
            f"""
🏦 Login Success

👤 {user[2]}

💰 Balance

ETB {user[5]:,.2f}
"""
        )

        return# ==========================
# WITHDRAW
# ==========================

if step == "withdraw":

    try:
        amount = float(update.message.text)
    except ValueError:
        await update.message.reply_text(
            "❌ Maallaqa sirrii galchi."
        )
        return

    user = get_user(update.effective_user.id)

    if amount > user[5]:

        await update.message.reply_text(
            "❌ Balance gahaa hin qabdu."
        )

        return

    new_balance = user[5] - amount

    update_balance(
        update.effective_user.id,
        new_balance
    )

    add_transaction(
        update.effective_user.id,
        "Withdraw",
        amount,
        "Cash Withdraw"
    )

    context.user_data.clear()

    await update.message.reply_text(
        f"""
✅ Withdraw Success

💸 Amount
ETB {amount:,.2f}

💰 New Balance
ETB {new_balance:,.2f}
"""
    )

    returnelif data == "history":

    user = get_user(query.from_user.id)

    if not user:
        await query.edit_message_text(
            "❌ Account hin qabdu."
        )
        return

    history = get_transactions(query.from_user.id)

    if not history:
        await query.edit_message_text(
            "📜 Transaction hin jiru."
        )
        return

    text = "📜 Transaction History\n\n"

    for row in history[:10]:

        t_type = row[0]
        amount = row[1]
        desc = row[2]
        date = row[3]

        text += (
            f"• {t_type}\n"
            f"ETB {amount:,.2f}\n"
            f"{desc}\n"
            f"{date}\n\n"
        )

    await query.edit_message_text(text)
