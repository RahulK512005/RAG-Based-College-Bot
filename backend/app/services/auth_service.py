from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserSignup, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import AppCustomException

class AuthService:
    @staticmethod
    def signup(db: Session, data: UserSignup) -> dict:
        if data.password != data.confirm_password:
            raise AppCustomException(status_code=400, code="PASSWORD_MISMATCH", message="Passwords do not match.")

        # Check existing email
        existing = db.query(User).filter(User.email == data.email.lower()).first()
        if existing:
            raise AppCustomException(status_code=400, code="EMAIL_EXISTS", message="An account with this email already exists.")

        # Security requirement: Students cannot register as admin
        user = User(
            name=data.name.strip(),
            email=data.email.lower().strip(),
            password_hash=hash_password(data.password),
            role="student"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(subject=user.id, role=user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    @staticmethod
    def login(db: Session, data: UserLogin) -> dict:
        user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise AppCustomException(status_code=401, code="INVALID_CREDENTIALS", message="Invalid email or password.")

        token = create_access_token(subject=user.id, role=user.role)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AppCustomException(status_code=404, code="USER_NOT_FOUND", message="User not found.")
        return user

auth_service = AuthService()
