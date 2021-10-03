from typing import List
from app.modules.utils.models.image import Image
from app.modules.product.schemas.product import ProductInDB
from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app.dependencies import database, auth

from app.modules.user.models import User
from app.modules.product.schemas import (ProductCreate, ProductUpdate)
from app.modules.product.repositories import product_repo, category_repo
from app.modules.utils.api.dependencies import upload_image
from app.modules.utils.repositories import image_repo

router = APIRouter()
PRODUCT_NOT_FOUND_EXCEPTION = HTTPException(status_code=404, detail="product not found")


@router.post("/{id}/images")
async def add_image(*,
                    id: int,
                    db: Session = Depends(database.get_db),
                    image: Image = Depends(upload_image),
                    current_user: User = Depends(auth.get_current_active_user)):
    product = product_repo.get(db, id=id)
    if not product:
        raise PRODUCT_NOT_FOUND_EXCEPTION

    product_repo.add_image(db, db_obj=product, image=image)
    return {"url": image.url}


@router.delete("/{id}/images")
def remove_image(*,
                 id: int,
                 image_url: str = Body(...),
                 db: Session = Depends(database.get_db),
                 current_user: User = Depends(auth.get_current_active_user)):
    product = product_repo.get(db, id=id)
    if not product:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    image = image_repo.get_with_url(db, url=image_url)
    if image:
        product_repo.remove_image(db, db_obj=product, image=image)


@router.post("/", status_code=201)
def create_product(*,
                   product_in: ProductCreate,
                   categories: List[str] = Body(None),
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    product = product_repo.create_with_user(
        db, obj_in=product_in, owner_id=current_user.id)
    categories = category_repo.get_with_names(db, names=categories)
    product_repo.add_categories(db, db_obj=product, categories=categories)
    return product


@router.get("/", response_model=List[ProductInDB])
def get_products(*,
                 skip: int = 0,
                 limit: int = 5,
                 db: Session = Depends(database.get_db)):
    return product_repo.get_multi(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=List[ProductInDB])
def get_user_products(*,
                      user_id: int,
                      skip: int = 0,
                      limit: int = 5,
                      db: Session = Depends(database.get_db)):
    return product_repo.get_multi_by_user(db, user_id=user_id, skip=skip, limit=limit)


@router.put("/{id}")
def update_product(*, id: int,
                   product_in: ProductUpdate,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    return product_repo.update(db, db_obj=db_obj, obj_in=product_in)


@router.get("/{id}", response_model=ProductInDB)
def get_product(*, id: int, db: Session = Depends(database.get_db)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    return db_obj


@router.delete("/{id}")
def delete_product(*, id: int, db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    return product_repo.remove(db, id=id)


@router.post("/{id}/categories")
def add_category(*, id: int, c_id: int = Body(...),
                 db: Session = Depends(database.get_db),
                 current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    category = category_repo.get(db, id=c_id)
    return product_repo.add_category(db, db_obj=db_obj, category=category)


@router.delete("/{id}/categories/{c_id}")
def remove_categories(*, id: int, c_id: int, db: Session = Depends(database.get_db),
                      current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise PRODUCT_NOT_FOUND_EXCEPTION
    category = category_repo.get(db, id=c_id)
    return product_repo.remove_category(db, db_obj=db_obj, category=category)
