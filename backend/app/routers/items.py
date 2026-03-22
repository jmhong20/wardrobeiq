import json
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.item import CategoryEnum
from ..models.user import User
from ..schemas.item import ClothingItemRead, ClothingItemUpdate
from ..services import items as svc

router = APIRouter(prefix="/items", tags=["items"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[ClothingItemRead])
def list_items(
    current_user: CurrentUser,
    db: DB,
    category: CategoryEnum | None = Query(default=None),
    include_inactive: bool = Query(default=False),
):
    return svc.get_items(db, current_user.id, category=category, active_only=not include_inactive)


@router.post("/", response_model=ClothingItemRead, status_code=201)
async def create_item(
    current_user: CurrentUser,
    db: DB,
    name: str = Form(...),
    category: CategoryEnum = Form(...),
    favorability: int = Form(default=3),
    # Tags sent as JSON strings e.g. '["casual","streetwear"]'
    style_tags: str = Form(default="[]"),
    color_tags: str = Form(default="[]"),
    season_tags: str = Form(default="[]"),
    image: UploadFile | None = File(default=None),
):
    from ..schemas.item import ClothingItemCreate

    payload = ClothingItemCreate(
        name=name,
        category=category,
        favorability=favorability,
        style_tags=json.loads(style_tags),
        color_tags=json.loads(color_tags),
        season_tags=json.loads(season_tags),
    )
    return svc.create_item(db, current_user.id, payload, image=image)


@router.get("/{item_id}", response_model=ClothingItemRead)
def get_item(item_id: int, current_user: CurrentUser, db: DB):
    return svc.get_item(db, current_user.id, item_id)


@router.patch("/{item_id}", response_model=ClothingItemRead)
def update_item(item_id: int, payload: ClothingItemUpdate, current_user: CurrentUser, db: DB):
    return svc.update_item(db, current_user.id, item_id, payload)


@router.post("/{item_id}/image", response_model=ClothingItemRead)
async def upload_image(
    item_id: int,
    current_user: CurrentUser,
    db: DB,
    image: UploadFile = File(...),
):
    return svc.upload_item_image(db, current_user.id, item_id, image)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, current_user: CurrentUser, db: DB):
    svc.delete_item(db, current_user.id, item_id)
