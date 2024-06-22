from __future__ import annotations
from typing import List,Optional
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from models.base import db

class GithubToken(db.Model):
    __tablename__ = 'github_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token_type: Mapped[str] = mapped_column(String(40))
    access_token: Mapped[str] = mapped_column(String(200))
    refresh_token: Mapped[Optional[str]] = mapped_column(String(40))
    expires_at:Mapped[Optional[int]]= mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="github_token")

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )