from flask import Flask, render_template
from database import get_connection, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    conn = get_connection()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

if __name__=="__main__":
    app.run(debug=True)