#!/usr/bin/env python3
"""encrypt_password.py
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """hash password function """

    hack = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), hack)
    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validate password """
    check = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return (check)
