from flask import Flask, render_template, request, redirect, url_for
from main import baixar_youtube, listar_pastas_musicas, criar_pasta
app = Flask(__name__)

folders = listar_pastas_musicas()
if not folders:
    criar_pasta("Favoritas")
playlist = {folder: [] for folder in folders}

@app.route("/", methods=["GET"])
def index():
    selected_folder = request.args.get("folder", folders[0])
    return render_template("index.html", folders=folders, selected_folder=selected_folder, msg=None)

@app.route("/add_folder", methods=["POST"])
def add_folder():
    new_folder = request.form.get("new_folder", "").strip()
    selected_folder = request.form.get("folder", folders[0])
    msg = None
    if new_folder and new_folder not in folders:
        new_folder_path = criar_pasta(new_folder)
        folders.append(new_folder)
        playlist[new_folder] = []
        msg = f"Pasta '{new_folder}' adicionada!"
    return render_template("index.html", folders=folders, selected_folder=selected_folder, msg=msg)

@app.route("/add_music", methods=["POST"])
def add_music():
    link = request.form.get("music_link", "").strip()
    folder = request.form.get("folder", folders[0])
    msg = None
    if link:
        playlist.setdefault(folder, []).append(link)
        baixar_youtube(link, folder)
        msg = f"Música adicionada à pasta '{folder}'!"
    return render_template("index.html", folders=folders, selected_folder=folder, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)