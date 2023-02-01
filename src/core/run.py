import uvicorn

from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from settings import Settings, custom_openapi
from src.routes.item import item_router
from src.routes.jwt_authentication import jwt_router
from src.routes.song import song_route
from src.routes.user import user_route
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.openapi = custom_openapi(app)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("home.html", {"request": request, "id": id})

# create the instance for the routes
main_route = APIRouter()

# set routes to the api instance
main_route.include_router(user_route, prefix="/user", tags=["user"])
app.include_router(item_router)
app.include_router(main_route)
app.include_router(song_route)
app.include_router(jwt_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
