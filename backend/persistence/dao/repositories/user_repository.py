import hashlib
from typing import List, Optional

from sqlalchemy.orm import Session
from persistence.dao.interfaces.user_dao_interface import UserDAOInterface
from persistence.dto.user_dto import UserDTO
from persistence.entities.user_entity import UserEntity
from persistence.mappers.user_mapper import UserMapper


class UserRepository(UserDAOInterface):
    def __init__(self, db: Session):
        self.db = db


    # Create & delete
    def create_user(self, user_dto: UserDTO) -> UserDTO:
        hashed_password = hashlib.sha256(user_dto.password.encode('utf-8')).hexdigest()
        user_entity = UserMapper.dto_to_entity(user_dto, hashed_password)
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return UserMapper.entity_to_dto(user_entity)

    def delete_user(self, email: str) -> None:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            self.db.delete(user_entity)
            self.db.commit()


    # Setters
    def update_user_first_name(self, email: str, first_name: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            user_entity.first_name = first_name
            self.db.commit()
            self.db.refresh(user_entity)
            return UserMapper.entity_to_dto(user_entity)
        return None

    def update_user_last_name(self, email: str, last_name: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            user_entity.last_name = last_name
            self.db.commit()
            self.db.refresh(user_entity)
            return UserMapper.entity_to_dto(user_entity)
        return None

    def update_user_password(self, email: str, new_password: str) -> None:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if not user_entity:
            raise ValueError("User with the specified email not found")

        hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        user_entity.password = hashed_password

        self.db.commit()
        self.db.refresh(user_entity)

    def update_user_phone(self, email: str, phone: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            user_entity.phone = phone
            self.db.commit()
            self.db.refresh(user_entity)
            return UserMapper.entity_to_dto(user_entity)
        return None

    def update_user_gender(self, email: str, gender: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            user_entity.gender = gender
            self.db.commit()
            self.db.refresh(user_entity)
            return UserMapper.entity_to_dto(user_entity)
        return None

    def update_user_country(self, email: str, country: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity:
            user_entity.country = country
            self.db.commit()
            self.db.refresh(user_entity)
            return UserMapper.entity_to_dto(user_entity)
        return None


    # Getters
    def get_user_by_id(self, user_id: int) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    def get_user_by_first_name(self, first_name: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.first_name == first_name).first()
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    def get_user_by_last_name(self, last_name: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.last_name == last_name).first()
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    def get_user_by_email(self, email: str) -> UserDTO:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    def get_user_by_password(self, password: str) -> UserDTO:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_entity = self.db.query(UserEntity).filter(UserEntity.password == hashed_password).first()
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    def get_user_by_email_and_password(self, email: str, password: str) -> Optional[UserDTO]:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_entity = (
            self.db.query(UserEntity)
            .filter(UserEntity.email == email, UserEntity.password == hashed_password)
            .first()
        )
        return UserMapper.entity_to_dto(user_entity) if user_entity else None

    # Getters - multiple rows
    def get_all_users(self) -> List[UserDTO]:
        users = self.db.query(UserEntity).all()
        return [UserMapper.entity_to_dto(user) for user in users]

    def validate_current_password_by_email(self, email: str, current_password: str) -> bool:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if not user_entity:
            raise ValueError("User with the specified email not found")

        hashed_password = hashlib.sha256(current_password.encode('utf-8')).hexdigest()
        return user_entity.password == hashed_password

    def verify_user_by_email(self, email: str) -> None:
        user_entity = self.db.query(UserEntity).filter_by(email=email).first()
        if not user_entity:
            raise ValueError("User not found")
        user_entity.is_verified = True
        self.db.commit()