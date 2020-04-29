import os
from imports import *

def find(field,search):
    if field=="isbn":
        list=db.session.query(Book).filter(Book.isbn.like(search))
        return list
    elif field=="title":
        list=db.session.query(Book).filter(Book.title.like(search))
        return list
    elif field=="author":
        list=db.session.query(Book).filter(Book.author.like(search))
        return list
    else:
        list=db.session.query(Book).filter(Book.year.like(search))
        return list

