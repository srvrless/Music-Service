import aioredis
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.google_auth import google_router
from src.api.router import router
from src.database.config import get_db
from src.routes.images import gif_router
from src.routes.item import item_router
from src.routes.payment import payment_router
from src.routes.song import song_router
from src.routes.subscription import subscribe_router, schedule_expired_subscriptions_cleanup
from src.routes.user import user_router
from tests.test_del_subscription import testx_router

app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")


# Initialize redis
@app.on_event("startup")
async def startup_event(db: AsyncSession = Depends(get_db)):
    background_tasks = BackgroundTasks()
    await schedule_expired_subscriptions_cleanup(db, background_tasks)
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
app.include_router(testx_router)
app.include_router(google_router)
app.include_router(payment_router)
app.include_router(subscribe_router)
