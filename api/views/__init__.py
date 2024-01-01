#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/')

from .persons import *
from .product import *
from .stock import *
from .sales import *
