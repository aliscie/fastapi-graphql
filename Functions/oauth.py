from icecream import ic

from Functions.CRUD import get_or_create
from Users import models
from db_conf import db_session

db = db_session.session_factory()


def oauth(token):
    from google.oauth2 import id_token
    from google.auth.transport import requests
    client_id = "218303560881-osv51bj8cmnq71sopn3331t2k7stkcvb.apps.googleusercontent.com"
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
    kwargs = {'email': idinfo['email']}
    user, created = get_or_create(db, models.User, **kwargs)
    return user, created
