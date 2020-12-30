#from passlib.hash import pbkdf2_sha256 as hasher
from flask import current_app
from flask_login import UserMixin
from passlib.hash import sha256_crypt

import dbop 


class User(UserMixin):
    def __init__(self, uid, email, password, name, surname):
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.uid = uid
        self.active = True

    def get_id(self):
        return self.uid

    @property
    def is_active(self):
        return self.active
    
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

def get_user(user_id):
    print(user_id)
    user = None
    if user_id > 0:
        user = dbop.getUser(user_id)
    print("user", user)
    return user