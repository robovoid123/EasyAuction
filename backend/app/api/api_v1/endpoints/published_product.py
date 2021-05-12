from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.easy_auction import market
from app.schemas.market import (
    PublishedProductCreate,
    PublishedProductUpdate
)

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user


router = APIRouter()


@router.get('/')
def get_published_products(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    return market.get_published_products(db, skip=skip, limit=limit)


@router.post('/')
def publish_product(
        product_in: PublishedProductCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_active_user)):

    product = market.publish_product(db, obj_in=product_in)
    return product.get()


@router.put('/{id}')
def update_published_product(
        id: int,
        product_in: PublishedProductUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_active_user)):

    product = market.get_published_product(db, id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    if product.owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only product owner can do this action'
        )
    return product.update(obj_in=product_in)


@router.get('/{id}')
def get_published_product(
        id: int,
        db: Session = Depends(get_db)):

    product = market.get_published_product(db, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='product not found'
        )

    return product.get()


@router.delete('/{id}')
def unpublish_product(
        id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_active_user)):

    return market.unpublish_product(db, id)


@router.post('/{id}/buy')
def buy_product(
        id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_active_user)):

    product = market.get_published_product(db, id)
    return product.buy(quantity=1, buyer_id=current_user.id)
