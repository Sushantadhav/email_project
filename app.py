from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session

# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SushantMysql",
    database="email_project1",
    connection_timeout=600 
)
cursor = db.cursor()

@app.route('/', methods=["GET", "POST"])
def index():
    message = ""
    success_message = ""

    if request.method == "POST":
        email = request.form.get("email")
        if email:
            try:
                cursor.execute("INSERT INTO subscribers1 (email) VALUES (%s)", (email,))
                db.commit()
                success_message = "Thanks for joining!"
            except mysql.connector.IntegrityError:
                message = "This email is already registered."

    # Always get the updated subscriber count
    cursor.execute("SELECT COUNT(*) FROM subscribers1")
    count = cursor.fetchone()[0]

    # Only set the success message if the email was successfully added
    if request.method == "POST" and not message:
        success_message = f"Thanks for joining! {count} people have already joined."

    return render_template("index.html", count=count, message=message, success_message=success_message)

@app.route('/admin', methods=["GET"])
def admin_dashboard():
    cursor.execute("SELECT email, created_at FROM subscribers1")
    subscribers = cursor.fetchall()
    
    return render_template("admin_dashboard.html", subscribers=subscribers)

if __name__ == '__main__':
    app.run(debug=False)