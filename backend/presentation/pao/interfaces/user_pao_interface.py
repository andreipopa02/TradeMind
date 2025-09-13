from typing import Dict
from business.bto.user_bto import UserBTO

class UserPAOInterface:
    def request_to_bto(self, user_data: Dict) -> UserBTO:
        pass

    def bto_to_response(self, user_bto: UserBTO) -> Dict:
        pass


    # Getters
    def get_user_details(self, user_id: int) -> dict:
      pass

    def get_user_by_password(self, password: str) -> dict:
        pass


    # Get all users
    def get_all_users(self) -> list[dict]:
        pass


    # Create & Delete
    def register_user(self, user_data: dict) -> dict:
        pass

    def delete_user(self, email: str) -> None:
        pass


    # Updates
    def update_user_details(self, user_id: int, updated_data: dict) -> dict:
        pass

    def update_password(self, email: str, current_password: str, new_password: str) -> None:
        pass

    def login_user(self, user_data: dict) -> dict:
        pass

    def verify_user_email_by_token(self, token: str) -> dict:
        pass

    def forgot_password(self, email: str) -> None:
        pass

    def reset_password(self, token: str, new_password: str) -> None:
        pass

