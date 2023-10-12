import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class UserAttrs(BaseModel):
    name: str
    email: str


class User(UserAttrs):
    id: int


collection = [
  User(id=1, name='Ирина', email='rter@gmail.com'),
  User(id=2, name='Сергей', email='koles@mail.ru')
]


@app.get('/users/', response_class=HTMLResponse)
def users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": collection})


@app.post('/users/')
def create_users(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()]):
    user = User(id=len(collection) + 1, email=email, name=name)
    collection.append(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": collection})


@app.get('/users/{id}', response_model=User)
def get_user(id: int):
    for user in collection:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")



@app.put('/users/{id}', response_model=User)
def update_task(id: int, attrs: UserAttrs):
    for user in collection:
        if user.id == id:
            user.email = attrs.email
            user.name = attrs.name
            return user
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete('/users/{id}', response_model=dict)
def destroy_user(id: int):
    for user in collection:
        if user.id == id:
            collection.remove(user)
            return {'message': 'Destroy was success'}
    raise HTTPException(status_code=404, detail="Task not found")



if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
