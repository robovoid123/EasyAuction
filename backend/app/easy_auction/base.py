from sqlalchemy.orm import Session
from app.crud.base import CRUDBase


class Base:
    def __init__(self, crud: CRUDBase, db: Session):
        self.crud = crud(db)

    def get(self, id):
        return self.crud.get(id)

    def get_multi(self, skip=0, limit=10):
        return self.crud.get_multi(skip=skip, limit=limit)

    def create(self, obj_in):
        return self.crud.create(obj_in=obj_in)

    def update(self, db_obj, obj_in):
        return self.crud.update(db_obj=db_obj, obj_in=obj_in)

    def remove(self, id):
        return self.crud.remove(id)
