import stripe as stripe
from fastapi import APIRouter, BackgroundTasks
from fastapi_cache.decorator import cache
from loguru import logger
from src.layouts.dal_user import UserDAL
from src.routes.images import get_gif

router = APIRouter(prefix="/report")
stripe.api_key = "STRIPE_KEY"


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks):
    # 1400 ms - Клиент ждет
    get_gif()
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    background_tasks.add_task(get_gif)
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    get_gif.delay()
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }


# data
stars = {
    "Bruce Willis": {"movies": ["Die Hard", "Blind Date"]},
    "Arnold Shwarzenegger": {"movies": ["Terminator", "Conan", "Commando"]},
    "Sylvester Stallone": {"movies": ["Rambo", "Cobra", "Over the Top"]},
}


@router.get("/fetch")
@cache(expire=3)
async def fetch():
    """returns 80s movie stars"""
    logger.info("fetching movie stars to front end (Vue)")
    return stars


