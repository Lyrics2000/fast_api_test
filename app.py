
import uvicorn
from fastapi import FastAPI

from handler import add_user_to_db
from settings import APP_PORT

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


@app.post("/create_user/")
async def user_registration(user: dict):
    app =  add_user_to_db(user)
    return app

    
        
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(APP_PORT))


        