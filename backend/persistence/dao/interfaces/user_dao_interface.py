from typing import List

from persistence.dto.trading_account_dto import TradingAccountDTO
from persistence.dto.user_dto import UserDTO

class UserDAOInterface:

    # Getters
    def get_user_by_id(self, user_id: int) -> UserDTO:
        pass

    def get_user_by_fist_name(self, first_name: str) -> UserDTO:
        pass

    def get_user_by_last_name(self, last_name: str) -> UserDTO:
        pass

    def get_user_by_email(self, email: str) -> UserDTO:
        pass

    def get_user_by_password(self, password: str) -> UserDTO:
        pass

    def get_user_by_email_and_password(self, email: str, password: str):
        pass


    # Create & delete
    def create_user(self, user_dto: UserDTO) -> UserDTO:
        pass

    def delete_user(self, email: str) -> None:
        pass


    # Setters
    def update_user_first_name(self, email: str, first_name: str) -> UserDTO:
        pass

    def update_user_last_name(self, email: str, last_name: str) -> UserDTO:
        pass

    def update_user_password(self, email: str, password: str) -> UserDTO:
        pass

    def update_user_phone(self, email: str, phone: str) -> UserDTO:
        pass

    def update_user_gender(self, email: str, phone: str) -> UserDTO:
        pass

    def update_user_country(self, email: str, country: str) -> UserDTO:
        pass


    # Getters - multiple rows
    def get_all_users(self) -> List[UserDTO]:
        pass

    def verify_user_by_email(self, email: str) -> None:
        pass
