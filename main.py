from sqlmodel import Session
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from core.models import Users
from api.main import api_router
from core.config import settings
from core.db import get_session
from core.utils import get_current_user


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware,secret_key=settings.SESSION_SECRET_KEY, max_age=3600 * 24 * 7)
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: Session = Depends(get_session),
    current_user: Users = Depends(get_current_user),
):
    # Here search for all the notes and return it.
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})



