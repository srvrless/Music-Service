import aioredis
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.google_auth import google_router
from src.database.config import get_db
from src.routes.images import gif_router
from src.routes.payment import payment_router
from src.routes.song import song_router
from src.routes.subscription import subscribe_router, schedule_expired_subscriptions_cleanup
from src.routes.user import user_router
from src.routes.favorite_song_library import libary_router

app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


# Initialize redis and create background task remove subscription
@app.on_event("startup")
async def startup_event(db: AsyncSession = Depends(get_db)):
    background_tasks = BackgroundTasks()
    await schedule_expired_subscriptions_cleanup(db, background_tasks)
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get('/home')
async def get_article(request: Request, ):
    return templates.TemplateResponse('base.html', {"request": request})


@app.get('/never')
async def nevermore(request: Request, ):
    return templates.TemplateResponse('music_player.html', {"request": request})


main_router = APIRouter()

# set routes to the api instance
app.include_router(gif_router)
app.include_router(user_router)
app.include_router(main_router)
app.include_router(song_router)
app.include_router(libary_router)
app.include_router(google_router)
app.include_router(payment_router)
app.include_router(subscribe_router)
