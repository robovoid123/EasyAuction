from typing import Optional
from sqlalchemy.orm import Session
from app.repository.repository_base import BaseRepository
from app.modules.utils.models import Image
from app.modules.utils.schemas import ImageCreate, ImageUpdate


class ImageRepository(BaseRepository[Image, ImageCreate, ImageUpdate]):
    def get_with_url(self, db: Session, url: str) -> Optional[Image]:
        return db.query(self.model).filter(self.model.url == url).first()


image_repo = ImageRepository(Image)
