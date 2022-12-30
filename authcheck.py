import os
from passlib.hash import pbkdf2_sha256
import sqlite3
import random
import string


def create_account(username, password):
    def generate_id():
        """
        Generate a random id and check the database if it exists
        """
        # Generate a random id
        acc_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase +
                                                      string.digits) for _ in range(16))  # it's a "id" per se
        conn_ = sqlite3.connect("accounts_db.db")
        cursor_ = conn_.cursor()

        # Check if the id already exists
        cursor_.execute("SELECT account_id FROM accounts")
        ids = cursor_.fetchall()
        conn_.close()

        for id_ in ids:
            if id_ != acc_id:
                pass
            else:
                return generate_id()
        return acc_id

    # Connect to the database
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS accounts (username text, password_hash, account_id text)"
    )

    # Hash the password
    hashed_pw = pbkdf2_sha256.hash(password)
    gen_id = generate_id()

    # Insert the username and hashed password into the database
    cursor.execute(
        "INSERT INTO accounts (username, password_hash, account_id) VALUES (?, ?, ?)",
        (username, hashed_pw, gen_id),
    )

    conn.commit()
    conn.close()


def authenticate(username, password):
    """
    Authenticate the user from sqlite3 database
    """
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, password_hash, account_id FROM accounts")
    accounts = cursor.fetchall()
    conn.close()

    for account in accounts:
        if account[0] == username and pbkdf2_sha256.verify(password, account[1]):
            return True

    return False


def name_check(username):
    """
    Check if the username already exists
    """
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM accounts")
    accounts = cursor.fetchall()
    conn.close()

    # Check if the username already exists
    for account in accounts:
        if account[0] == username:
            return True

    return False


def create_db():
    """
    Generate the database
    """
    os.system("del accounts_db.db")
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE accounts (username text, password_hash, account_id text)"
    )

    conn.commit()
    conn.close()


def check_db():
    """
    attempt to open the database via os
    """
    try:
        open("accounts_db.db")
    except FileNotFoundError:
        create_db()


def change_password(username, old_password, new_password):
    """
    Change the password of the account
    """
    # Check if the account exists
    if authenticate(username, old_password):
        # Hash the new password
        hashed_pw = pbkdf2_sha256.hash(new_password)

        # Connect to the database
        conn = sqlite3.connect("accounts_db.db")
        cursor = conn.cursor()

        # Update the password
        cursor.execute(
            "UPDATE accounts SET password_hash = ? WHERE username = ?",
            (hashed_pw, username),
        )

        conn.commit()
        conn.close()

        return True
    else:
        return False


def return_db():
    """
    Return the database
    """
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    conn.close()

    return accounts


def get_id(username):
    """
    Get the id of the account that is used to encrypt the diary too
    """
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT account_id FROM accounts WHERE username = ?", (username,))
    id_ = cursor.fetchone()
    conn.close()
    return id_[0]

# debug account = "test", password = "test"
