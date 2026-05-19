from app.models.box_user_model import BoxUser
from app.schemas.user_schema import UserCreate, UserUpdate
from .base_repo import CRUDBase


class UserRepository(CRUDBase[BoxUser, UserCreate, UserUpdate]):
    pass


user_repo = UserRepository(BoxUser)
