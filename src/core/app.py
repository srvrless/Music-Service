# from settings import Settings, custom_openapi

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from src.routes.gifs import gif_router
from src.routes.item import item_router
# from src.routes.jwt_authentication import jwt_router
from src.routes.song import song_router
from src.routes.user import user_router

app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# app.openapi = custom_openapi(app)


# from api.views import main
@app.get('/home/', response_class=HTMLResponse)
async def get_article(request: Request, ):
    return templates.TemplateResponse('home.html', {"request": request})


stars = {
    "Bruce Willis": {"movies": ["Die Hard", "Blind Date"]},
    "Arnold Shwarzenegger": {"movies": ["Terminator", "Conan", "Commando"]},
    "Sylvester Stallone": {"movies": ["Rambo", "Cobra", "Over the Top"]},
}


@app.get("/fetch")
async def fetch():
    """returns 80s movie stars"""
    logger.info("fetching movie stars to front end (Vue)")
    return stars


# @AuthJWT.load_config
# def get_config():
#     return Settings()

main_router = APIRouter()
# create the instance for the routes

# set routes to the api instance
app.include_router(gif_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(main_router)
app.include_router(song_router)
# app.include_router(jwt_router)
