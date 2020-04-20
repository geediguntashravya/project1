import os
import datetime

from flask import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


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
def register():
    Username=""
    message=""
    if request.method=='POST':
        Username=request.form.get("Username")
        Password=request.form.get("Password")
        Email=request.form.get("Email")
        message=Username+" "+"Successfully registered"
        Timestamp=datetime.datetime.now()
        users=User(Username,Password,Email,Timestamp)
        db.add(users)
        db.commit()
        return render_template("register.html", message=message)
    else:
        return render_template("register.html")


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
        if user!=None:
            if Password==user.Password:
                session['Username']=Username
                return render_template("account.html")
            else:
                return "Invalid password"
        else:
            return "Please check your credentials"

@app.route("/search")
def search():
    if session["Username"]!=None:
        return "Maintained successfully"
    else: 
        return redirect(url_for("/logout"))

@app.route("/logout",methods=['GET','POST'])
def logout():
    session["Username"]=None
    return redirect("/register")


