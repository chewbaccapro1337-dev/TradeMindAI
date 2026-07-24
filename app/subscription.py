from datetime import datetime
from database import get_connection


def check_subscription(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT expires_at
        FROM subscriptions
        WHERE user_id=?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if not result:
        return False

    try:
        expires_date = datetime.fromisoformat(result[0])

    except Exception:
        return False

    return expires_date > datetime.now()
