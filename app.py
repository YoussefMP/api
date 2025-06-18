from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import FileResponse
from pydantic import EmailStr, BaseModel
from typing import Union, List
import json 
import os 

app = FastAPI()

GUID = ["b963d4f0-cb8b-46c4-ba31-f6aabab21fcf"]
client = None
CLIENTS = {
    "b963d4f0-cb8b-46c4-ba31-f6aabab21fcf": "90",
}

class Token(BaseModel): 
    token: str

def get_current_user(token: str = Header()):
    global client 
    global CLIENTS
    client = CLIENTS[token]

    if token not in GUID:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token",
                            )
    else:
        return token

router = APIRouter(dependencies=[Depends(get_current_user)])
content: List[str] = []

def read_content():
    file = open("./Data/Data.txt", "r", encoding="utf-8")
    content = file.readlines()
    file.close()
    return content 

@router.get("/")
async def read_root():
    return "You get data, You get Data, EVERYBODY gets Data"

@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    global content
    if not content:
        content = read_content()
    return content[item_id]

@router.get("/list")
async def list_content():
    global client 
    if not os.path.exists(f"./Data/{client}"):
        return {
            "client": client,
            "current_path": os.listdir(),
            "check": os.path.exists(f"./Data/{client}",
            "Check1": os.path.exists(f".\\Data\\{client}"),
            "Check2": os.path.exists(f".\\..\\Data\\{client}"),
        }
    files = os.listdir(f"./Data/{client}")
    response = []
    for file in files:
        if file.endswith(".json"):
            metadata_file = open(f"./Data/{client}/{file}", "r", encoding="utf-8")
            response.append(json.load(metadata_file))

    return response

@router.get("/file/{file_name}")
async def send_file(file_name: str):
    try:
        return FileResponse(f"./Data/{client}/{file_name}")
    except FileNotFoundError:
        return {"error": "File not found!"}

app.include_router(router)
