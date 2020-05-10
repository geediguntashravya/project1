import os
from imports import *

@app.route('/api/search',methods=['POST','GET'])
def search_api():
    #info=request.get_json()
    key=request.form.get('Search')
    #key=info["key"]
    key="%"+key+"%"
    key=key.title()
    data=db.query(Book).filter(or_(Book.isbn.like(key),Book.title.like(key),Book.author.like(key),Book.year.like(key))).all()
    books={"books":[]}
    for i in data:
        dictionary=dict()
        dictionary["isbn"]=i.isbn
        dictionary["title"]=i.title
        dictionary["author"]=i.author
        dictionary["year"]=i.year
        books["books"].append(dictionary)
    if len(data)<1:
        return jsonify({"success":False})
    else:
        books["successs"]=True
        return jsonify(books)