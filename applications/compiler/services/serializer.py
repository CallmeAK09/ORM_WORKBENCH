import json

from django.db import models

def serialize_value(val):
    """
    Conver field value into json-string to display in frontend,
    date/datetime -> ISO string eg:"2026-07-30 12:30"
    Non serializables like UUID, Decimal -> str()
    """

    import datetime
    import uuid
    
    from decimal import Decimal

    if val is None:
        return None
    if isinstance(val, bool):
        return str(val)
    if isinstance(val, (Decimal, uuid.UUID)):
        return str(val)
    if isinstance(val, (datetime.datetime,)):
        return val.strftime('%y-%m-%d %H:%M')
    if isinstance(val, datetime.date):
        return val.strftime('%y-%m-%d')
    if isinstance(val, dict):
        return {k: serialize_value(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [serialize_value(v) for v in val]

    try:
        json.dumps(val)
        return val
    except(ValueError, TypeError):
        return str(val)

def get_record_dict(instance, model):
    """
    Build a display friendly dictionary for a single model instance
    - ForeignKey Fields : id + __str__ of the related_name values
    - ManyToMany Fields : __str__values
    - Other Fields : raw value
    """

    record = {}

    # Regular fields
    for field in model._meta.fields:
        val = getattr(instance, field.attname)
        record[field.name] = serialize_value(val)

        # Foreign Key fields
        if isinstance(field, models.ForeignKey):
            try:
                related_obj = getattr(instance, field.name)
                if related_obj is not None:
                     record[field.name + '__str'] = str(related_obj)
                else:
                     record[field.name + '__str'] = None
            except Exception:
                 record[field.name + '__str'] = None

    # Many To Many fields
    for field in model._meta.many_to_many:
        try:
            related_qs = getattr(instance, field.name).all()
            record[field.name] = ', '.join(str(obj) for obj in related_qs) or '-'
        except Exception:
            record[field.name] = '-'

    return record

def get_field_name(model):
    """ 
    Rturn the ordered list of column headers,
    Insert FK + __str column right after FK.id column
    """

    columns = []

    for field in model._meta.fields:
        columns.append(field.name)
        if isinstance(field, models.ForeignKey):
            columns.append(field.name + '__str')

    for field in model._meta.many_to_many:
        columns.append(field.name)

    return columns