"""
JSON -> BlogPost -> SQL
SQL -> BogPost -> JSON
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class BlogPost(SQLModel, table=True):
    id
    date: datetime = Field(default_factory=datetime.now)
    title: str
    text: str
