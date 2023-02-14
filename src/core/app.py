# from settings import Settings, custom_openapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from loguru import logger
from redis import asyncio as aioredis

from src.routes.gifs import gif_router
from src.routes.item import item_router
from src.routes.song import song_router
from src.routes.user import user_router

# from src.routes.jwt_authentication import jwt_router

app = FastAPI(title="Nevless")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="web/templates")


# app.openapi = custom_openapi(app)


# from api.views import main
@app.get('/home')
async def get_article(request: Request, ):
    return templates.TemplateResponse('base.html', {"request": request})

# data
stars = {
    "Bruce Willis": {"movies": ["Die Hard", "Blind Date"]},
    "Arnold Shwarzenegger": {"movies": ["Terminator", "Conan", "Commando"]},
    "Sylvester Stallone": {"movies": ["Rambo", "Cobra", "Over the Top"]},
}

# Initialize redis
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/fetch")
@cache(expire=30)
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
