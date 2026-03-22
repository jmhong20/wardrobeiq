import csv
import io
import json
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..services import stats as svc

router = APIRouter(prefix="/stats", tags=["stats"])

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


@router.get("/summary")
def summary(current_user: CurrentUser, db: DB):
    return svc.get_summary(db, current_user.id)


@router.get("/by-category")
def by_category(current_user: CurrentUser, db: DB):
    return svc.get_by_category(db, current_user.id)


@router.get("/by-style")
def by_style(current_user: CurrentUser, db: DB):
    return svc.get_style_breakdown(db, current_user.id)


@router.get("/never-worn")
def never_worn(current_user: CurrentUser, db: DB):
    return svc.get_never_worn(db, current_user.id)


@router.get("/most-worn")
def most_worn(current_user: CurrentUser, db: DB, limit: int = Query(default=5, le=20)):
    return svc.get_most_worn(db, current_user.id, limit=limit)


@router.get("/gaps")
def wardrobe_gaps(current_user: CurrentUser, db: DB):
    return svc.get_wardrobe_gaps(db, current_user.id)


@router.get("/wear-calendar")
def wear_calendar(current_user: CurrentUser, db: DB, days: int = Query(default=90, le=365)):
    return svc.get_wear_calendar(db, current_user.id, days=days)


@router.get("/export")
def export(
    current_user: CurrentUser,
    db: DB,
    format: str = Query(default="json", pattern="^(json|csv)$"),
):
    data = svc.export_wardrobe(db, current_user.id)

    if format == "csv":
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=wardrobe.csv"},
        )

    json_bytes = io.BytesIO(json.dumps(data, indent=2).encode())
    return StreamingResponse(
        json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=wardrobe.json"},
    )
