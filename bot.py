from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
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

# ==========================
# STATES
# ==========================
NAME, PHONE, PIN = range(3)

TOKEN = "8918296234:AAFZuKJ99TGJvN0ZWylQkjJYh5CEw6aYUgs"

BOT_NAME = "🏦 MoaBank"if query.data == "create":

    user = get_user(query.from_user.id)

    if user:
        await query.edit_message_text(
            "✅ Account kee duraan uumameera."
        )
        return

    context.user_data.clear()

    await query.message.reply_text(
        "👤 Maqaa guutuu kee ergi."
    )

    context.user_data["step"] = "name"async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "step" not in context.user_data:
        return

    step = context.user_data["step"]

    if step == "name":

        context.user_data["name"] = update.message.text

        context.user_data["step"] = "phone"

        await update.message.reply_text(
            "📱 Lakkoofsa bilbilaa kee ergi."
        )

        return

    if step == "phone":

        context.user_data["phone"] = update.message.text

        context.user_data["step"] = "pin"

        await update.message.reply_text(
            "🔐 PIN (lakkoofsa 4) galchi."
        )

        return

    if step == "pin":

        pin = update.message.text

        if not pin.isdigit() or len(pin) != 4:

            await update.message.reply_text(
                "❌ PIN lakkoofsa 4 qofa ta'uu qaba."
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
            "✅ Account MoaBank kee milkaa'inaan uumameera."
        )elif query.data == "login":

    user = get_user(query.from_user.id)

    if not user:
        await query.edit_message_text(
            "❌ Dura account uumi."
        )
        return

    context.user_data["step"] = "login"

    await query.message.reply_text(
        "🔐 PIN kee galchi."
    )if step == "login":

    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text(
            "❌ Account hin argamne."
        )
        context.user_data.clear()
        return

    pin = update.message.text

    if pin != user[4]:
        await update.message.reply_text(
            "❌ PIN sirrii miti."
        )
        return

    context.user_data.clear()

    await update.message.reply_text(
        f"""✅ Login Milkaa'e!

👤 {user[2]}
💰 Balance: ETB {user[5]:.2f}
"""
    )elif query.data == "balance":

    user = get_user(query.from_user.id)

    if not user:
        await query.edit_message_text(
            "❌ Account hin qabdu."
        )
        return

    await query.edit_message_text(
        f"""🏦 MoaBank

👤 {user[2]}

💰 Balance
ETB {user[5]:.2f}
"""
    )
