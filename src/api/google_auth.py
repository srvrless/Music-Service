from fastapi import APIRouter, HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.models.user import User
from src.schemas.user import ShowSignUp, Token, CreateUserModel, Google_Token

from src.utils.jwt_token import create_access_token, create_token

google_router = APIRouter(tags=["auth_google"])
GOOGLE_CLIENT_ID = "42683423809-js6evf69ea36budsv10dvt5d7vqa4dr6.apps.googleusercontent.com"
templates = Jinja2Templates(directory="web/templates")


async def create_user(user: CreateUserModel) -> User:
    _user = await User.objects.get_or_create(**user.dict(exclude={"token"}))
    return _user


async def google_auth(user: CreateUserModel) -> tuple:
    try:
        idinfo = id_token.verify_oauth2_token(user.token, requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(403, "Bad code")
    user = await create_user(user)
    internal_token = create_token(user.user_id)
    return user.user_id, internal_token.get("access_token")


@google_router.get('/sss')
async def google_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@google_router.post('/google/auth', response_model=Google_Token)
async def google_auth(user: CreateUserModel):
    id, token = await google_auth(user)
    return Google_Token(user_id=id, token=token)


