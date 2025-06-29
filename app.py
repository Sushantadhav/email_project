from flask import Flask, render_template, request
import sqlite3
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# SQLite DB setup
db = sqlite3.connect("emails.db", check_same_thread=False)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
db.commit()

@app.route('/', methods=["GET", "POST"])
def index():
    message = ""
    success_message = ""

    if request.method == "POST":
        email = request.form.get("email")
        if email:
            try:
                cursor.execute("INSERT INTO subscribers1 (email) VALUES (?)", (email,))
                db.commit()
                success_message = "Thanks for joining!"
            except sqlite3.IntegrityError:
                message = "This email is already registered."

    cursor.execute("SELECT COUNT(*) FROM subscribers1")
    count = cursor.fetchone()[0]

    return render_template("index.html", count=count, message=message, success_message=success_message)

@app.route('/admin')
def admin_dashboard():
    cursor.execute("SELECT email, created_at FROM subscribers1")
    subscribers = cursor.fetchall()
    return render_template("admin_dashboard.html", subscribers=subscribers)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # default 5000 for local testing
    app.run(host="0.0.0.0", port=port)