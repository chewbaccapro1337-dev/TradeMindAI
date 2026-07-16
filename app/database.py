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
    
def get_last_trades(user_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, side, entry, exit, pnl, created_at
        FROM trades
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    trades = cursor.fetchall()

    conn.close()

    return trades