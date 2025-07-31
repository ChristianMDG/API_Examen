

from typing import List

import datetime
from fastapi import FastAPI, Request, HTTPException
from pydantic.v1 import BaseModel
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"pong": "pong"}

@app.get("/home")
async def home():
    with open("home.html", "r",encoding="utf-8") as file:
        html_content=file.read()
        return HTMLResponse(content=html_content)

class Books(BaseModel):
    author: str
    title: str
    content: str
    creation_date:datetime.datetime

book_db :List[Books] =[]
@app.post("/posts")
async def posts(new_book:List[Books]):
    book_db.extend(new_book)
    return book_db

@app.get("/posts")
async def get_posts():
    return book_db

@app.put("/posts")
async def update_posts(book:Books):
    for i,existing_book in enumerate(book_db):
        if book.title == existing_book.title:
            book_db[i] = book
        book_db.append(book)
        return book_db



