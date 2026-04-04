from app.repositories.user import UserRepository
from app.utilities.security import encrypt_password, verify_password, create_access_token
from app.schemas.user import RegularUserCreate
from typing import Optional

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        user = self.user_repo.get_by_username(username)

        if not user:
            return None

        if not verify_password(
            plaintext_password=password,
            encrypted_password=user.password
        ):
            return None

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        return access_token

    def register_user(self, username: str, email: str, password: str):
        existing_user = self.user_repo.get_by_username(username)
        if existing_user:
            raise Exception("Username already exists")
        
        hashed_password = encrypt_password(password)

        new_user = RegularUserCreate(
            username=username,
            email=email,
            password=hashed_password
        )

        return self.user_repo.create(new_user)
