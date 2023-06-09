from app.tasks.celery import celery
from PIL import Image
from pathlib import Path

@celery.task
def resize_image(image_path: str):
    img_path = Path(image_path)
    img = Image.open(img_path)
    img_1000_500 = img.resize((1000, 500))
    img_200_100 = img.resize((200, 100))
    img_1000_500.save(f"app/static/images/1000_500_{img_path.name}")
    img_200_100.save(f"app/static/images/200_100_{img_path.name}")