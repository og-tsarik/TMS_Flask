from flask import Flask, request, Response, render_template, redirect, url_for
from sqlalchemy import exc
from crud import create_notes, add_note, get_note, get_all_notes
from models import drop_tables, create_tables

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static-files/"
)

drop_tables()
create_tables()
add_note()


@app.route("/", methods=["GET"])
def home_page_view():
    all_notes = get_all_notes()
    return render_template("home.html", notes=all_notes)


@app.route("/create_post", methods=["GET"])
def get_register_page_view():
    return render_template("create_post.html")


@app.route("/create_post", methods=["POST"])
def register_note_view():
    note_data = request.form
    try:
        note = create_notes(
            title=note_data["title"],
            content=note_data["content"]
        )
    except exc.IntegrityError:
        return f"""Ошибка! Запись с заголовком" {note_data['title']}" уже существует!"""
    return redirect(url_for("home_page_view", uuid=note.uuid))


@app.route("/<uuid>", methods=["GET"])
def note_view(uuid):
    try:
        note = get_note(uuid)
    except exc.NoResultFound:
        return Response("Запись не найдена", status=404)
    return render_template(
        "note_view.html",
        uuid=note.uuid,
        title=note.title,
        content=note.content,
        created_ad=note.created_at
    )
