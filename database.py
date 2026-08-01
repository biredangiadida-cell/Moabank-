import sqlite3

DB_NAME = "users.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        full_name TEXT NOT NULL,
        phone TEXT,
        pin TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        transaction_type TEXT,
        amount REAL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_user(telegram_id, full_name, phone, pin):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users
    (telegram_id, full_name, phone, pin)
    VALUES (?, ?, ?, ?)
    """, (telegram_id, full_name, phone, pin))

    conn.commit()
    conn.close()


def get_user(telegram_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE telegram_id=?",
        (telegram_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user


def update_balance(telegram_id, balance):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET balance=?
    WHERE telegram_id=?
    """, (balance, telegram_id))

    conn.commit()
    conn.close()


def add_transaction(
    telegram_id,
    transaction_type,
    amount,
    description
):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO transactions
    (telegram_id, transaction_type, amount, description)
    VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        transaction_type,
        amount,
        description
    ))

    conn.commit()
    conn.close()


def get_transactions(telegram_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT transaction_type,
           amount,
           description,
           created_at
    FROM transactions
    WHERE telegram_id=?
    ORDER BY id DESC
    """, (telegram_id,))

    data = cur.fetchall()

    conn.close()

    return data


if __name__ == "__main__":
    create_tables()
    print("✅ Database created successfully.")
