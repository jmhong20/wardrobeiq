from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.user import UserCreate, UserRead, Token, LoginRequest
from ..services.auth import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """JSON login — used by the React frontend."""
    token = authenticate_user(db, payload.username, payload.password)
    return Token(access_token=token)


@router.post("/token", response_model=Token, include_in_schema=False)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 form login — used by the /docs Swagger UI."""
    token = authenticate_user(db, form.username, form.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
