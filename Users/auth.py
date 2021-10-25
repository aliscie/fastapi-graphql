from datetime import timedelta

import bcrypt
from ariadne import MutationType
from icecream import ic

from Users import models
from core.jwt_token import create_access_token, decode_access_token
from db_conf import db_session

db = db_session.session_factory()

mutation = MutationType()


class AuthenticationError(Exception):
    extensions = {"code": "UNAUTHENTICATED"}


class DuplicateError(Exception):
    extensions = {"code": "UNAUTHENTICATED"}


@mutation.field("signin")
def __init__(*args, **kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    access_token_expires = timedelta(minutes=60)

    db_user_info = db.query(models.User).filter(models.User.username == username).first()
    if not db_user_info:
        return 'user not found'
    access_token = create_access_token(data={"user": username}, expires_delta=access_token_expires)
    encrption = bcrypt.checkpw(password.encode("utf-8"), db_user_info.password.encode("utf-8"))

    if encrption:
        return access_token
    else:
        return AuthenticationError("invalid credentials.")


@mutation.field("signup")
def __init__(*args, **kwargs):
    password = kwargs.get('password')
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    data = {}
    for i in models.User.__table__.columns.keys():
        if i != 'id':
            data[i] = kwargs.get(i)
    data['password'] = hashed_password.decode("utf8")

    db_user = models.User(**data)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return True
    except Exception as e:
        db.rollback()
        raise DuplicateError("User with this information already exists.")
