from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import PostgresConfiguration
from models import UserModel
from sqlalchemy.exc import InvalidRequestError

class PosgresHandler:
    def __init__(self, db_string):
        self.engine = create_engine(db_string)
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    # --------------------------------------------------USERS----------------------------------------------------
    def add_user(self, data: dict):
        user = UserModel(**data)
        self.session.add(user)
        try:
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError
        return user

    def get_users(self):
        users = self.session.query(UserModel).all()
        if users:
            return users

    def get_user_by_uuid(self, uuid: str):
        user = self.session.query(UserModel).filter(
            UserModel.user_id == uuid).all()
        if user:
            return user

    def delete_user(self, uuid: int):
        self.session.query(UserModel).filter(UserModel.uuid == uuid).delete()
        try:
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            raise InvalidRequestError


pg_handler = PosgresHandler(PostgresConfiguration().postgres_db_path)