from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from api import models
from api.crud import auth as crud_auth
from api.crud import categories as crud_categories
from api.database import get_db
from api.schemas import categories as schemas_categories

router = APIRouter()


@router.get("", response_model=Page[schemas_categories.Category])
def read_categories(db: Session = Depends(get_db)):
    return paginate(crud_categories.get_categories(db=db))


@router.post("", response_model=schemas_categories.Category)
def create_category(
    category: schemas_categories.CategoryCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(crud_auth.get_current_active_user),
):
    return crud_categories.create_category(db=db, category=category, user=user)


@router.delete("")
def remove_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    user: models.User = Depends(crud_auth.get_current_active_user),
):
    return crud_categories.remove_category(db=db, category_id=category_id, user=user)
