from ariadne import MutationType
from ariadne import QueryType

from Functions.CRUD import Create
from db_conf import db_session
from posts.models import Post

db = db_session.session_factory()

mutation = MutationType()
query = QueryType()




@mutation.field('post')
def __init__(*args, **kwargs):
    return Create(Post,kwargs)


@query.field('posts')
def resolve_posts(*args, **kwargs):
    return db.query(Post).all()

# @event.listens_for(models.Post, 'after_insert')
# def do_stuff(mapper, connection, target, *args, **kwargs):
#     ic('do_stuffdo_stuffdo_stuffdo_stuff')
#     # ic(mapper, connection, target, args, kwargs)


types = [mutation, query]
