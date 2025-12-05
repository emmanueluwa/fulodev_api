"""
JSON -> BlogPost -> SQL
SQL -> BogPost -> JSON
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class BlogPost(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    title: str
    text: str


# db setup

sqlite_url = "sqlite:///blog.db"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/create_blog/", response_model=BlogPost)
def create_blog(post: BlogPost):
    with Session(engine) as session:
        session.add(post)
        session.commit()
        session.refresh(post)

        return post


@app.get("/blogs/", response_model=list[BlogPost])
def read_blogs():
    with Session(engine) as session:
        blogs = session.exec(select(BlogPost)).all()

        return blogs


@app.get("/blogs/{blog_id}", response_model=BlogPost)
def read_blog(blog_id: int):
    with Session(engine) as session:
        blog = session.get(BlogPost, blog_id)

        if not blog:
            raise HTTPException(
                status_code=404, detail=f"Blog with id {blog_id} does not exist"
            )

        return blog
