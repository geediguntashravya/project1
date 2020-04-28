import os
import datetime

from flask import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from imports import *
from find import *


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
    return "Project 1: TODO"


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
                return redirect(url_for('account'))
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
        return find(field,search)
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

@app.route("/book",methods=['POST','GET'])
@app.route("/book/<string:args>", methods= ['POST','GET'])
def book(args=None):
    message="This is isbn of the book: "+args
    if request.method=='POST':
        return render_template('book.html',message=message)
    return render_template('book.html',message=message)

