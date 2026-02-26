from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tickets = []

@app.route("/")
def home():
    return render_template("index.html", tickets=tickets)

@app.route("/add", methods=["POST"])
def add_ticket():
    title = request.form["title"]
    description = request.form["description"]
    tickets.append({"title": title, "description": description})
    return redirect("/")

@app.route("/delete/<int:index>")
def delete_ticket(index):
    tickets.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run()
