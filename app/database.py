import sqlite3

DB_NAME = "trademind.db"


def get_connection():
    return sqlite3.connect(DB_NAME)



def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        entry REAL NOT NULL,
        exit REAL,
        risk REAL,
        pnl REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()



def save_trade(user_id, symbol, side, entry, exit_price, risk, pnl):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades (
            user_id,
            symbol,
            side,
            entry,
            exit,
            risk,
            pnl
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        symbol,
        side,
        entry,
        exit_price,
        risk,
        pnl
    ))

    conn.commit()
    conn.close()



def get_last_trades(user_id, limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            symbol,
            side,
            entry,
            exit,
            risk,
            pnl,
            created_at
        FROM trades
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    trades = cursor.fetchall()

    conn.close()

    return trades


def get_statistics(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END),
            SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END),
            SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END),
            SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END),
            SUM(pnl),
            AVG(CASE WHEN pnl > 0 THEN pnl END),
            AVG(CASE WHEN pnl < 0 THEN pnl END),
            MAX(pnl),
            MIN(pnl)

        FROM trades
        WHERE user_id = ?
    """, (user_id,))


    stats = cursor.fetchone()

    conn.close()

    return stats
