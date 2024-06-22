from __future__ import annotations
from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String,DateTime, func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from models.base import db
from models.blog_author import blog_author

class Blog(db.Model):
    __tablename__ = 'blog'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    branch: Mapped[str] = mapped_column(String(150))
    repo: Mapped[str] = mapped_column(String(150))
    owner_id: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),insert_default=func.now())
    authors: Mapped[List["Author"]] = relationship(
        secondary=blog_author, back_populates="blogs"
    )

def __repr__(self) -> str:
    return f"Blog(id={self.id!r}, name={self.name!r}, branch={self.branch!r}, repo={self.repo!r}, owner_id={self.owner_id!r}, create_date={self.create_date!r})"
