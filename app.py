from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    conn = get_connection()
    notes = conn.execute(
        "SELECT * FROM notes ORDER BY is_pinned DESC, id DESC"
        ).fetchall()
    items = conn.execute("SELECT * FROM checklist_items ORDER BY id").fetchall()
    conn.close()
    
    items_by_note = {}
    for item in items:
        items_by_note.setdefault(item["note_id"], []).append(item)
    
    return render_template("index.html", notes=notes, items_by_note=items_by_note)

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

@app.route("/pin/<int:note_id>", methods=["POST"])
def pin_note(note_id):
    conn = get_connection()
    conn.execute(
        "UPDATE notes SET is_pinned = 1 - is_pinned WHERE id = ?",
        (note_id,),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/note/<int:note_id>/items/add", methods=["POST"])
def add_item(note_id):
    text = request.form["text"].strip()

    if text:
        conn = get_connection()
        conn.execute(
            "INSERT INTO checklist_items (note_id, text) VALUES (?, ?)",
            (note_id, text),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)