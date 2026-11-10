from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    conn = get_connection()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    conn = get_connection()
    conn.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    conn = get_connection()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
            (title, content, note_id),
        )

        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()

    if note is None:
        return "Catatan tidak ditemukan", 404

    return render_template("edit.html", note=note)

if __name__=="__main__":
    app.run(debug=True)