from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import database, auth

from app.models.user import User
from app.schemas.product import (ProductCreateRequest, ProductInDB,
                                 ProductUpdateRequest)

from app.easy_auction.product.product import Product

router = APIRouter()


@router.post("/", response_model=ProductInDB)
def create_product(*,
                   product_in: ProductCreateRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product = Product(db)
    db_obj = product.create({**product_in.dict(), 'owner_id': current_user.id})

    return db_obj


@router.get("/")
def get_products(*,
                 skip=0,
                 limit=5,
                 db: Session = Depends(database.get_db)):

    product = Product(db)
    return product.get_multi(skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductInDB)
def get_product(id,
                *,
                db: Session = Depends(database.get_db)):

    product = Product(db)
    db_obj = product.get(id)

    if not db_obj:

        raise HTTPException(
            status_code=404,
            detail="product does not exist")

    return db_obj


@router.put("/{id}", response_model=ProductInDB)
def update_product(id,
                   *,
                   product_in: ProductUpdateRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product = Product(db)
    db_obj = product.get(id)

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="product does not exist")

    if db_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only owner can update")

    db_obj = product.update(db_obj, product_in)
    return db_obj


# @router.delete("/{id}")
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
