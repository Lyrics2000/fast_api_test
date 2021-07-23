from uuid import uuid4, UUID
from random import randint
import sys
from typing import Optional, Text
import uvicorn
import psycopg2
from fastapi import FastAPI
from fastapi.param_functions import Body
from pydantic import BaseModel, Field, HttpUrl, EmailStr

DB_CONNECTION_STRING:str = "dbname=bonga_test user=postgres host=localhost password=postgres"


tags_metadata = [
    {
        "name": "users",
        "description": "uSER DATA JAFASF",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

class UserModel(BaseModel):
    user_id: UUID = Field(uuid4())
    username: str = Field(
        f'Username: {randint(1, 1000)}', 
        description="User's username", 
        max_length=255
        )
    email_address: EmailStr
    password: str = Field(min_length=8)
    about: str = Field("Hi there, I'm new here.", max_length=255)
    profile_picture: Optional[HttpUrl] = Field(max_length=255)

class CreateUserResponseModel(BaseModel):
    user_id: int
    username: str
    email_address: EmailStr
    about: str
    profile_picture: Optional[HttpUrl]

@app.post("/create_user/", response_model=CreateUserResponseModel)
async def user_registration(user: UserModel = Body(...)):
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)
    except psycopg2.OperationalError as e:
        print(f"Unable to connect!: {e}")
        sys.exit(1)
    else:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (user_id UUID NOT NULL PRIMARY KEY, 
                    username VARCHAR(255) UNIQUE, email_address VARCHAR NOT NULL, 
                    password VARCHAR NOT NULL, about VARCHAR, profile_picture VARCHAR(200));"""
                    )
        cur.execute(
            f"""INSERT INTO users
                (user_id, username, email_address, password, about, profile_picture)
                VALUES ({user.user_id, user.username, user.email_address, 
                user.password, user.about,user.profile_picture}
                );"""
        )
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


        