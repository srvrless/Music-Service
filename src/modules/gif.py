# async def create_upload_file(file):
#     FILEPATH = "src/code/static/images/"
#     filename = file.filename
#     extension = filename.split('.')[1]
#
#     if extension not in ['png', 'jpg']:
#         return {"status": "error", "detail": "File extension not allowed"}
#
#     # ./static/images/hiu235tir2423ijg.png
#     token_name = secrets.token_hex(10) + "." + extension
#     generate_name = FILEPATH + token_name
#     file_content = await file.read()
#
#     with open(generate_name, "wb") as file:
#         file.write(file_content)
#
#     # PILLOW
#     img = Image.open(generate_name)
#     img = img.resize(size=(200, 200))
#     img.save(generate_name)
#
#     return await generate_name
import os
import secrets

from PIL import Image


# import secrets
# from PIL import Image

async def create_upload_file(file):
    FILEPATH = "src/code/static/images"
    filename = file.filename
    extension = filename.split('.')[-1]

    if extension not in ['png', 'jpg']:
        return {"status": "error", "detail": "File extension not allowed"}

    # ./static/images/hiu235tir2423ijg.png
    token_name = secrets.token_hex(10) + "." + extension
    generate_name = os.path.join(FILEPATH, token_name)
    os.makedirs(FILEPATH, exist_ok=True)

    async with open(generate_name, "wb") as file_out:
        file_content = await file.read()
        file_out.write(file_content)

    img = Image.open(generate_name)
    img = img.resize(size=(200, 200))
    img.save(generate_name)

    return generate_name
