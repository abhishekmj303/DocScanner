import os
import shutil
import uuid
from typing import Annotated

from fastapi import Cookie, FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    user_id: Annotated[str | None, Cookie()] = None,
):
    response = templates.TemplateResponse("index.html", {"request": request})
    print(f"User ID: {user_id}")
    if user_id is None:
        user_id = str(uuid.uuid4())
        response.set_cookie(key="user_id", value=user_id, httponly=True)
        print(f"Set cookie: {user_id}")
    return response


@app.post("/upload/")
async def create_upload_file(
    request: Request, 
    user_id: Annotated[str, Cookie()],
    files: list[UploadFile], 
):
    print(f"User ID: {user_id}")
    print({"filenames": [file.filename for file in files]})
    if os.path.exists(f"uploads/{user_id}"):
        shutil.rmtree(f"uploads/{user_id}")
    os.makedirs(f"uploads/{user_id}", exist_ok=True)
    for i, file in enumerate(files):
        file_path = f"uploads/{user_id}/{i}_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    return ""