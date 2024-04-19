from typing import Annotated

from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile):
    with open(f"static/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    return templates.TemplateResponse("upload.html", {"request": request})