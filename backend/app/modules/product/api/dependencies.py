from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import auth, database

from app.modules.user.models.user import User
from app.modules.product.repositories import product_repo
from app.modules.product.models import Product

PRODUCT_NOT_EXIST_EXCEPTION = HTTPException(
    status_code=404, detail="product dose not exists")
NOT_OWNER_EXCEPTION = HTTPException(
    status_code=401, detail="only owner can do this action")


def get_product(id: int,
                db: Session = Depends(database.get_db)):
    db_obj = product_repo.get(db, id)
    if not db_obj:
        raise PRODUCT_NOT_EXIST_EXCEPTION
    return db_obj


def get_current_product_owner(prod_db: Product = Depends(get_product),
                              current_user: User = Depends(auth.get_current_active_user)):
    if prod_db.owner_id != current_user.id:
        raise NOT_OWNER_EXCEPTION
    return current_user
