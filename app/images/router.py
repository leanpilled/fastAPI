from fastapi import APIRouter, UploadFile
import shutil

from app.tasks.tasks import resize_image

router = APIRouter(
    prefix="/images",
    tags=["images"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    img_path = f"app/static/images/{name}.webp"
    with open(img_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    resize_image.delay(img_path)