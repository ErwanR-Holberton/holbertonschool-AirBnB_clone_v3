#!/usr/bin/python3
"""import thing here to avoid circular import"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if True:
    from api.v1.views.index import *
    from .states import *
