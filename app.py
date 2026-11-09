from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    nama = "Ragil"
    daftar_catatan = [
        "Belajar Flask",
        "Bikin proyek Keep Clone",
        "Push ke GitHub",
        "Portofolio mandiri"
    ]
    return render_template("index.html", nama=nama, daftar_catatan=daftar_catatan)

if __name__=="__main__":
    app.run(debug=True)