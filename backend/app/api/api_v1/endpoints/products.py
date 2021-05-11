from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.api.dependencies import database, auth

from app.models.user import User
from app.schemas.product import (ProductRequest,
                                 ProductResponse,
                                 ProductCreate,
                                 ProductUpdate)

from app.easy_auction.product.product_manager import product_manager

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create_product(*,
                   product_in: ProductRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product_obj = ProductCreate(
        **jsonable_encoder(product_in),
        owner_id=current_user.id)

    # TODO: after implementing property ommit .get()
    return product_manager.create_product(db, product_obj,
                                          quantity=product_in.quantity,
                                          categories=product_in.categories).get()


@router.get("/")
def get_products(*,
                 skip=0,
                 limit=5,
                 db: Session = Depends(database.get_db)):

    return product_manager.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductResponse)
def get_product(id,
                *,
                db: Session = Depends(database.get_db)):

    product = product_manager.get_product(db, id)

    if not product:

        raise HTTPException(
            status_code=404,
            detail="product does not exist")

    return product.get()


@router.put("/{id}", response_model=ProductResponse)
def update_product(id,
                   *,
                   product_in: ProductRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product = product_manager.get_product(db, id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="product does not exist")

    if product.owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only owner can update")

    update_obj = ProductUpdate(**jsonable_encoder(product_in))

    if product_in.quantity:
        product.update_inventory(product_in.quantity)
    if product_in.categories:
        product.update_categories(product_in.categories)

    return product.update(update_obj)
