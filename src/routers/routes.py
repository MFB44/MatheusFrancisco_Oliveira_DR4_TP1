from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

router = APIRouter()

class User(BaseModel):
    username: str
    message: Optional[str] = None

class PostUser(BaseModel):
    username: str
    age: int
USERS = []

class Item(BaseModel):
    id: int
    name: str
ITEMS = [{id: 1, "name": "item1"}, {id: 2, "name": "item2"},
          {id: 3, "name": "item3"}, {id: 4, "name": "item4"}, {id: 5, "name": "item5"}]

class Birthday(BaseModel):
    name: str
    birthday: datetime.date

@router.get("/status")
async def return_status():
    return {"message": "The server is running."}

@router.get("/user/{username}", response_model=User)
async def return_username(username: str):
    if not username:
        raise HTTPException(status_code=404, detail="Username not found.")
    return {"username": username,
            "message": (f"Welcome, {username}! Enjoy your stay.")}

@router.post("/create-user", response_model=PostUser)
async def create_user(user: PostUser):   
    global USERS
    USERS.append(user)
    if not user.username or user.age <= 0:
        raise HTTPException(status_code=400, detail="Invalid user data provided.")
    return {"username": user.username,
            "age": user.age}

@router.get("/item/{item_id}", response_model=Item)
async def return_item(item_id: int):
    if item_id not in range(1, 6):
        raise HTTPException(status_code=400, detail="Item not found.")
    return {"id": item_id,
            "name": f"item{item_id}"}

@router.delete("/item/{item_id}")
async def delete_item(item_id: int):
    if item_id not in range(1, 6):
        raise HTTPException(status_code=400, detail="Item not found.")
    return {"message": f"Item {item_id} has been deleted."}

@router.post("/birthday")
async def days_till_bday(birthday: Birthday):
    today = datetime.date.today()
    bday = birthday.birthday
    if today.month > bday.month:
        bday = bday.replace(year=today.year + 1)
    elif today.month == bday.month and today.day > bday.day:
        bday = bday.replace(year=today.year + 1)    
    else:
        bday = bday.replace(year=today.year)
    days = (bday - today).days
    return {"name": birthday.name,
            "birthday": birthday.birthday,
            "message": f"Wow, there are {days} days left untill your birthday!"}
