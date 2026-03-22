from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.wear_log import WearLogCreate, WearLogRead
from ..services import wear_logs as svc

router = APIRouter(prefix="/wear-logs", tags=["wear-logs"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=WearLogRead, status_code=201)
def log_wear(payload: WearLogCreate, current_user: CurrentUser, db: DB):
    return svc.log_wear(db, current_user.id, payload)


@router.get("/", response_model=list[WearLogRead])
def wear_history(current_user: CurrentUser, db: DB, limit: int = 50):
    return svc.get_wear_history(db, current_user.id, limit=limit)
