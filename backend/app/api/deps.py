from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import decode_access_token
from app.core.exceptions import AppCustomException
from app.models.user import User

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Extract and authenticate user from Authorization: Bearer <token>."""
    if not authorization or not authorization.startswith("Bearer "):
        raise AppCustomException(
            status_code=401,
            code="MISSING_TOKEN",
            message="Authentication token is required."
        )

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise AppCustomException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid or expired authentication token."
        )

    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppCustomException(
            status_code=401,
            code="USER_NOT_FOUND",
            message="User associated with token no longer exists."
        )

    return user

def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Authorize only users with role 'admin'."""
    if current_user.role != "admin":
        raise AppCustomException(
            status_code=403,
            code="ADMIN_REQUIRED",
            message="Administrator privileges are required to perform this action."
        )
    return current_user
