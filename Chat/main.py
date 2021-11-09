import asyncio
import json
from typing import Any, AsyncGenerator

from ariadne import MutationType
from ariadne import SubscriptionType, QueryType
from celery_sqlalchemy_scheduler.session import SessionManager
from graphql import GraphQLResolveInfo
from icecream import ic

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
sub2 = SubscriptionType()


@query.field("hello")
def __init__(*args, **kwargs):
    # raise AuthenticationError("PLEASE LOGIN")
    return "xxxxxxx"


@mutation.field("send")
async def __init__(obj, info ,*args, **kwargs):
    number = kwargs.get('number')
    user = info.context.get('user')
    if hasattr(user, 'username'):
        username = user.username
    else:
        username = 'anonymous'
    await broadcast.publish(channel="chatroom", message=json.dumps({'message': number, "sender":username }))
    return number


@subscription.source("counter")
async def __init__(obj, info):
    for i in range(4):
        await asyncio.sleep(1)
        yield i


@subscription.field("counter")
def __init__(count, info, *args, **kwargs):
    # request = info.context.get('request')
    # from urllib.parse import urlparse, parse_qs
    # parsed_url = urlparse(f"?{request.scope['query_string'].decode('utf-8')}")
    # token =  parse_qs(parsed_url.query)['token'][0]

    return count


@sub2.source("chat")
async def __init__(_: Any, info: GraphQLResolveInfo) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            yield json.loads(event.message)


@sub2.field("chat")
def __init__(count, info):
    return count


types = [sub2,mutation,  query, subscription]
