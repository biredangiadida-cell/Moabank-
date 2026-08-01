# ==========================================
# FIND USER BY PHONE
# ==========================================

def find_user_by_phone(phone):

    conn = connect()

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE phone=?",
        (phone,)
    )

    user = cur.fetchone()

    conn.close()

    return user


# ==========================================
# TRANSFER BALANCE
# ==========================================

def transfer_balance(sender_id, receiver_id, amount):

    conn = connect()

    cur = conn.cursor()

    # Sender Balance

    cur.execute(
        "SELECT balance FROM users WHERE telegram_id=?",
        (sender_id,)
    )

    sender = cur.fetchone()

    if sender is None:

        conn.close()

        return False

    if sender[0] < amount:

        conn.close()

        return False

    # Receiver Balance

    cur.execute(
        "SELECT balance FROM users WHERE telegram_id=?",
        (receiver_id,)
    )

    receiver = cur.fetchone()

    if receiver is None:

        conn.close()

        return False

    sender_balance = sender[0] - amount

    receiver_balance = receiver[0] + amount

    # Update Sender

    cur.execute(
        "UPDATE users SET balance=? WHERE telegram_id=?",
        (
            sender_balance,
            sender_id
        )
    )

    # Update Receiver

    cur.execute(
        "UPDATE users SET balance=? WHERE telegram_id=?",
        (
            receiver_balance,
            receiver_id
        )
    )

    conn.commit()

    conn.close()

    return True
