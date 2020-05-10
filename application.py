import os
import datetime

from flask import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import *
from models import *
from imports import *
from find import *
from sqlalchemy import or_, and_


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="Username"

db.init_app(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    try:
        Username=session["Username"]
        return render_template('userHome.html')
    except:
        return redirect(url_for('register'))


@app.route("/register", methods= ['POST','GET'])
@app.route("/register/<int:args>", methods= ['POST','GET'])
def register(args=None):
    Username=""
    message=""
    if request.method=='POST':
        Username=request.form.get("Username")
        Password=request.form.get("Password")
        Email=request.form.get("Email")
        Timestamp=datetime.datetime.now()
        try:
            if len(Email)<1:
                message="Email mandatory for registration"
                return render_template("register.html",message=message)
            else:
                message=Username+" "+"Successfully registered"
                users=User(Username,Password,Email,Timestamp)
                db.add(users)
                db.commit()
                return render_template("register.html", message=message)
        except:
            message="Already registered, please login"
            return render_template("register.html",message=message)
    else:
        if args==1:
            message="Wrong password"
        elif args==2:
            message="Please register"
        elif args==3:
            message="Session exired"
        elif args==4:
            message="Please login"
        elif args==5:
            message="Logged out successfully"
        else: 
            message=""
        return render_template("register.html",message=message)


@app.route("/admin")
def admin():
    data=db.query(User).order_by(User.Timestamp)
    return render_template('admin.html',list=data)

@app.route("/auth", methods=['POST','GET'])
def auth(): 
    if request.method=='POST':
        Username=request.form.get("Username")
        Password=request.form.get("Password")
        user=User.query.get(Username)
        try:
            if (Username==user.Username) and (Password==user.Password):
                session['Username']=Username
                return redirect(url_for('index'))
            else:
                return redirect(url_for('register',args=1))
        except:
            return redirect(url_for('register',args=2))
    else:
        return redirect(url_for('register',args=4))

@app.route("/search", methods=['POST','GET'])
def search():
    if request.method=='POST':
        field=((request.form['Choose']))
        key=request.form.get('Search') 
        search="%{}%".format(key)
        list=find(field,search)
        return render_template('search.html',list=list)
    else: 
        return render_template('search.html')
    return render_template('search.html')

@app.route('/api/search',methods=['POST','GET'])
def search_api():
    #info=request.get_json()
    key=request.form.get('key')
    #key=info["Search"]
    key="%"+key+"%"
    key=key.title()
    data=db.query(Book).filter(or_(Book.isbn.like(key),Book.title.like(key),Book.author.like(key),Book.year.like(key))).all()
    books={"books":[]}
    if data==None:
        return jsonify({"success":False})
    else:
        for i in data:
            dictionary=dict()
            dictionary["isbn"]=i.isbn
            dictionary["title"]=i.title
            dictionary["author"]=i.author
            dictionary["year"]=i.year
            books["books"].append(dictionary)
        books["success"]=True
        return jsonify(books)

@app.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('register',args=5))

@app.route("/account",methods=['GET','POST'])
def account():
    try:
        Username=session["Username"]
        return render_template('userHome.html')
    except:
        return redirect(url_for('register'))

@app.route("/book",methods=['POST','GET'])
@app.route("/book/<string:args>", methods= ['POST','GET'])
def book(args=None):
    message="This is isbn of the book: "+args
    if request.method=='POST':
        return render_template('book.html',message=message)
    return render_template('book.html',message=message)

@app.route('/api/book',methods=['GET','POST'])
def book_api():
    key=request.form.get("isbn")
    print(key)
    isbn=Book.query.get(key)
    print(isbn)
    return jsonify({"title":isbn.title,"author":isbn.author,"year":isbn.year,"isbn":isbn.isbn})

@app.route('/api/review',methods=['GET','POST'])
def review_api():
    title=request.form.get("title")
    rating=request.form.get("rating")
    review=request.form.get("review")
    data=Review.query.filter(and_(Review.title == title ,Review.username == session.get("Username"))).first()
    if data is None:
        reviewobj = Review(title=title,rating=rating,review=review,Username=session.get("Username"))
        db.add(reviewobj)
        db.commit()
        print("inserted into db")
        # existing_reviews = Review.query.filter_by(title=title).order_by(Review.timestamp.desc()).all()
        # book_details = Book.query.get(title)
        return jsonify({"review":review,"rating":rating})
    else:
        return jsonify({"error":"You have already reviewed this book"})

