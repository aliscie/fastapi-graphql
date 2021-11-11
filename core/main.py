import contextlib
import importlib

from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from broadcaster import Broadcast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_admin.app import app as admin_app
from icecream import ic
from sqlalchemy import MetaData

from Users import models
from core.MiddleWare.Pagination import pagination
from core.MiddleWare.SearchAndFiltering import serach
from core.jwt_token import decode_access_token
from core.settings import APPS, origins
from db_conf import engine, db_session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

broadcast = Broadcast("redis://redis:6379")
# broadcast = Broadcast("redis://localhost:6379")


meta = MetaData()

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()


@app.on_event("startup")
async def startup_event():
    await broadcast.connect()


@app.on_event("shutdown")
async def startup_event():
    await broadcast.disconnect()


types = []
type_defs = [load_schema_from_path('../../')]

for i in APPS:
    x = importlib.import_module(f'{i}.main')
    try:
        y = importlib.import_module(f'{i}.TypeDefs')
        type_defs.extend(y.type_defs)
    except:
        pass
    types.extend(x.types)

middleware = [pagination, serach]
schema = make_executable_schema(type_defs, *types)

from ariadne.types import Extension


class QueryExecutionTimeExtension(Extension):
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None

    def request_started(self, context):
        self.start_timestamp = ''

    def request_finished(self, context):
        self.end_timestamp = '1'


db = db_session.session_factory()


def context_value(request, *args, **kwargs):
    from urllib.parse import urlparse, parse_qs
    URL = str(request.url)
    parsed_url = urlparse(URL)
    query_string = parse_qs(parsed_url.query)
    token = query_string.get('token')
    context = {}
    if token:
        token = token[0]

    try:
        authorization = request._headers.get('authorization')
        if not token:
            token = authorization
    except:
        pass

    if token:
        try:
            payload = decode_access_token(data=token)
            user = db.query(models.User).filter(models.User.username == payload.get('user')).first()
            context['user'] = user
        except Exception as e:
            ic(e)
    return context


ariadneApp = GraphQL(schema, context_value=context_value, debug=True, middleware=middleware,
                     extensions=[QueryExecutionTimeExtension])
app.mount("/", ariadneApp)
app.mount("/admin", admin_app)