import random

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from src.modules.image import upload_image, get_image_filenames

gif_router = APIRouter(prefix='/image', tags=['image'])

directory_name = "web/static/image"


# get image on cover
@gif_router.get("/")
def get_image():
    images = get_image_filenames(directory_name)
    random_image = random.choice(images)
    path = f"{directory_name}/{random_image}"
    return FileResponse(path)


# set image on cover
@gif_router.post("/")
def set_image_on_cover(image: UploadFile = File(...)):
    try:
        file_path = upload_image('web/static/image', image)
        if file_path is None:
            return HTTPException(status_code=409, detail='incorrect file type')
        return file_path
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
