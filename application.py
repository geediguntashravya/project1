import os
import datetime

from flask import *
from flask_session import Session
from sqlalchemy import create_engine,func
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from imports import *
from find import *
from check_isbn import *



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
   
    return render_template('intropage.html')


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

@app.route("/login", methods=['POST','GET'])
def login(): 
    if request.method=='POST':
        Username=request.form.get("Username")
        Password=request.form.get("Password")
        user=User.query.get(Username)
        try:
            if (Username==user.Username) and (Password==user.Password):
                session['Username']=Username
                return redirect(url_for('search'))
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

@app.route("/logout",methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('register',args=5))

@app.route("/account",methods=['GET','POST'])
def account():
    try:
        Username=session["Username"]
        return render_template('account.html')
    except:
        return redirect(url_for('register'))


@app.route("/review/<isbn>", methods =['GET', 'POST'])
def review(isbn=None):
    if session.get("Username") is None:
        return redirect("/register")

    # isbn = "0380795272"
    book  = db.query(Book).filter_by(isbn = isbn).first()
    rating = db.query(Review).filter_by(title=book.title).all()
    # print("hello book name",book.isbn)
    
    # obj = db.query(User).get("Username")
    Uname = session.get("Username")
    print(Uname) 
    if request.method == "POST":
        title = book.title
        rating1 = request.form.get("rate")
        review = request.form.get("comment")
        temp = Review(Uname,title,rating1,review)
        try:
            db.add(temp)
            db.commit() 
            ratin = db.query(Review).filter_by(title=book.title).all()
            return render_template("review.html",data = book, name = Uname, rating = rating)
        except:
            db.rollback()
            return render_template("review.html", data = book, name = "User already given review", rating = rating)
    else:
        return render_template("review.html",data = book, name = Uname ,rating = rating)





@app.route("/book",methods=['POST','GET'])
@app.route("/book/<string:args>", methods= ['POST','GET'])
def book(args=None):
    session['isbn'] = args
    data = check_isbn(args)
    if request.method=='POST':
        return render_template("book.html",list=data)
    return render_template("book.html",list=data)
      
@app.route('/home',methods=['GET','POST'])
def home():
	return render_template("intropage.html")






