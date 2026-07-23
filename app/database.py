import sqlite3
from datetime import datetime, timedelta

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(
    os.path.dirname(BASE_DIR),
    "trademind.db"
)


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
        tp REAL NOT NULL,
        sl REAL NOT NULL,

        risk REAL NOT NULL,
        rr REAL,

        expected_profit REAL,

        position_size REAL,
        comment TEXT,

        status TEXT DEFAULT 'OPEN',

        exit REAL,
        pnl REAL,

        currency TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        closed_at TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER PRIMARY KEY,
        expires_at TEXT
    )
    """)
	
    conn.commit()
    conn.close()



def save_trade(
    user_id,
    symbol,
    side,
    entry,
    tp,
    sl,
    risk,
    rr,
    expected_profit,
    position_size,
    comment,
    currency
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO trades (
        user_id,
        symbol,
        side,
        entry,
        tp,
        sl,
        risk,
        rr,
        expected_profit,
        position_size,
        comment,
        status,
        currency
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        symbol,
        side,
        entry,
        tp,
        sl,
        risk,
        rr,
        expected_profit,
        position_size,
        comment,
        "OPEN",
        currency
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
            tp,
            sl,
            risk,
            rr,
            expected_profit,
            currency,
            status,
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

def clear_trades(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM trades
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

def get_open_trades(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            symbol,
            side,
            entry,
            tp,
            sl,
            risk,
            rr,
            expected_profit,
            created_at
        FROM trades
        WHERE user_id = ?
        AND status = 'OPEN'
        ORDER BY id DESC
    """, (user_id,))

    trades = cursor.fetchall()

    conn.close()

    return trades

def close_trade(trade_id, exit_price, pnl):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE trades
        SET
            exit = ?,
            pnl = ?,
            status = 'CLOSED',
            closed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        exit_price,
        pnl,
        trade_id
    ))

    conn.commit()
    conn.close()

def create_subscription_table():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER PRIMARY KEY,
        expires_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_subscription(user_id, days):

    conn = get_connection()
    cursor = conn.cursor()

    expires = datetime.now() + timedelta(days=days)

    cursor.execute("""
    INSERT OR REPLACE INTO subscriptions
    (user_id, expires_at)
    VALUES (?, ?)
    """, (
        user_id,
        expires.isoformat()
    ))

    conn.commit()
    conn.close()
