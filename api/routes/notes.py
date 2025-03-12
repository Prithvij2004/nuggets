from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from core.db import get_session
from core.models import Notes, Users
from core.queries import get_notes_from_userid
from core.utils import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])
template = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def notes(
    request: Request,
    session: Session = Depends(get_session),
    current_user: Optional[Users] = Depends(get_current_user)
):
    if not current_user:
        return HTTPException(status_code=400, detail="User not authenticated")
    query = select(Notes).where(Notes.user_id == current_user.id)
    notes = session.exec(query).all()
    notes_list = []
    for note in notes:
        note_dict = note.model_dump()
        note_dict["id"] = str(note.id)
        note_dict["user_id"] = str(note.user_id)
        notes_list.append(note_dict)
    return template.TemplateResponse("notes_list.html", {"request": request, "notes": notes_list})

@router.post("/create", response_class=HTMLResponse)
async def create_note(
    request: Request,
    session: Session = Depends(get_session),
    content: str = Form(...),
    current_user: Optional[Users] = Depends(get_current_user)
):
    if not current_user:
        return HTTPException(status_code=400, detail="User not authenticated")
    try:
        note = Notes(content=content, user_id=current_user.id)
        session.add(note)
        session.commit()

        notes = await get_notes_from_userid(current_user.id, session)
        return template.TemplateResponse("notes_list.html", {"request": request, "notes": notes, "edit": False})
    except Exception as e:
        print(str(e))
        return HTTPException(status_code=400, detail="Could not create note")


@router.get("/{note_id}", response_class=HTMLResponse)
async def read_note(
    request: Request,
    note_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[Users] = Depends(get_current_user)
):
    if not current_user:
        return HTTPException(status_code=400, detail="User not authenticated")
    query = select(Notes).where(Notes.id == note_id, Notes.user_id == current_user.id)
    note = session.exec(query).first()
    if not note:
        return HTTPException(status_code=404, detail="Note not found")
    note_dict = note.model_dump()
    note_dict["id"] = str(note.id)
    note_dict["user_id"] = str(note.user_id)
    return template.TemplateResponse("note_form.html", {"request": request, "note": note_dict, "edit": True})

@router.put("/{note_id}/update", response_class=HTMLResponse)
async def update_post(
    request: Request,
    note_id: str,
    session: Session = Depends(get_session),
    content: str = Form(...),
    current_user: Optional[Users] = Depends(get_current_user)
):
    if not current_user:
        return HTTPException(status_code=400, detail="User not authenticated")
    query = select(Notes).where(Notes.id == note_id, Notes.user_id == current_user.id)
    note = session.exec(query).first()
    if not note:
        return HTTPException(status_code=404, detail="Note not found")
    note.content = content
    session.add(note)
    session.commit()
    notes = await get_notes_from_userid(current_user.id, session)
    return template.TemplateResponse("notes_list.html", {"request": request, "notes": notes})


