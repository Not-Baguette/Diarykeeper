import os
from passlib.hash import pbkdf2_sha256
import sqlite3


def create_account(username, password):
    # Connect to the database
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS accounts (username text, password_hash text)"
    )

    # Hash the password
    hashed_pw = pbkdf2_sha256.hash(password)

    # Insert the username and hashed password into the database
    cursor.execute(
        "INSERT INTO accounts (username, password_hash) VALUES (?, ?)",
        (username, hashed_pw),
    )

    conn.commit()
    conn.close()


def authenticate(username, password):
    """
    Authenticate the user from sqlite3 database
    """
    conn = sqlite3.connect("accounts_db.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, password_hash FROM accounts")
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
        "CREATE TABLE accounts (username text, password_hash text)"
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

# debug account = "test", password = "test"