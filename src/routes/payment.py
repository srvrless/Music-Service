from fastapi import APIRouter, HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.api.payment import create_payment, check_if_successful_payment, payment_check

payment_router = APIRouter(tags=['payment'])


@payment_router.post("/payments")
def post_request_payment():
    try:
        return create_payment()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@payment_router.get('/status_payment')
def status_payment():
    try:
        if check_if_successful_payment():
            return {"ok": True}
        else:
            return {"wait for capture": False}
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@payment_router.get('/check_payment')
def get_order_payment():
    try:
        return payment_check()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
