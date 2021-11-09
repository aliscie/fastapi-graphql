from icecream import ic

from Users import models
from core.jwt_token import decode_access_token
from db_conf import db_session

db = db_session.session_factory()


def authenticate(resolver, obj, info, **args):
    request = info.context.get('request')

    if request:
        authorization = request._headers.get('authorization')
        try:
            payload = decode_access_token(data=authorization)
            user = db.query(models.User).filter(models.User.username == payload.get('user')).first()
            info.context['user'] = user
        except:
            pass

    value = resolver(obj, info, **args)
    return value

