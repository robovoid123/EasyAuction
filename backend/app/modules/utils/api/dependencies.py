import os
from uuid import uuid4
from typing import List
import aiofiles
from PIL import Image as PilImage
from fastapi import File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.modules.utils.repositories import image_repo
from app.modules.utils.models import Image
from app.modules.utils.schemas import ImageCreate
from app.dependencies import database
from app.core.config import settings

IMAGE_OUT_FILE_PATH = f"{settings.STATIC_PATH}/images"
IMAGE_STATIC_URL_PATH = f"{settings.STATIC_URL}/images"


def compress(filepath: str, size: int = 600):
    """
    alter the size of image in the given filepath
    """
    s = (size, size)
    img = PilImage.open(filepath)
    img.thumbnail(s, PilImage.ANTIALIAS)
    img.save(filepath, "JPEG")


async def upload_image(db: Session = Depends(database.get_db), image: UploadFile = File(...)) -> Image:
    """
    upload image and store image url in database
    """
    _, f_ext = os.path.splitext(image.filename)
    filename = str(uuid4()) + f_ext

    out_file_path = f"{IMAGE_OUT_FILE_PATH}/{filename}"
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
    db_obj = image_repo.create(db, obj_in=ImageCreate(
        url=f"{IMAGE_STATIC_URL_PATH}/{filename}"
    ))

    compress(out_file_path)
    return db_obj


async def upload_images(db: Session = Depends(database.get_db),
                        images: List[UploadFile] = File(...)) -> List[Image]:
    """
    upload multiple image and store image url in database
    """
    db_obj_list = []
    for image in images:
        _, f_ext = os.path.splitext(image.filename)
        filename = str(uuid4()) + f_ext
        fp = f"{IMAGE_OUT_FILE_PATH}/{filename}"
        async with aiofiles.open(fp, 'wb') as out_file:
            while content := await image.read(1024):
                await out_file.write(content)
        db_obj = image_repo.create(db, obj_in=ImageCreate(
            url=f"{IMAGE_STATIC_URL_PATH}/{filename}"
        ))
        compress(fp)
        db_obj_list.append(db_obj)
    return db_obj_list
