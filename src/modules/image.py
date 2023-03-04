import os
from time import strftime
from typing import List

from fastapi import UploadFile, HTTPException


def get_image_filenames(directory_name: str) -> List[str]:
    return os.listdir("web/static/image")


# check image if valid extensions
def is_image(filename: str) -> bool:
    valid_extensions = (".png", ".jpg", ".jpeg", "gif")
    return filename.endswith(valid_extensions)


# upload
def upload_image(directory_name: str, image: UploadFile):
    """Upload image with add datetime on root directory"""
    if is_image(image.filename):
        timestr = strftime("%Y%m%d-%H%M%S")
        image_name = timestr + image.filename
        with open(f'{directory_name}/{image_name}', 'wb+') as image_file_upload:
            image_file_upload.write(image.file.read())
        return f"{directory_name}/{image_name}"
    raise HTTPException(status_code=404, detail=f"Image not found")
