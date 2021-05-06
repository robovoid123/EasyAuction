from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.api.dependencies import database, auth

from app.models.user import User
from app.crud.product import product
from app.schemas.product import (ProductRequest,
                                 ProductResponse,
                                 ProductCreate,
                                 ProductUpdate)

router = APIRouter()


@router.get("/{id}", response_model=ProductResponse)
def get_product(
        id,
        *,
        db: Session = Depends(database.get_db)):

    product_o = product.get(db=db, id=id)
    if not product_o:
        raise HTTPException(status_code=404,
                            detail="product does not exist")
    return product_o


@router.put("/{id}", response_model=ProductResponse)
def update_product(
        id,
        *,
        product_in: ProductRequest,
        db: Session = Depends(database.get_db),
        current_user: User = Depends(auth.get_current_active_user)):

    old_product = product.get(db=db, id=id)
    if not old_product:
        raise HTTPException(status_code=404,
                            detail="product does not exist")

    if old_product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="only owner can update")

    if product_in.quantity is not None:
        product.update_inventory(db=db,
                                 product_db=old_product,
                                 quantity=product_in.quantity,
                                 )

    if product_in.categories:
        product.add_categories(db=db,
                               categories=product_in.categories,
                               product_id=old_product.id)

    product_obj = ProductUpdate(**jsonable_encoder(product_in))
    updated_product = product.update(db=db,
                                     db_obj=old_product,
                                     obj_in=product_obj)

    return updated_product


@router.post("/", response_model=ProductResponse)
def create_product(
        *,
        product_in: ProductRequest,
        db: Session = Depends(database.get_db),
        current_user: User = Depends(auth.get_current_active_user)):
    new_inventory = product.create_inventory(db=db,
                                             quantity=product_in.quantity)
    product_obj = ProductCreate(**jsonable_encoder(product_in),
                                inventory_id=new_inventory.id,
                                owner_id=current_user.id)
    new_product = product.create(db=db,
                                 obj_in=product_obj)
    product.add_categories(db=db,
                           categories=product_in.categories,
                           product_id=new_product.id)

    return new_product


@router.get("/")
def get_products(
        *,
        skip=0,
        limit=5,
        db: Session = Depends(database.get_db)):
    return product.get_multi(db=db, skip=skip, limit=limit)