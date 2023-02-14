from pydantic import BaseModel
from sqlalchemy import String, Boolean, Integer, Column, Text

from src.database.config import Base


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Item name={self.name} price={self.price}>"


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)


class ArticleSchema(BaseModel):
    id: int
    title: str
