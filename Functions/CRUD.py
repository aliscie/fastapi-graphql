from db_conf import db_session

db = db_session.session_factory()


def Create(Model, original_Data):
    data = {}
    for i in Model.__table__.columns.keys():
        if i != 'id':
            data[i] = original_Data.get(i)
    db_post = Model(**data)
    db.add(db_post)
    try:
        db.commit()
        db.refresh(db_post)
        ok = True
    except Exception as e:
        db.rollback()
        ok = False
    return ok


def Update(self, *args, **kwargs):
    pass


def Delete(self, *args, **kwargs):
    pass


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True