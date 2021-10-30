def make_relational_schemas(model):
    d = """
    """
    from sqlalchemy import inspect
    thing_relations = inspect(model).relationships.items()
    for key, item in thing_relations:
        name = item.target.name.title()
        if item.uselist:
            d += f"""
                            {key}: [{name}]
                            """
        else:
            d += f"""
                            {key}: {name}
                            """
    return d


def make_schemas(model, is_list=True):
    name = model.__tablename__

    d = """
        """
    d += make_relational_schemas(model)
    for i, key in model.__table__.columns.items():
        x = str(key.type.python_type)
        x = x.replace("<class '", '')
        x = x.replace("'>", '')
        x = x.title()
        if x in ['Str', 'Datetime.Datetime']:
            x = 'String'
        if x == 'Bool':
            x = 'Boolean'
        d += f"""
                {i}: {x}
                """

    y = f"""
    type {name.title()} {{
    {d}
    }}
    """

    if is_list:
        y += f"""
            extend type Query{{
            {name.lower()}(input: ListInput): [{name.title()}]
            }}
            """
    return y
