# crud - create/read/update/delete

from sqlalchemy import select
from models import session, Note


def create_notes(title: str, content: str):
    with session() as conn:
        note = Note(title=title, content=content)
        # Создаем объект python, его НЕТ в базе и сразу добавляем через подключение (conn.add)
        conn.add(note)
        # подтверждение добавления
        conn.commit()
        conn.refresh(note)
    return note


def add_note():
    with session() as conn:
        conn.add(Note(title="cats", content="some cats"))
        conn.commit()


def get_note(uuid):
    with session() as conn:
        query = select(Note).where(Note.uuid == uuid)
        # (User,) - one()
        # User - scalar_one()
        return conn.execute(query).scalar_one()


def get_all_notes():
    with session() as conn:
        return conn.execute(select(Note)).scalars().all()
