from typing import Optional
import re

from business.bto.user_bto import UserBTO
from business.bao.interfaces.user_bao_interface import UserBAOInterface
from business.mappers.user_mapper import UserMapper
from persistence.dal.user_dal import UserDAL
from persistence.utils.data_validators import validate_password_strength, validate_email_format, validate_phone, \
    validate_gender


class UserBAOService(UserBAOInterface):
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal

    # Getters
    def get_user_by_id(self, user_id: int) -> Optional[UserBTO]:
        user_dto = self.user_dal.get_user_by_id(user_id)
        return UserMapper.dto_to_bto(user_dto) if user_dto else None

    def get_user_by_email(self, email: str) -> Optional[UserBTO]:
        user_dto = self.user_dal.get_user_by_email(email)
        return UserMapper.dto_to_bto(user_dto) if user_dto else None

    def get_user_by_first_name(self, first_name: str) -> Optional[UserBTO]:
        user_dto = self.user_dal.get_user_by_first_name(first_name)
        return UserMapper.dto_to_bto(user_dto) if user_dto else None

    def get_user_by_last_name(self, last_name: str) -> Optional[UserBTO]:
        user_dto = self.user_dal.get_user_by_last_name(last_name)
        return UserMapper.dto_to_bto(user_dto) if user_dto else None

    def get_user_by_password(self, password: str) -> Optional[UserBTO]:
        user_dto = self.user_dal.get_user_by_password(password)
        return UserMapper.dto_to_bto(user_dto) if user_dto else None

    def get_user_by_email_and_password(self, email: str, password: str) -> UserBTO:
        user_dto = self.user_dal.get_user_by_email(email)
        if not user_dto:
            raise ValueError("User not found")
        if not self.user_dal.validate_current_password_by_email(email, password):
            raise ValueError("Incorrect password")
        return UserMapper.dto_to_bto(user_dto)


    # Get all users
    def get_all_users(self) -> list[UserBTO]:
        users_dto = self.user_dal.get_all_users()
        return [UserMapper.dto_to_bto(user) for user in users_dto]


    # Create & delete
    def create_user(self, user_bto: UserBTO) -> UserBTO:
        if self.get_user_by_email(user_bto.email):
            raise ValueError("User with this email already exists.")

        validate_password_strength(user_bto.password)
        validate_email_format(user_bto.email)
        validate_phone(user_bto.phone)
        validate_gender(user_bto.gender)

        user_dto = UserMapper.bto_to_dto(user_bto)
        created_user_dto = self.user_dal.create_user(user_dto)
        return UserMapper.dto_to_bto(created_user_dto)

    def delete_user(self, email: str) -> None:
        if not self.get_user_by_email(email):
            raise ValueError("User doesn't exist.")
        self.user_dal.delete_user(email)


    # Updates
    def update_user_first_name(self, email: str, current_first_name: str, new_first_name: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        if user.first_name != current_first_name:
            raise ValueError("Current first name does not match")
        self.user_dal.update_user_first_name(email, new_first_name)

    def update_user_last_name(self, email: str, current_last_name: str, new_last_name: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        if user.last_name != current_last_name:
            raise ValueError("Current last name does not match")
        self.user_dal.update_user_last_name(email, new_last_name)

    def update_user_password(self, email: str, current_password: str, new_password: str) -> None:
        if not self.user_dal.validate_current_password_by_email(email, current_password):
            raise ValueError("Current password is incorrect")

        if len(new_password) < 8:
            raise ValueError("New password must be at least 8 characters long")

        validate_password_strength(new_password)
        self.user_dal.update_user_password(email, new_password)

    def update_user_phone(self, email: str, current_phone: str, new_phone: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        validate_phone(new_phone)

        if not user:
            raise ValueError("User not found")
        if user.phone != current_phone:
            raise ValueError("Current phone number does not match")
        self.user_dal.update_user_phone(email, new_phone)

    def update_user_gender(self, email: str, current_gender: str, new_gender: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        validate_gender(new_gender)

        if not user:
            raise ValueError("User not found")
        if user.gender != current_gender:
            raise ValueError("Current gender does not match")
        self.user_dal.update_user_gender(email, new_gender)

    def update_user_country(self, email: str, current_country: str, new_country: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        if user.country != current_country:
            raise ValueError("Current country does not match")
        self.user_dal.update_user_country(email, new_country)

    def update_user(self, user_id: int, user_bto: UserBTO) -> UserBTO:
        user = self.user_dal.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user.first_name != user_bto.first_name:
            self.update_user_first_name(user.email, user.first_name, user_bto.first_name)

        if user.last_name != user_bto.last_name:
            self.update_user_last_name(user.email, user.last_name, user_bto.last_name)

        if user.phone != user_bto.phone:
            self.update_user_phone(user.email, user.phone, user_bto.phone)

        if user.gender != user_bto.gender:
            self.update_user_gender(user.email, user.gender, user_bto.gender)

        if user.country != user_bto.country:
            self.update_user_country(user.email, user.country, user_bto.country)

        updated_user = self.user_dal.get_user_by_id(user_id)

        return UserBTO(
            id=updated_user.id,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            email=updated_user.email,
            password=user.password,
            phone=updated_user.phone,
            gender=updated_user.gender,
            country=updated_user.country,
            is_verified=True
        )

    def verify_user_by_email(self, email: str) -> None:
        self.user_dal.verify_user_by_email(email)

    def reset_user_password(self, email: str, new_password: str) -> None:
        validate_password_strength(new_password)
        self.user_dal.update_user_password(email, new_password)