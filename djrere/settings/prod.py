from ..utils.dict import update_recursive
from .base import *

DEBUG = False

update_recursive(WEBPACK_LOADER, WEBPACK_LOADER_PROD)
