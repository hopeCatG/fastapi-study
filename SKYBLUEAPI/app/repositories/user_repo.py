from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from .base_repo import CRUDBase

class UserRepository(CRUDBase[User, UserCreate, UserUpdate]):
    # Add any model-specific methods here
    pass

# Instantiate the repository
user_repo = UserRepository(User)