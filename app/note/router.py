# app/note/router.py
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    await file.read()
    # https://picsum.photos/200/200
    # return {"url": "https://fastly.picsum.photos/id/477/1920/1080.jpg?hmac=8V4fJHSP89AfrwJxObukCzN7UvUriZ6QbXAC6lL-zDs"}
    return {"url": "https://fastly.picsum.photos/id/867/200/200.jpg?hmac=o_T4KIW6jPbGySRv8Em8TaP9PH_tgegfmPaYJJ394Y4"}
    # return {"url": "http://localhost:9090/test.png"}