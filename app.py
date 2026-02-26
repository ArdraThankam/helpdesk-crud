from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# 🔹 Azure SQL Connection
conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:helpdeskardra.database.windows.net,1433;"
    "Database=helpdeskardra;"
    "Uid=CloudSAeb57e490;"
    "Pwd=;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 🔹 Create table if not exists
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Tickets' AND xtype='U')
CREATE TABLE Tickets (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(200),
    Description NVARCHAR(MAX),
    CreatedAt DATETIME DEFAULT GETDATE()
)
""")
conn.commit()


@app.route("/")
def home():
    cursor.execute("SELECT * FROM Tickets ORDER BY Id DESC")
    rows = cursor.fetchall()

    tickets = []
    for row in rows:
        tickets.append({
            "id": row[0],
            "title": row[1],
            "description": row[2]
        })

    return render_template("index.html", tickets=tickets)


@app.route("/add", methods=["POST"])
def add_ticket():
    title = request.form["title"]
    description = request.form["description"]

    cursor.execute(
        "INSERT INTO Tickets (Title, Description) VALUES (?, ?)",
        title, description
    )
    conn.commit()

    return redirect("/")


@app.route("/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    cursor.execute("DELETE FROM Tickets WHERE Id = ?", ticket_id)
    conn.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run()
