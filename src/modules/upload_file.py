import secrets

from PIL import Image
from fastapi import UploadFile, File, Depends
from fastapi_jwt_auth import AuthJWT


async def create_upload_file(file: UploadFile = File(...), user: AuthJWT = Depends()):
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split('.')[1]

    if extension not in ['png', 'jpg']:
        return {"status": "error", "detail": "File extension not allowed"}

    # ./static/images/hiu235tir2423ijg.png
    token_name = secrets.token_hex(10) + "." + extension
    generate_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generate_name, "wb") as file:
        file.write(file_content)

    # PILLOW
    img = Image.open(generate_name)
    img = img.resize(size=(200, 200))
    img.save(generate_name)

    file.close()

    return generate_name
