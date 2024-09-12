#!/usr/bin/env python3
"""DB module"""

from user import User, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, tuple_

user_keys = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a user to the database"""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find a user by a given attribute"""
        User_keys = []
        User_values = []
        for key, val in kwargs.items():
            if hasattr(User, key):
                User_keys.append(getattr(User, key))
                User_values.append(val)
            else:
                raise InvalidRequestError()
        returned_item = self._session.query(User).filter(
            tuple_(*User_keys).in_([tuple(User_values)])
        ).first()
        if returned_item is None:
            raise NoResultFound("Not found")
        return returned_item

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates user after getting it"""
        updated_user = self.find_user_by(id=user_id)
        for (key, val) in kwargs.items():
            if key not in user_keys:
                raise ValueError
            setattr(updated_user, key, val)
        self._session.commit()
        return None
