from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Header, File, UploadFile, Form, Query
from fastapi.responses import FileResponse, JSONResponse
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
    client = CLIENTS.get(token)

    if token not in GUID:

        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid request"
        )

        # return JSONResponse(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     content={"status": "Invalid Request"}
        # )

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


@router.post("/establish-connection")
async def authenticate_user():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "connected", "permissions": "admin"}
    )
    

@router.get("/list-files")
async def list_files():
    response = []
    if os.path.exists(f"./Data/{client}/Unecessary"):
        files = os.listdir(f"./Data/{client}/Unecessary")
        print(files)

        for file_id in range(len(files)):
            response.append({"id": file_id,
                            "name": files[file_id],
                            "description": ""
                            })

    return {"files": response}


@router.post("/request-file")
async def request_file(
    file: UploadFile = File(...),
    location_id: str = Form(None)
):
    try:
        if not file:
            return JSONResponse(
                status_code=400,
                content={"status": "invalidrequest", "message": "Malformed request or missing file"}
            )

        else:                     
            contents = await file.read()
            file_size = len(contents)
            await file.seek(0)
            max_size_mb = 25
            max_size_bytes = max_size_mb * 1024 * 1024

            if file_size > max_size_bytes:
                return "File is too large (over 25 MB)."
            else:
                save_path = f"./Data/{client}/Received/{file.filename}"
                with open(save_path, "wb") as f:
                    f.write(contents)

                # Here you would handle the file (e.g. save, process, etc.)
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "accepted",
                        "location_id": location_id or "unspecified",
                        "message": "File submitted for processing"
                    }



        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )



@router.get("/request-targetfile")
async def request_targetfile(location_id: str = Query(None)):
    if not location_id:
        return JSONResponse(
            status_code=400,
            content={"status": "invalidrequest", "message": "Missing location_id"}
        )

    try:
        # Replace with actual file lookup logic
        file_path = f"./Data/{client}/Outputs/result_{location_id}.zip"

        # Simulate file not found
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={"status": "notfound", "message": "File not found or access denied"}
            )

        return FileResponse(
            path=file_path,
            media_type='application/zip',
            filename=f"result_{location_id}.zip"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )




# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     global content
#     if not content:
#         content = read_content()
#     return content[item_id]

# @router.get("/list")
# async def list_content():
#     global client 
#     if not os.path.exists(f"./Data/{client}"):
#         return {
#             "client": client,
#             "current_path": os.listdir(),
#             "check": os.path.exists(f"./Data/{client}"),
#             "Check1": os.path.exists(f".\\Data\\{client}"),
#             "Check2": os.path.exists(f".\\..\\Data\\{client}"),
#         }
#     files = os.listdir(f"./Data/{client}")
#     response = []
#     for file in files:
#         if file.endswith(".json"):
#             metadata_file = open(f"./Data/{client}/{file}", "r", encoding="utf-8")
#             response.append(json.load(metadata_file))

#     return response

# @router.get("/file/{file_name}")
# async def send_file(file_name: str):
#     try:
#         return FileResponse(f"./Data/{client}/{file_name}")
#     except FileNotFoundError:
#         return {"error": "File not found!"}

app.include_router(router)
