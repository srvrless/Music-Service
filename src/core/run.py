import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from src.routes.user import user_route
from src.routes.song import song_route
from src.routes.auth_routes import auth_router
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth import AuthJWT
from src.schemas.authentication import Settings

app = FastAPI(title="Nevless")


@AuthJWT.load_config
def get_config():
    return Settings()


app.mount("/static", StaticFiles(directory="static"), name="static")

# @api.get("/")
# async def hello_world():
#     return "hello_world"


# create the instance for the routes
main_route = APIRouter()

# set routes to the api instance
main_route.include_router(user_route, prefix="/user", tags=["user"])
app.include_router(main_route)
app.include_router(song_route)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
