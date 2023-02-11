
#
# @app.get('/articless/')
# async def get_article(db: AsyncSession = Depends(get_db)):
#     myarticle = select(Article)
#     res = await db.execute(myarticle)
#     return res.fetchone()
#
#
# @app.get('/articless/{id}')
# async def get_article_by_id(id: int, db: AsyncSession = Depends(get_db)):
#     myarticle = select(Article).where(Article.id == id)
#     res = await db.execute(myarticle)
#     return res.fetchone()
#
#
# @app.post('/articles/', response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
# async def add_article(article: ArticleSchema, db: AsyncSession = Depends(get_db)):
#     new_article = Article(title=article.title)
#     db.add(new_article)
#     await db.commit()
#     await db.refresh(new_article)
#     return new_article
#
#
# @app.put('/artitcles_update/{id}', status_code=status.HTTP_202_ACCEPTED)
# async def update_article(id: int, article: ArticleSchema, db: AsyncSession = Depends(get_db)):
#     update_article = update(Article).where(Article.id == id).values({"title": article.title}).returning(Article.title)
#     res = await db.execute(update_article)
#     update_user_id_row = res.fetchone()
#     return update_user_id_row
#
#
# @app.delete('/articles_delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_article(id: int, db: AsyncSession = Depends(get_db)):
#     query = delete(Article).where(Article.id == id)
#     await db.execute(query)
#     return {}
#
