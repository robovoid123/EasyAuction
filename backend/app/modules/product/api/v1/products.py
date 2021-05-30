from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

from app.dependencies import database, auth

from app.modules.user.models import User
from app.modules.product.schemas import (ProductCreate, ProductUpdate)
from app.modules.product.repositories import product_repo, category_repo

router = APIRouter()


@router.post("/", status_code=201)
def create_product(*,
                   product_in: ProductCreate,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    return product_repo.create(db, obj_in=product_in)


@router.get("/")
def get_products(*,
                 skip: int = 0,
                 limit: int = 5,
                 db: Session = Depends(database.get_db)):
    return product_repo.get_multi(db, skip=skip, limit=limit)


@router.put("/{id}")
def update_product(*, id: int,
                   product_in: ProductUpdate,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="product not found")
    return product_repo.update(db, db_obj=db_obj, obj_in=product_in)


@router.get("/{id}")
def get_product(*, id: int, db: Session = Depends(database.get_db)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="product not found")
    return db_obj


@router.delete("/{id}")
def delete_product(*, id: int, db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="product not found")
    return product_repo.remove(db, id=id)


@router.post("/{id}/categories")
def add_category(*, id: int, c_id: int = Body(...),
                 db: Session = Depends(database.get_db),
                 current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="product not found")
    category = category_repo.get(db, id=c_id)
    return product_repo.add_category(db, db_obj=db_obj, category=category)


@router.delete("/{id}/categories/{c_id}")
def remove_categories(*, id: int, c_id: int, db: Session = Depends(database.get_db),
                      current_user: User = Depends(auth.get_current_active_user)):
    db_obj = product_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="product not found")
    category = category_repo.get(db, id=c_id)
    return product_repo.remove_category(db, db_obj=db_obj, category=category)
