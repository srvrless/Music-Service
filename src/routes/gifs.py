import os
from logging import getLogger

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse

from src.modules.gif import create_upload_file
from src.modules.user import oauth2_scheme

logger = getLogger(__name__)
gif_router = APIRouter(prefix='/gif', tags=['gif'])


@gif_router.get("/get")
async def get_gif(token: str = Depends(oauth2_scheme)):
    out = []
    for filename in os.listdir("static/gif"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/static/gif/" + filename
        })
    return out[0]


# @gif_router.post("/create")
# async def create_gif(gif: str, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     filename = f"{gif}.gif"
#     with open(os.path.join("static/gif", filename), "wb") as f:
#         f.write(db)
#     return {"name": gif, "path": f"/static/gif/{filename}"}


@gif_router.post("/create")
async def create_gif(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        return create_upload_file(file)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
