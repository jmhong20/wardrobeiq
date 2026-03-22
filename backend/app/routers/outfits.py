from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.outfit import OutfitCreate, OutfitRead, OutfitUpdate
from ..services import outfits as svc

router = APIRouter(prefix="/outfits", tags=["outfits"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=list[OutfitRead])
def list_outfits(current_user: CurrentUser, db: DB, limit: int = 50):
    return svc.get_outfits(db, current_user.id, limit=limit)


@router.post("/", response_model=OutfitRead, status_code=201)
def create_outfit(payload: OutfitCreate, current_user: CurrentUser, db: DB):
    return svc.create_outfit(db, current_user.id, payload)


@router.get("/{outfit_id}", response_model=OutfitRead)
def get_outfit(outfit_id: int, current_user: CurrentUser, db: DB):
    return svc.get_outfit(db, current_user.id, outfit_id)


@router.patch("/{outfit_id}", response_model=OutfitRead)
def update_outfit(outfit_id: int, payload: OutfitUpdate, current_user: CurrentUser, db: DB):
    return svc.update_outfit(db, current_user.id, outfit_id, payload)


@router.post("/{outfit_id}/rate", response_model=OutfitRead)
def rate_outfit(outfit_id: int, rating: int, current_user: CurrentUser, db: DB):
    return svc.rate_outfit(db, current_user.id, outfit_id, rating)
