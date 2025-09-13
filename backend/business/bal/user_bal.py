from business.bao.services.user_bao_service import UserBAOService
from business.bto.user_bto import UserBTO


class UserBAL:
    def __init__(self, bao_service: UserBAOService):
        self.bao_service = bao_service

    # Getters
    def get_user_details(self, user_email: str) -> UserBTO:
        return self.bao_service.get_user_by_email(user_email)

    def get_user_by_id(self, user_id: int) -> UserBTO:
        return self.bao_service.get_user_by_id(user_id)

    def get_user_by_password(self, password: str) -> UserBTO:
        return self.bao_service.get_user_by_password(password)

    def get_user_by_first_name(self, first_name: str) -> UserBTO:
        return self.bao_service.get_user_by_first_name(first_name)

    def get_user_by_last_name(self, last_name: str) -> UserBTO:
        return self.bao_service.get_user_by_last_name(last_name)

    def get_user_by_email_and_password(self, email: str, password: str) -> UserBTO:
        return self.bao_service.get_user_by_email_and_password(email, password)



    # Get all users
    def get_all_users(self) -> list[UserBTO]:
        return self.bao_service.get_all_users()


    # Create & Delete
    def register_user(self, user_bto: UserBTO) -> UserBTO:
        return self.bao_service.create_user(user_bto)

    def delete_user(self, email: str) -> None:
        self.bao_service.delete_user(email)


    # Updates
    def update_user_password(self, email: str, current_password: str, new_password: str) -> None:
        self.bao_service.update_user_password(email, current_password, new_password)

    def update_user_first_name(self, email: str, current_first_name: str, new_first_name: str) -> None:
        self.bao_service.update_user_first_name(email, current_first_name, new_first_name)

    def update_user_last_name(self, email: str, current_last_name: str, new_last_name: str) -> None:
        self.bao_service.update_user_last_name(email, current_last_name, new_last_name)

    def update_user_phone(self, email: str, current_phone: str, new_phone: str) -> None:
        self.bao_service.update_user_phone(email, current_phone, new_phone)

    def update_user_gender(self, email: str, current_gender: str, new_gender: str) -> None:
        self.bao_service.update_user_gender(email, current_gender, new_gender)

    def update_user_country(self, email: str, current_country: str, new_country: str) -> None:
        self.bao_service.update_user_country(email, current_country, new_country)

    def update_user(self, user_id: int, user_bto: UserBTO) -> UserBTO:
        return self.bao_service.update_user(user_id, user_bto)


    def verify_user_by_email(self, email: str) -> None:
        self.bao_service.verify_user_by_email(email)

    def reset_user_password(self, email: str, new_password: str) -> None:
        self.bao_service.reset_user_password(email, new_password)