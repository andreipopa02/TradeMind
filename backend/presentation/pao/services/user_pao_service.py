from datetime import timedelta
from typing import Dict

from business.bal.user_bal import UserBAL
from business.bto.user_bto import UserBTO
from email_service.email_sender import send_email
from email_service.email_templates import verification_email_template, reset_password_email_template
from email_service.verification_token import verify_token_email, create_token_email, used_reset_tokens
from presentation.pao.interfaces.user_pao_interface import UserPAOInterface
from configurations.jws_authentification import create_access_token

class UserPAOService(UserPAOInterface):
    def __init__(self, user_bal: UserBAL):
        self.user_bal = user_bal

    def request_to_bto(self, user_data: Dict) -> UserBTO:
        if "email" not in user_data or "first_name" not in user_data:
            raise ValueError("Missing required fields: email or first_name")

        return UserBTO(
            id=None,
            first_name=user_data["first_name"],
            last_name=user_data.get("last_name", ""),
            email=user_data["email"],
            password=user_data.get("password"),
            phone=user_data.get("phone"),
            gender=user_data.get("gender"),
            country=user_data.get("country"),
            is_verified=user_data.get("is_verified", False)
        )

    def bto_to_response(self, user_bto: UserBTO) -> Dict:
        return {
            "id": user_bto.id,
            "first_name": user_bto.first_name,
            "last_name": user_bto.last_name,
            "email": user_bto.email,
            "password": user_bto.password,
            "phone": user_bto.phone,
            "gender": user_bto.gender,
            "country": user_bto.country,
            "is_verified": user_bto.is_verified
        }


    # Getters
    def get_user_details(self, user_id: int) -> dict:
        user_bto = self.user_bal.get_user_by_id(user_id)
        return self.bto_to_response(user_bto)

    def get_user_by_password(self, password: str) -> dict:
        user_bto = self.user_bal.get_user_by_password(password)
        return self.bto_to_response(user_bto)

    # Get all users
    def get_all_users(self) -> list[dict]:
        users_bto = self.user_bal.get_all_users()
        return [self.bto_to_response(user) for user in users_bto]

    # Create & Delete
    def register_user(self, user_data: dict) -> dict:
        user_bto = self.request_to_bto(user_data)
        created_user = self.user_bal.register_user(user_bto)

        token = create_token_email({
            "user_id": created_user.id,
            "email": created_user.email
        })

        verification_link = f"http://localhost:3000/verify-email?token={token}"
        html_content = verification_email_template(created_user.first_name, verification_link)
        send_email(created_user.email, "Verify your TradeMind account", html_content)

        return self.bto_to_response(created_user)

    def delete_user(self, email: str) -> None:
        self.user_bal.delete_user(email)


    def update_user_details(self, user_id: int, updated_data: dict) -> dict:
        user_bto = self.request_to_bto(updated_data)
        updated_user = self.user_bal.update_user(user_id, user_bto)
        return self.bto_to_response(updated_user)

    def update_password(self, email: str, current_password: str, new_password: str) -> None:
        self.user_bal.update_user_password(email, current_password, new_password)

    def login_user(self, user_data: dict) -> dict:
        email = user_data.get("email")
        password = user_data.get("password")
        if not email or not password:
            raise ValueError("Email and password are required.")

        authenticated_user = self.user_bal.get_user_by_email_and_password(email, password)

        if not authenticated_user.is_verified:
            raise ValueError("Email address not verified. Please check your inbox.")

        access_token = create_access_token(data={
            "sub": str(authenticated_user.email),
            "user_id": authenticated_user.id,
            "first_name": authenticated_user.first_name,
            "last_name": authenticated_user.last_name
        })

        return {
            "access_token": access_token,
            # "user": self.bto_to_response(authenticated_user)
        }

    def verify_user_email_by_token(self, token: str) -> dict:
        payload = verify_token_email(token)
        if not payload:
            raise ValueError("Invalid or expired token!")

        email = payload.get("email")
        if not email:
            raise ValueError("Email not found!")

        self.user_bal.verify_user_by_email(email)
        used_reset_tokens.add(token)
        return {"message": "Email confirmed!"}

    def forgot_password(self, email: str) -> None:
        user = self.user_bal.get_user_details(email)
        if not user:
            raise ValueError("User not found")

        token = create_token_email({
            "user_id": user.id,
            "email": user.email
        }, expires_delta=timedelta(minutes=30))

        reset_link = f"http://localhost:3000/reset-password?token={token}"
        html = reset_password_email_template(user.first_name, reset_link)
        send_email(user.email, "Reset your TradeMind password", html)

    def reset_password(self, token: str, new_password: str) -> None:
        payload = verify_token_email(token)
        if not payload:
            raise ValueError("Invalid or expired token!")

        email = payload.get("email")
        if not email:
            raise ValueError("Token does not contain email")

        self.user_bal.reset_user_password(email, new_password=new_password)
        used_reset_tokens.add(token)
