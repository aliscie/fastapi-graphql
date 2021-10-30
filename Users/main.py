import asyncio

from ariadne import QueryType
from icecream import ic
from sqlalchemy import inspect

from Users import models
from Users.auth import mutation
from db_conf import db_session
from posts.models import Post

db = db_session.session_factory()


users_query = QueryType()


def send_auth_email(user):
    asyncio.sleep(1)
    print(f'verification email is sent to {user}')


@users_query.field("users")
def __init__(_,info, *args, **kwargs):
    users = db.query(models.User).all()
    return users


types = [mutation, users_query]
