import sqlite3
import datetime
import authcheck

"""
a db log file to check the time on accessing the diary
"""


def access_write(account_id):
    """
    Write the time and username to the log file
    """
    check_db_log()

    time = datetime.datetime.now()
    conn = sqlite3.connect("log_db.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO log VALUES (?, ?)",
        (account_id, time)
    )
    conn.commit()
    conn.close()


def access_read(account_id):
    """
    Read the log file
    """
    conn = sqlite3.connect("log_db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM log")
    log = cursor.fetchall()
    conn.close()
    self_log = []

    for row in log:
        row = list(row)
        if row[0] == account_id:
            row[0] = authcheck.get_username(account_id)
            self_log.append(row)

    return self_log


def check_db_log():
    """
    attempt to open the database
    """
    try:
        open("log_db.db")
    except FileNotFoundError:
        create_db_log()


def create_db_log():
    """
    Create the database
    """
    conn = sqlite3.connect("log_db.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE log (account_id TEXT, time TEXT)"
    )
    conn.commit()
    conn.close()
