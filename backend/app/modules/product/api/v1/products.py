from app.modules.product.schemas.product import ProductInDB
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies import database, auth

from app.modules.user.models import User
from app.modules.product.schemas import (ProductCreate, ProductCreateRequest, ProductMultiResponse, ProductResponse, ProductUpdate,
                                         ProductUpdateRequest, Product)

from app.modules.product.repositories import product_repo

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create_product(*,
                   product_in: ProductCreateRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product_obj = ProductCreate(**product_in.dict(exclude_unset=True))

    return product_repo.create_complete(db, product_obj, owner_id=current_user.id,
                                        quantity=product_in.quantity, categories=product_in.categories)


@router.get("/", response_model=List[ProductMultiResponse])
def get_products(*,
                 skip=0,
                 limit=5,
                 db: Session = Depends(database.get_db)):

    return product_repo.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductResponse)
def get_product(id,
                *,
                db: Session = Depends(database.get_db)):

    db_obj = product_repo.get(db, id)

    if not db_obj:

        raise HTTPException(
            status_code=404,
            detail="product does not exist")
    return db_obj


@router.put("/{id}", response_model=ProductResponse)
def update_product(id,
                   *,
                   product_in: ProductUpdateRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    db_obj = product_repo.get(db, id)

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="product does not exist")

    if db_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only owner can update")

    product_obj = ProductUpdate(**product_in.dict(exclude_unset=True))
    return product_repo.update_complete(
        db, db_obj, product_obj, quantity=product_in.quantity)


# @router.delete("/{id}", response_model=ProductResponse)
# def delete_product(
#         id,
#         db: Session = Depends(database.get_db),
#         current_user: User = Depends(auth.get_current_active_user)):
#     product = Product(db)
#     db_obj = product.get(id)

#     if not db_obj:
#         raise HTTPException(
#             status_code=404,
#             detail="product does not exist")

#     if db_obj.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="only owner can delete")

#     return product.remove(id)
