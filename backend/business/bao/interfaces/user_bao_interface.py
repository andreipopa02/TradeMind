from typing import Optional
from business.bto.user_bto import UserBTO

class UserBAOInterface:

    # Getters
    def get_user_by_id(self, user_id: int) -> Optional[UserBTO]:
        pass

    def get_user_by_email(self, email: str) -> Optional[UserBTO]:
        pass

    def get_user_by_first_name(self, first_name: str) -> Optional[UserBTO]:
        pass

    def get_user_by_last_name(self, last_name: str) -> Optional[UserBTO]:
        pass

    def get_user_by_password(self, password: str) -> Optional[UserBTO]:
        pass

    def get_user_by_email_and_password(self, email: str, password: str) -> Optional[UserBTO]:
        pass

    # Get all users
    def get_all_users(self) -> list[UserBTO]:
        pass


    # Create & delete
    def create_user(self, user_bto: UserBTO) -> UserBTO:
        pass

    def delete_user_by_email(self, email: str) -> None:
        pass


    # Updates
    def update_user_first_name(self, email: str, current_first_name: str, new_first_name: str) -> None:
        pass

    def update_user_last_name(self, email: str, current_last_name: str, new_first_name: str) -> None:
        pass

    def update_user_password(self, email: str, current_password: str, new_password: str) -> None:
        pass

    def update_user_phone(self, email: str, current_phone: str, new_phone: str) -> None:
        pass

    def update_user_gender(self, email: str, current_gender: str, new_gender: str) -> None:
        pass

    def update_user_country(self, email: str, current_country: str, new_country: str) -> None:
        pass

    def update_user(self, user_id: int, user_bto: UserBTO) -> UserBTO:
        pass


    def verify_user_by_email(self, email: str) -> None:
        pass

    def reset_user_password(self, email: str, new_password: str) -> None:
        pass
