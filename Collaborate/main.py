import asyncio
import json
from typing import Any, AsyncGenerator

from ariadne import MutationType
from ariadne import SubscriptionType, QueryType
from celery_sqlalchemy_scheduler.session import SessionManager
from graphql import GraphQLResolveInfo
from icecream import ic

from Users.models import User
from core.main import broadcast
from db_conf import beat_dburi
from db_conf import db_session

session_manager = SessionManager()
engine, Session = session_manager.create_session(beat_dburi)
session = Session()

query = QueryType()
subscription = SubscriptionType()
db = db_session.session_factory()
mutation = MutationType()


@mutation.field("collaborate")
async def __init__(obj, info, *args, **kwargs):
    properties = kwargs.get('properties')
    user = info.context.get('user')
    if hasattr(user, 'username'):
        username = user.username
    else:
        username = 'anonymous'
    await broadcast.publish(channel="collaborate", message=json.dumps({'message': properties, "sender": username}))
    return properties


@subscription.source("collaborate")
async def __init__(_: Any, info: GraphQLResolveInfo) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="collaborate") as subscriber:
        async for event in subscriber:
            message = json.loads(event.message)
            sender = message.get('sender')
            user = info.context.get('user')
            ic(sender, user.username)
            if sender != user.username:
                yield message


@subscription.field("collaborate")
def __init__(data, info):
    return data


types = [mutation, subscription]
