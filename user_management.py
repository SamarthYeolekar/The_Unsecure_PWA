import sqlite3 as sql
import time
import random
import bleach
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, dateOfBirth) VALUES (?, ?, ?)",
        (username, password, DoB),
    )
    con.commit()
    con.close()

def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cur.fetchone() is None:
        con.close()
        return False
    else:
        cur.execute("SELECT * FROM users WHERE password = ?", (password,))
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() is None:
            con.close()
            return False
        else:
            con.close()
            return True

def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (feedback) VALUES (?)", (feedback,))
    con.commit()
    con.close()

def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    with open("templates/partials/success_feedback.html", "w") as f:
        for row in data:
            sanitized_feedback = bleach.clean(row[1])
            f.write("<p>\n")
            f.write(f"{sanitized_feedback}\n")
            f.write("</p>\n")

if __name__ == "__main__":
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=True,
    )
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)