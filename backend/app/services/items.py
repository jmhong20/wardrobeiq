import os
import uuid

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps
from sqlalchemy.orm import Session

from ..core.config import get_settings
from ..models.item import ClothingItem, CategoryEnum
from ..schemas.item import ClothingItemCreate, ClothingItemUpdate

settings = get_settings()


def _save_image(file: UploadFile, user_id: int) -> str:
    user_dir = os.path.join(settings.UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    dest = os.path.join(user_dir, filename)

    img = Image.open(file.file)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    img.thumbnail((settings.MAX_IMAGE_SIZE_PX, settings.MAX_IMAGE_SIZE_PX))
    img.save(dest, "JPEG", quality=85)

    return f"/uploads/{user_id}/{filename}"


def get_items(db: Session, user_id: int, category: str | None = None, active_only: bool = True):
    q = db.query(ClothingItem).filter(ClothingItem.user_id == user_id)
    if active_only:
        q = q.filter(ClothingItem.active == True)
    if category:
        q = q.filter(ClothingItem.category == category)
    return q.order_by(ClothingItem.created_at.desc()).all()


def get_item(db: Session, user_id: int, item_id: int) -> ClothingItem:
    item = db.query(ClothingItem).filter(
        ClothingItem.id == item_id,
        ClothingItem.user_id == user_id,
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
    return item


def create_item(
    db: Session,
    user_id: int,
    payload: ClothingItemCreate,
    image: UploadFile | None = None,
) -> ClothingItem:
    image_path = _save_image(image, user_id) if image else None
    item = ClothingItem(
        user_id=user_id,
        image_path=image_path,
        **payload.model_dump(),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, user_id: int, item_id: int, payload: ClothingItemUpdate) -> ClothingItem:
    item = get_item(db, user_id, item_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def upload_item_image(db: Session, user_id: int, item_id: int, image: UploadFile) -> ClothingItem:
    item = get_item(db, user_id, item_id)
    item.image_path = _save_image(image, user_id)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, user_id: int, item_id: int) -> None:
    item = get_item(db, user_id, item_id)
    item.active = False
    db.commit()
