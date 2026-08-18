from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(db: Session, id: int) -> User | None:
        return db.query(User).filter_by(id=id).first()

    @staticmethod
    def get_user_by_role(db: Session, role: str) -> User | None:
        return db.query(User).filter_by(role=role).first()

    @staticmethod
    def has_unique_name(db: Session, username: str) -> User | None:
        return db.query(User).filter_by(username=username).all()

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str) -> User:
        user = User(
            username=username,
            password=password,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
