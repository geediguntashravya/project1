import os
import datetime
import csv

from flask import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)

class Book(db.Model):
    __tablename__="books"
    isbn=db.Column(db.String,primary_key=True)
    title=db.Column(db.String)
    author=db.Column(db.String)
    year=db.Column(db.String)

    def __init__(self,isbn,title,author,year):
        self.isbn=isbn
        self.title=title
        self.author=author
        self.year=year

def main():
    db.create_all()
    file=open("books.csv")
    reader=csv.reader(file)
    for isbn,title,author,year in reader:
        book=Book(isbn=isbn,title=title,author=author,year=year)
        db.session.add(book)
        print(f"Added book of year {year}, isbn: {isbn}, title: {title}, author: {author}.")
    db.session.commit()

if __name__=='__main__':
    with app.app_context():
        main()
