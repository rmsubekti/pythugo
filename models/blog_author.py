from sqlalchemy import Table, Column, ForeignKey
from models.base import db

blog_author = Table(
    "blog_author",
    db.metadata,
    Column("author_id", ForeignKey("author.id"), primary_key=True),
    Column("blog_id", ForeignKey("blog.id"), primary_key=True),
)