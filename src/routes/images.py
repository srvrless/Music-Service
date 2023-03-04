import os
import random
from logging import getLogger

from celery import Celery
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse

from src.modules.image import upload_image, get_image_filenames
from src.modules.user import oauth2_scheme

celery = Celery('tasks', broker='redis://localhost:6379')
logger = getLogger(__name__)
gif_router = APIRouter(prefix='/gif', tags=['gif'])

directory_name = "web/static/image"


# @celery.task
# TODO: delete after complete set/get images
@gif_router.get("/get")
def get_gif(token: str = Depends(oauth2_scheme)):
    out = []
    for filename in os.listdir("web/static/image"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/static/image/" + filename
        })
    return out[0]


# get image on cover
@gif_router.get("/getsss")
def get_image():
    images = get_image_filenames(directory_name)
    random_image = random.choice(images)
    path = f"{directory_name}/{random_image}"
    return FileResponse(path)


# set image on cover
@gif_router.post("/createsss")
def set_image_on_cover(image: UploadFile = File(...)):
    try:
        file_path = upload_image('web/static/image', image)
        if file_path is None:
            return HTTPException(status_code=409, detail='incorrect file type')
        return file_path
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
