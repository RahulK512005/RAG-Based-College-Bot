from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.auth import UserSignup, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import auth_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse)
def signup(data: UserSignup, db: Session = Depends(get_db)):
    """Register a new student user."""
    return auth_service.signup(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and issue JWT."""
    return auth_service.login(db, data)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logout current user session."""
    return {"success": True, "message": "Successfully logged out."}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Fetch current user profile and role details."""
    return current_user
