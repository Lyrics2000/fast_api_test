from sqlalchemy import Column, Integer, MetaData, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from settings import PostgresConfiguration
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

pg = PostgresConfiguration()
engine = create_engine(pg.postgres_db_path)
meta = MetaData(engine)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user_details'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email_address = Column(String)
    password = Column(String)
    about = Column(String,default="Hi there, I'm new here.")
    profile_picture = Column(String,nullable=True)


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)


if __name__ == '__main__':
    create_tables()
    # Base.metadata.drop_all(engine)


    