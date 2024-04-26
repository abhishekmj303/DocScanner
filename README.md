# DocScanner

DocScanner is a simple tool to scan a document and create a PDF file from it. It uses OpenCV to detect the document in the image and then uses the detected document to create a PDF file.

## Frontend
- Change order of images before uploading
- Upload progress bar
- Processing animation

## Backend
- Isolate different anonymous users
- Robust edge detection
- Perspective transformation
- Auto add filters to final images
- Create PDF document
- Auto delete generated document after 1 hour

## Setup Requirements

```bash
sudo apt install libgl1
```

```
pip install -r requirements.txt
```

## Usage

**Development:**
```
tailwindcss -i static/src/input.css -o static/dist/css/output.css --watch
```
```
uvicorn main:app --reload
```

**Production:**
```
tailwindcss -i static/src/input.css -o static/dist/css/output.css --minify
uvicorn main:app --port 8778
```