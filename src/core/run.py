import uvicorn
from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from settings import Settings, custom_openapi
from src.database.config import get_db
from src.models.item import ArticleSchema, Article
from src.routes.item import item_router
from src.routes.jwt_authentication import jwt_router
from src.routes.song import song_route
from src.routes.user import user_route

app = FastAPI(title="Nevless")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.openapi = custom_openapi(app)


# """"""

@app.get('/articless/')
async def get_article(db: AsyncSession = Depends(get_db)):
    myarticle = select(Article)
    res = await db.execute(myarticle)
    return res.fetchone()


@app.get('/articless/{id}')
async def get_article_by_id(id: int, db: AsyncSession = Depends(get_db)):
    myarticle = select(Article).where(Article.id == id)
    res = await db.execute(myarticle)
    return res.fetchone()


@app.post('/articles/', response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
async def add_article(article: ArticleSchema, db: AsyncSession = Depends(get_db)):
    new_article = Article(title=article.title)
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    return new_article


@app.put('/artitcles_update/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_article(id: int, article: ArticleSchema, db: AsyncSession = Depends(get_db)):
    update_article = update(Article).where(Article.id == id).values({"title": article.title}).returning(Article.title)
    res = await db.execute(update_article)
    update_user_id_row = res.fetchone()
    return update_user_id_row


@app.delete('/articles_delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id: int, db: AsyncSession = Depends(get_db)):
    query = delete(Article).where(Article.id == id)
    await db.execute(query)
    return {}


# """"""

@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("home.html", {"request": request, "id": id})


main_route = APIRouter()
# create the instance for the routes

# set routes to the api instance
main_route.include_router(user_route, prefix="/user", tags=["user"])
app.include_router(item_router)
app.include_router(main_route)
app.include_router(song_route)
app.include_router(jwt_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
