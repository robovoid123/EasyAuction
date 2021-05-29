from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import database, auth

from app.modules.user.models import User
from app.modules.product.schemas import (CategoryCreate, CategoryUpdate)
from app.modules.product.repositories import category_repo

router = APIRouter()


@router.post("/")
def create_category(*,
                    category_in: CategoryCreate,
                    db: Session = Depends(database.get_db),
                    current_user: User = Depends(auth.get_current_active_superuser)):
    return category_repo.create(db, obj_in=category_in)


@router.get("/")
def get_categories(*,
                   skip: int = 0,
                   limit: int = 5,
                   db: Session = Depends(database.get_db)):
    return category_repo.get_multi(db, skip=skip, limit=limit)


@router.put("/{id}")
def update_category(*, id: int,
                    category_in: CategoryUpdate,
                    db: Session = Depends(database.get_db),
                    current_user: User = Depends(auth.get_current_active_superuser)):
    db_obj = category_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="category not found")
    return category_repo.update(db, db_obj=db_obj, obj_in=category_in)


@router.get("/{id}")
def get_category(*, id: int, db: Session = Depends(database.get_db)):
    db_obj = category_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="category not found")
    return db_obj


@router.delete("/{id}")
def delete_category(*, id: int, db: Session = Depends(database.get_db),
                    current_user: User = Depends(auth.get_current_active_superuser)):
    db_obj = category_repo.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404,
                            detail="category not found")
    return category_repo.remove(db, id=id)
