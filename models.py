from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"
    Username    =   db.Column(db.String, primary_key=True)
    Password    =   db.Column(db.String,nullable=False)
    Email       =   db.Column(db.String,nullable=False)
    Timestamp   =   db.Column(db.DateTime,nullable=False)

    def __init__(self, Username, Password, Email, Timestamp):
        self.Username = Username
        self.Password = Password
        self.Email = Email
        self.Timestamp= Timestamp


class review(db.Model):
    __tablename__ = "review"
    title = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, primary_key=True)
    rating = db.Column(db.String, nullable=False)
    review = db.Column(db.String, index=False, unique=False, nullable=False)

    def __init__(self, Username, title, rating, review):
        
        self.title = title
        self.username = Username
        self.rating = rating
        self.review = review