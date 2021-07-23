from random import random
from db_handler import pg_handler
from datetime import datetime
import random

def add_user_to_db(user_data: dict):
    user = pg_handler.add_user(dict(
        username = user_data['username'],
                                    email_address = user_data['email_address'],
                                    password=user_data['password'],
                                    about=user_data['about'],
                                    profile_picture=user_data['profile_picture']
                                    ))