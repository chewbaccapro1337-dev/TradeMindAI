from database import DB_NAME
import sqlite3
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


    expires = result[0]


    try:
        expires_date = datetime.fromisoformat(expires)

    except Exception:
        return False


    if expires_date > datetime.now():
        return True


    return False

def check_subscription(user_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT expires_at FROM subscriptions WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return False

    return datetime.fromisoformat(row[0]) > datetime.now()
