# -*- coding: utf-8 -*-
"""
Handles all User interaction.

Could have a database backend, or plaintext.
"""
import os
import json

from flask import current_app
from flask_login import UserMixin

from baseapp.extensions import bcrypt


class User(UserMixin):
    DB = {1: {'id': 1,
              'username': 'admin',
              'email': 'admin@example.com',
              'password': '$2a$13$hOFH6WESLLl0csqOlQIZvuBz'
                          'Qh5TMFY3364U44iMiMcqscvQpL6WK',
              'first_name': 'Admin',
              'last_name':'Istrator',
              'is_admin': True,
              'active': True }}
    _USER_DICT = {'id':'', 'username': '', 'email': '', 'password': '', # HASHED
                  'first_name': '', 'last_name': '', 'is_admin': False,
                  'active': False, }

    def __init__(self, **kwargs):
        self.__dict__.update(self._USER_DICT.copy())  # is copy necessary?
        for arg in self._USER_DICT.keys(): # limit kwargs to known values
            if arg in kwargs:
                self.__dict__[arg] = kwargs[arg]

    def set_password(self, password):
        if not password:
            self.password = None
        else:
            self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def is_active(self):
        """Method expected by Flask Login."""
        return self.active

    def is_authenticated(self):
        """Checks for loggedin-ness"""
        sessionfile = current_app.config.get("SESSION_LOG_FILE_PATH")
        if not os.path.exists(sessionfile):
            return False
        try:
            data = json.load(open(sessionfile))
        except ValueError:
            return False
        try:
            return data.get(str(self.id), None)
        except AttributeError:
            pass
        return False

    def authenticate(self, is_authentic=False):
        """Sets loggedin-ness. VERY vulnerable to race conditions."""
        sessionfile = current_app.config.get("SESSION_LOG_FILE_PATH")
        try:
            data = json.load(open(sessionfile))
        except (ValueError, OSError):
            data = {}
        data[str(self.id)] = is_authentic
        try:
            with open(sessionfile, 'w') as fh:
                json.dump(data, fh)
        except OSError:
            print("Whelp writing {} failed.".format(sessionfile))

    def __repr__(self):
        return '<User({}:{})>'.format(self.id, self.username)

    @staticmethod
    def get_by_id(user_id):
        return User.search(user_id=user_id)

    @staticmethod
    def search(user_id=None, username=None, email=None):
        """Searches USER database, returns User object in search order:
        ID > username > email
        """
        found_user = None
        if email is not None:
            for db_id, user in User.DB.items():
                if user['email'] == email:
                    found_user = user
        if username is not None:
            for db_id, user in User.DB.items():
                if user['username'] == username:
                    found_user = user
        if user_id is not None and user_id in User.DB:
            found_user = User.DB[user_id]
        if not found_user:
            return None
        return User(**found_user)

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping User(**kwargs)."""
        return User(**kwargs)
