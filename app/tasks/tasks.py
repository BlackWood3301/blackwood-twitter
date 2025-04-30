from app.tasks.celery import celery
from PIL import Image
from pathlib import Path

@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    