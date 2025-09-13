from business.bto.user_bto import UserBTO


class UserUtils:
    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email

    @staticmethod
    def format_phone_number(phone: str) -> str:
        return phone.replace("-", "").replace(" ", "")

    def register_user(self, user_bto: UserBTO) -> UserBTO:
        if not UserUtils.validate_email(user_bto.email):
            raise ValueError("Invalid email format")
        if self.bao_service.get_user_by_email(user_bto.email):
            raise ValueError("User with this email already exists.")
        return self.bao_service.create_user(user_bto)


