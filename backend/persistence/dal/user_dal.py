from typing import List

from sqlalchemy.orm import Session
from persistence.dao.repositories.user_repository import UserRepository
from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.dto.user_dto import UserDTO


class UserDAL:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # Getters
    def get_user_by_id(self, user_id: int) -> UserDTO:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> UserDTO:
        return self.user_repository.get_user_by_email(email)

    def get_user_by_first_name(self, first_name: str) -> UserDTO:
        return self.user_repository.get_user_by_fist_name(first_name)

    def get_user_by_last_name(self, last_name: str) -> UserDTO:
        return self.user_repository.get_user_by_last_name(last_name)

    def get_user_by_password(self, password: str) -> UserDTO:
        return self.user_repository.get_user_by_password(password)

    def get_user_by_email_and_password(self, email: str, password: str) -> UserDTO:
        return self.user_repository.get_user_by_email_and_password(email, password)


    # Get all users
    def get_all_users(self) -> list[UserDTO]:
        return self.user_repository.get_all_users()


    # Create & Delete
    def create_user(self, user_dto: UserDTO) -> UserDTO:
        return self.user_repository.create_user(user_dto)

    def delete_user(self, email: str) -> None:
        self.user_repository.delete_user(email)


    # Updates
    def update_user_first_name(self, email: str, first_name: str) -> UserDTO:
        return self.user_repository.update_user_first_name(email, first_name)

    def update_user_last_name(self, email: str, last_name: str) -> UserDTO:
        return self.user_repository.update_user_last_name(email, last_name)

    def update_user_password(self, email: str, new_password: str) -> None:
        self.user_repository.update_user_password(email, new_password)

    def update_user_phone(self, email: str, phone: str) -> UserDTO:
        return self.user_repository.update_user_phone(email, phone)

    def update_user_gender(self, email: str, gender: str) -> UserDTO:
        return self.user_repository.update_user_gender(email, gender)

    def update_user_country(self, email: str, country: str) -> UserDTO:
        return self.user_repository.update_user_country(email, country)


    def validate_current_password_by_email(self, email: str, current_password: str) -> bool:
        return self.user_repository.validate_current_password_by_email(email, current_password)

    def verify_user_by_email(self, email: str) -> None:
        self.user_repository.verify_user_by_email(email)
