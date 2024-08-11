import bcrypt

from jwcrypto import jwk, jwt
from sqlalchemy import inspect

from uuid import uuid4
from datetime import datetime

from config import config


def now():
    return datetime.now()


def generate_id():
    id = str(uuid4())
    return id

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def create_password(password):
    password = bytes(password, "utf-8")
    password = bcrypt.hashpw(password, config["salt"])
    password = password.decode("utf-8")
    return password


