from sqlmodel import Session, select

from core.models import Notes

async def get_notes_from_userid(user_id: str, session: Session) -> list[Notes]:
    query = select(Notes).where(Notes.user_id == user_id)
    notes = session.exec(query).all()
    result = []
    for note in notes:
        note_dict = note.model_dump()
        note_dict["id"] = str(note.id)
        note_dict["user_id"] = str(note.user_id)
        result.append(note_dict)
    return result
