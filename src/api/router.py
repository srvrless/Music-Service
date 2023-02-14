from fastapi import APIRouter, BackgroundTasks, Depends


from .tasks import send_email_report_dashboard
from ..modules.user import get_current_user_from_token

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(get_current_user_from_token)):
    # 1400 ms - Клиент ждет
    send_email_report_dashboard(user.username)
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }