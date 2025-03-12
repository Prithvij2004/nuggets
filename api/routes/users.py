from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
import requests
import secrets

from core.config import settings
from core.models import Users
from core.db import get_session

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="templates")

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI
GOOGLE_AUTH_URL=f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20email%20profile"

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/logout")
async def logout_user(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

@router.get("/auth/google")
async def google_auth(request: Request):
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state
    google_auth_url = GOOGLE_AUTH_URL + f"&state={state}"
    return RedirectResponse(url=google_auth_url)

@router.get("/auth/google/callback")
async def google_auth_callback(
    request: Request,
    code: str,
    state: str,
    session: Session = Depends(get_session),
):
    stored_state = request.session.get("oauth_state", None)
    if not stored_state or state != stored_state:
        return HTTPException(status_code=400, detail="Invalid state parameter")

    request.session.clear()
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()

    if "error" in tokens:
        return HTTPException(status_code=400, detail=tokens["error_description"])

    access_token = tokens["access_token"]
    user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    user_info = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"}).json()

    google_id = user_info["sub"]
    query = select(Users).filter(Users.google_id == google_id)
    user = session.exec(query).first()

    try:
        if not user:
            user = Users(
                google_id=google_id,
                full_name=user_info["name"],
                email=user_info["email"],
            )
            session.add(user)
            session.commit()
            session.refresh(user)
    except Exception as e:
        session.rollback()
        return HTTPException(status_code=400, detail=f"An error occurred: {e}")

    request.session["user_id"] = str(user.id)

    return RedirectResponse(url="/")
