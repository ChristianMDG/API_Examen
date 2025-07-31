

from typing import List


from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, json
from starlette.responses import HTMLResponse, Response

app = FastAPI()


@app.get("/ping")
async def ping():
    return Response("pong")

@app.get("/home")
async def home():
    with open("home.html", "r",encoding="utf-8") as file:
        html_content=file.read()
        return HTMLResponse(content=html_content)



class Books(BaseModel):
    author: str
    title: str
    content: str
    creation_date:str

book_db :List[Books] =[]
@app.post("/posts",status_code=201,response_model=List[Books])
async def posts(new_book:List[Books]):
    book_db.extend(new_book)
    return book_db

@app.get("/posts",response_model=List[Books],status_code=200)
async def get_posts():
    return book_db

@app.put("/posts",status_code=202,response_model=List[Books])
async def update_posts(book:Books):
    for i,existing_book in enumerate(book_db):
        if book.title == existing_book.title:
            book_db[i] = book
    book_db.append(book)
    return book_db


@app.get("/get/ping/auth")
async def get_auth(request:Request):
    auth = request.headers.get("Authorization")
    if auth is None:
        raise HTTPException(status_code=401,detail="Authorization header missing")
    if auth != "123456":
        raise HTTPException(status_code=401,detail="Authorization header invalid")
    return Response("pong")

@app.get("/{full_path:path}",status_code=404)
def error():
    with open("404.html", "r",encoding="utf-8") as file:
        html_content=file.read()
        return HTMLResponse(content=html_content)
