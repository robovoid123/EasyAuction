from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.dependencies import database, auth


from app.modules.user.models import User
from app.modules.product.schemas import (
    ProductCreate, ProductCreateRequest, ProductMultiResponse, ProductResponse, ProductUpdate)
from app.modules.product.repositories import product_repo
from app.modules.product.api.dependencies import get_current_product_owner, get_product
from app.modules.product.models.product import Product
from app.modules.product.models import service_type

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create_product(*,
                   product_in: ProductCreateRequest,
                   db: Session = Depends(database.get_db),
                   current_user: User = Depends(auth.get_current_active_user)):

    product_obj = ProductCreate(**product_in.dict(exclude_unset=True))

    db_obj = product_repo.create_with_owner(
        db, obj_in=product_obj, owner_id=current_user.id)
    if not product_in.quantity:
        quantity = 1
    else:
        quantity = product_in.quantity
        product_repo.create_inventory(db, db_obj=db_obj, quantity=quantity)
    if product_in.categories:
        product_repo.add_categories(
            db, db_obj=db_obj, category_ids=product_in.categories)
    return db_obj


@router.get("/", response_model=List[ProductMultiResponse])
def get_products(*,
                 skip=0,
                 limit=5,
                 db: Session = Depends(database.get_db)):

    return product_repo.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductResponse)
def get_single_product(db_obj: Product = Depends(get_product)):
    return db_obj


@router.put("/{id}", response_model=ProductResponse)
def update_product(*,
                   db_obj: Product = Depends(get_product),
                   product_in: ProductUpdate,
                   db: Session = Depends(database.get_db),
                   owner: User = Depends(get_current_product_owner)):

    return product_repo.update(db, db_obj=db_obj, obj_in=product_in)


@router.delete("/{id}", response_model=ProductResponse)
def delete_product(
        *,
        db_obj: Product = Depends(get_product),
        db: Session = Depends(database.get_db),
        owner: User = Depends(get_current_product_owner)):
    return product_repo.remove(db, id=db_obj.id)


@router.get("/{id}/reserves")
def get_reserves(*,
                 db_obj: Product = Depends(get_product),
                 db: Session = Depends(database.get_db),
                 owner: User = Depends(get_current_product_owner)):
    return product_repo.get_reserves(db, db_obj=db_obj)


@router.put("/{id}/inventory")
def update_inventory(*,
                     db_obj: Product = Depends(get_product),
                     quantity: int = Body(...),
                     db: Session = Depends(database.get_db),
                     owner: User = Depends(get_current_product_owner)):
    return product_repo.update_inventory(db, db_obj=db_obj, quantity=quantity)


@router.post("/{id}/categories")
def append_categories(*,
                      db_obj: Product = Depends(get_product),
                      categories: List[int] = Body(...),
                      db: Session = Depends(database.get_db),
                      owner: User = Depends(get_current_product_owner)):
    return product_repo.add_categories(db, db_obj=db_obj, category_ids=categories)


@router.delete("/{id}/categories")
def remove_categories(*,
                      db_obj: Product = Depends(get_product),
                      categories: List[int] = Body(...),
                      db: Session = Depends(database.get_db),
                      owner: User = Depends(get_current_product_owner)):
    return product_repo.remove_categories(db, db_obj=db_obj, category_ids=categories)


@router.post("/{id}/unreserve/")
def unreserve(*,
              db_obj: Product = Depends(get_product),
              service_type: service_type.ServiceType = Body(...),
              db: Session = Depends(database.get_db),
              owner: User = Depends(get_current_product_owner)):
    return product_repo.unreserve(db, db_obj=db_obj, service_type=service_type)
