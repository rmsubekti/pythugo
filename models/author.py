from __future__ import annotations
from typing import List,Optional
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from models.base import db
from models.blog import Blog
from models.blog_author import blog_author
from models.github_token import GithubToken

class Author(db.Model):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(64), unique=True)
    name : Mapped[str] = mapped_column(String(100))
    avatar_url : Mapped[str] = mapped_column(String(200))
    email : Mapped[Optional[str]] = mapped_column(String(100))
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),insert_default=func.now())
    github_token: Mapped["GithubToken"] = relationship(back_populates="author")
    blogs: Mapped[List["Blog"]] = relationship(
        secondary=blog_author, back_populates="authors"
    )

def __repr__(self) -> str:
    return f"Author(id={self.id!r}, username={self.username!r}, name={self.name!r}, avatar_url={self.avatar_url!r}, email={self.email!r}, token={self.token!r}, created_date={self.created_date!r})"

