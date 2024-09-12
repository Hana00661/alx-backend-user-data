#!/usr/bin/env python3
"""auth.py"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """a user with the provided email and password"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """check the password with bcrypt.checkpw.
        If it matches return True.other wise, return False"""

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """find the user corresponding to the email,then return session ID"""

        try:
            user = self._db.find_user_by(email=email)
            session_ID = _generate_uuid()
            self._db.update_user(user.id, session_id=session_ID)
            return session_ID
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """get the user corresponding to the session ID."""
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy the session ID"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """reset the password"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """update the password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id, reset_token=None,
                                 hashed_password=_hash_password(password))
        except NoResultFound:
            raise ValueError()
