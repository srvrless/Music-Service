from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.api.payment import create_payment, check_if_successful_payment, payment_check
from src.modules.user import oauth2_scheme

payment_router = APIRouter(tags=['payment'])


# create payment
@payment_router.post("/payments")
def post_request_payment(token: str = Depends(oauth2_scheme)):
    try:
        return create_payment()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


# check status payment
@payment_router.get('/status_payment')
def status_payment(token: str = Depends(oauth2_scheme)):
    try:
        if check_if_successful_payment():
            return {"ok": True}
        else:
            return {"wait for capture": False}
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


# return check your subscription
@payment_router.get('/check_payment')
def get_order_payment(token: str = Depends(oauth2_scheme)):
    try:
        return payment_check()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
