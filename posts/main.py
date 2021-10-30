from ariadne import MutationType
from ariadne import QueryType
from icecream import ic

from Functions.CRUD import Create
from Users import models
from db_conf import db_session, Base, engine
from posts.models import Post

db = db_session.session_factory()

mutation = MutationType()
query = QueryType()




@mutation.field('post')
def __init__(*args, **kwargs):

    return Create(Post,kwargs)


@query.field('posts')
def resolve_posts(*args, **kwargs):
    # Base.metadata.drop_all(engine)  # all tables are deleted
    # x = db.query(models.User).all()
    # x.delete()
    # x = db.query(Post).all()
    # x.delete()
    # x.commit()
    posts = db.query(Post).all()
    return posts

# @event.listens_for(models.Post, 'after_insert')
# def do_stuff(mapper, connection, target, *args, **kwargs):
#     ic('do_stuffdo_stuffdo_stuffdo_stuff')
#     # ic(mapper, connection, target, args, kwargs)


types = [mutation, query]
