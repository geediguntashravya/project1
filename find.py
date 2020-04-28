import os
from imports import *

def find(field,search):
    if field=="isbn":
        list=db.session.query(Book).filter(Book.isbn.like(search))
        for x in list:
            return render_template('search.html',list=list)
    elif field=="title":
        list=db.session.query(Book).filter(Book.title.like(search))
        for x in list:
            return render_template('search.html',list=list)
    elif field=="author":
        list=db.session.query(Book).filter(Book.author.like(search))
        for x in list:
            return render_template('search.html',list=list)
    else:
        list=db.session.query(Book).filter(Book.year.like(search))
        for x in list:
            return render_template('search.html',list=list)

