import os
from imports import *

def check_isbn(args):
    return db.session.query(Book).filter(Book.isbn== args)
