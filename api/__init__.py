from flask import Blueprint
api=Blueprint('format',__name__)
api=Blueprint('member',__name__)

from .format import *
from .member import *