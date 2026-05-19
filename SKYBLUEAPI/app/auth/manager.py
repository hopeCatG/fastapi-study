import os
import hashlib
import secrets
from typing import Optional, Tuple
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from dotenv import load_dotenv

from .database import get_user_db
from app.models.box_user_model import BoxUser

try:
    from fastapi_users.password import PasswordHelperProtocol
except ImportError:
    PasswordHelperProtocol = object

# Load environment variables from .env file
load_dotenv()

SECRET = os.environ.get("SECRET_KEY")
if SECRET is None:
    raise ValueError("SECRET_KEY environment variable not set")


class MD5PasswordHelper(PasswordHelperProtocol):
    def verify_and_update(self, plain_password: str, hashed_password: str) -> Tuple[bool, str]:
        calculated = hashlib.md5(plain_password.encode("utf-8")).hexdigest()
        return calculated == (hashed_password or ""), hashed_password

    def hash(self, password: str) -> str:
        return hashlib.md5(password.encode("utf-8")).hexdigest()

    def generate(self) -> str:
        return secrets.token_hex(16)


md5_password_helper = MD5PasswordHelper()


class UserManager(IntegerIDMixin, BaseUserManager[BoxUser, int]):
    """
    Manages user-related operations, like password hashing, token generation, etc.
    """
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: BoxUser, request: Optional[Request] = None):
        """
        Hook called after a user has successfully registered.
        This is a good place to send a welcome email.
        """
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: BoxUser, token: str, request: Optional[Request] = None
    ):
        """
        Hook called after a user has requested a password reset.
        This is where you would send the password reset email.
        """
        print(f"User {user.id} has forgotten their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: BoxUser, token: str, request: Optional[Request] = None
    ):
        """
        Hook called after a user has requested an email verification.
        This is where you would send the verification email.
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    FastAPI dependency that provides the UserManager instance.
    """
    try:
        yield UserManager(user_db, md5_password_helper)
    except TypeError:
        manager = UserManager(user_db)
        manager.password_helper = md5_password_helper
        yield manager
