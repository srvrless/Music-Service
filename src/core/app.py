
import aioredis
from fastapi import FastAPI, Request
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.router import router
from src.routes.gifs import gif_router
from src.routes.item import item_router
from src.routes.payment import payment_router
from src.routes.song import song_router
from src.routes.user import user_router


app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


# Initialize redis
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# app.openapi = custom_openapi(app)
# @AuthJWT.load_config
# def get_config():
#     return Settings()

@app.get('/home')
async def get_article(request: Request, ):
    return templates.TemplateResponse('base.html', {"request": request})


main_router = APIRouter()

# set routes to the api instance
app.include_router(router)
app.include_router(gif_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(main_router)
app.include_router(song_router)
app.include_router(payment_router)
