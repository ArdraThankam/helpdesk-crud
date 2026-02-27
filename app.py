import os
import pyodbc
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn_str = os.getenv("DB_CONNECTION")

def get_connection():
    return pyodbc.connect(conn_str)

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_user(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run()
