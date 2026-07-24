from telegram import Update
from telegram.ext import ContextTypes
from database import get_connection, add_subscription


ADMIN_ID = 1176830974   # сюда свой Telegram ID


def is_admin(user_id):
    return user_id == ADMIN_ID



async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM subscriptions"
    )
    subscriptions = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM subscriptions
        WHERE expires_at > datetime('now')
        """
    )
    active = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM trades"
    )
    trades = cursor.fetchone()[0]


    conn.close()


    await update.message.reply_text(
        f"""
👑 TradeMind AI Admin

👥 Пользователи:
{subscriptions}

💎 Активные подписки:
{active}

📈 Сделки:
{trades}
"""
    )



async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return


    try:
        user_id = int(context.args[0])
        days = int(context.args[1])

    except:
        await update.message.reply_text(
            "Использование:\n/grant USER_ID DAYS"
        )
        return


    add_subscription(user_id, days)

    await update.message.reply_text(
        "✅ Подписка выдана"
    )



async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return


    user_id = int(context.args[0])


    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


    await update.message.reply_text(
        "❌ Подписка удалена"
    )
