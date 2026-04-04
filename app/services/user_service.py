from app.repositories.user import UserRepository
from app.utilities.security import encrypt_password, verify_password, create_access_token
from app.schemas.user import RegularUserCreate
from typing import Optional

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_all_users(self):
        return self.user_repo.get_all_users()
    
    def delete_user(self, current_user, user_id: int):
        if current_user.role != "admin":
            raise Exception("Unauthorized")

        return self.user_repo.delete(user_id)