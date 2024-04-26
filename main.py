import os
import shutil
import time
import uuid
from typing import Annotated

from fastapi import BackgroundTasks, Cookie, FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from docscanner.scanner import DocScanner

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

scanner = DocScanner()


@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    user_id: Annotated[str | None, Cookie()] = None,
):
    response = templates.TemplateResponse("index.html", {"request": request})
    print(f"User ID: {user_id}")

    # Set a cookie if it doesn't exist
    if user_id is None:
        user_id = str(uuid.uuid4())
        response.set_cookie(key="user_id", value=user_id, httponly=True)
        print(f"Set cookie: {user_id}")

    return response


@app.post("/upload/")
async def create_upload_file(
    user_id: Annotated[str, Cookie()],
    files: list[UploadFile],
    background_tasks: BackgroundTasks,
):
    print(f"User ID: {user_id}")
    print({"filenames": [file.filename for file in files]})

    # Create a directory for the user
    if os.path.exists(f"uploads/{user_id}"):
        shutil.rmtree(f"uploads/{user_id}")
    os.makedirs(f"uploads/{user_id}", exist_ok=True)

    # Save the uploaded files
    for i, file in enumerate(files):
        file_path = f"uploads/{user_id}/{i}_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
    
    # Create a PDF document
    pdf_path = scanner.create_document(f"uploads/{user_id}")

    # Clean up the uploaded and processed files
    shutil.rmtree(f"uploads/{user_id}")
    shutil.rmtree(f"scans/{user_id}")
    background_tasks.add_task(delete_document, user_id)

    return HTMLResponse("", headers={"HX-Redirect": pdf_path})


def delete_document(user_id: str):
    # Retain the document for an hour
    time.sleep(60*65)

    document_path = f"static/content/{user_id}/document.pdf"
    if os.path.exists(document_path):
        modify_time = os.path.getmtime(document_path)
        current_time = time.time()

        # Delete the document if it was last modified over an hour ago
        if current_time - modify_time > 60*60:
            os.remove(document_path)
            print(f"Deleted document for user {user_id}")


def cleanup():
    # Clean up the uploads and scans directories
    for directory in ["uploads", "scans", "static/content"]:
        if os.path.exists(directory):
            shutil.rmtree(directory)


cleanup()