from typing import Optional
import uuid
from fastapi import Depends, Request
from sqlmodel import Session, select

from core.models import Users
from core.db import get_session

async def get_current_user(request: Request, session: Session = Depends(get_session)) -> Optional[Users]:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    query = select(Users).where(Users.id == user_id)
    user: Users | None= session.exec(query).first()
    user.id = str(user.id) #type: ignore
    return user
