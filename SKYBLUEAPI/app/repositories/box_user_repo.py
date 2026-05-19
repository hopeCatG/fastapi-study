from app.models.box_user_model import BoxUser
from app.schemas.box_user_schema import BoxUserCreate, BoxUserUpdate
from .base_repo import CRUDBase


class BoxUserRepository(CRUDBase[BoxUser, BoxUserCreate, BoxUserUpdate]):
    pass


box_user_repo = BoxUserRepository(BoxUser)

